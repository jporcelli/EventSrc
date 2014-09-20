from Main.models import Event, EventForm, EventPhoto, Attendance
from django.template import RequestContext, loader 
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from datetime import date
from EventSource import settings
import os
import hashlib
import json
import redis


"""
    Load EventSrc main page
"""
@login_required
def home(request):
    temp = loader.get_template('main.html')
    
    # Current client
    cur_user = request.user
    
    entries = {}
    
    # Get data that requires the user to be authenticated
    if cur_user.is_authenticated():
        events_created = Event.objects.filter(owner_id = cur_user)
        
        # @todo: Implement pagination for client created event list in UI
        entries['events_created'] = events_created
        
        # @todo: As noted in Login.views the client lat, lng, cordinates may be better
        # passed in the clients session during the login handling in Login.views so they
        # dont have to become part of the Home URI
        
        # The clients current position cordinates
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        
        # @todo: Implement more complex, event suggestion, finding, algorithms
        
        # Lookup events in client location, not created by the client
        events = findEvents(lng, lat, cur_user)
        
        # Lookup events the client is attending
        planned_events = Attendance.objects.filter(user = cur_user)
        
        entries['my_events'] = planned_events
    else:
        # All other data not requiring authentication
        
        # Lookup events in client location
        events = findEvents(lng, lat, None)
            
    entries['events_in_area'] = events
    
    context = RequestContext(request, entries)
    return HttpResponse(temp.render(context))


"""
    Django Geo-spatial query based using the Event_Point model.
    Locates Event_Point' within q_radius km's from the client position
    and uses the Event_Points to obtain the corresponding Events.
    
    @param lng: The client position longitude cordinate
    @param lat: The client position latitude cordinate
    @param client_id: The User.id PK of the client
    @param q_radius: The radius to search around the clients location for events   
    @return: List of Event objects in and around the client location    
"""
def findEvents(lng, lat, client_id, q_radius=5):
    pnt = fromstr("POINT({0} {1})".format(lng, lat), srid=4326)
    
    # Find point objects within q_radius km from the center point = (lat, lng)
    events = Event.objects.filter(latlng__distance_lte = (pnt, D(km = q_radius))).exclude(owner = client_id)
        
    return events


"""
    Saves a new Event to the database including a corresponding Event_Point object.
    
    @attention: This is an XHR request (asynchronous)
    
    @param request: The HTTP POST request containing the request
    @return: JSON serialization of the Event object created and saved  
"""
@csrf_exempt
def newEvent(request):
    eventForm = EventForm(request.POST)
    
    if eventForm.is_valid():  
        event = eventForm.save(commit=False)
        
        user = request.user
        event.owner = user
        
        point = fromstr("POINT({0} {1})".format(event.longitude, event.latitude), srid=4326)
        
        event.latlng = point
        
        # @todo: Add event creator contact information from user object or seperatly

        event.save()
        
        for photo_hash in request.POST.getlist('event_photo_upload'):
            
            # @todo: Should use a redis list to store clients photo upload meta data and then delete the list when done
            photo_meta = request.session[photo_hash]
            
            event_photo = EventPhoto()
            
            event_photo.event = event
            event_photo.name = photo_meta['name']
            event_photo.size = photo_meta['size']
            event_photo.type = photo_meta['type']
            event_photo.hash_key = photo_hash
            
            # Persist the event photo
            event_photo.save()
            
            # Remove the photo meta data from the session once its persisted
            del request.session[photo_hash]
        
            # @todo: Must delete all photo upload meta data from the client session once the request is completed
            # e.g the deleted photo meta data still peristent in the session 
        
        json_data = serializers.serialize('json', [event,])
        
        struct = json.loads(json_data)
        data = json.dumps(struct[0])
        
        # Return the event object created in JSON format
        return HttpResponse(data, content_type='application/json')
    else:        
        # @todo: Find a better approach then returning None='null'
        return HttpResponse(None, content_type='application/json')


"""
    Handles the uploading, processing, and persisting, of a photo for a new
    event
    
    @attention: This is an XHR request (asynchronous)
    
    @param request: The HTTP POST request containing the request    
    @return: JSON encoded list of the uploaded file hash keys
"""
@csrf_exempt
def newEventFileUpload(request):
    
    # @todo: The format of the returned JSON file object should probably be improved 
    uploaded_file = {}
    
    for _, f in request.FILES.iteritems():
        
        f_type = f.content_type
        size = f.size
        
        uploaded_file['size'] = size
        uploaded_file['name'] = f.name
        uploaded_file['type'] = f_type
        
        # The actual usable file type extension, not a string description
        f_type_usable = f.name.split('.')[1]
        
        created_on = date.today()
        s_created_on =  created_on.isoformat()
        
        # Using a concatanation of the file properties to avoid collisions
        storage_key = f.name + str(size) + str(f_type) + s_created_on
        
        hash_instance = hashlib.md5(storage_key.encode())
        hash_key = hash_instance.hexdigest() 
        
        uploaded_file['hash'] = hash_key
        
        storePhoto(hash_key, f)
        
        # @todo: Should use a redis list to store clients photo upload meta data and then delete the list when done
        request.session[hash_key] = {'name' : f.name, 'size' : size, 'type' : f_type_usable}
        
    data = json.dumps(uploaded_file)
    
    # Return a JSON representation of the uploaded file
    return HttpResponse(data, content_type='application/json')


"""
    Deletes the file given by the hash key in the parameter from the storage
    
    @param photo_hash: The hash key identifying the photo on the storage
    @param request: The HTTP POST request containing the request     
    
    @todo Add functionality to be able to delete photos after the meta data
    has been created e.g not just during the creation of a new event, but also
    during the editing of an existing event **
"""
@csrf_exempt
def newEventPhotoDelete(request, photo_hash):
    os.remove('/storage/photos/{0}'.format(photo_hash))


"""
    Write the photo to storage in chunks to limit the use memory
    
    @param hash: The unique hashed encoding used to indentify the file
    @param file: The actual file instance
     
    @note: The hash includes a file type suffix
"""
def storePhoto(file_hash, f):
    with open(os.path.join(settings.BASE_DIR, 'storage/photos/{0}'.format(file_hash)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
