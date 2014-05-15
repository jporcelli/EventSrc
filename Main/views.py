from django.shortcuts import render
from django.template import RequestContext, loader 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
import urllib2
import json


"""
Load EventSrc main page
"""
def home(request):
    temp = loader.get_template('main.html')
    context = RequestContext(request, {})
    return HttpResponse(temp.render(context))


"""
Facebook login django extension for use with facebook javascript login api
"""
def fbLogin(request):
    # Handle facebook Oauth
    accessToken = request.GET.get('accessToken')
    userId = request.GET.get('userId')
    
    #validate the access token recieved form the javascript facebook login api
    fb_res = urllib2.urlopen('https://graph.facebook.com/me?access_token=' + accessToken)
    data = json.load(fb_res)
                
    if not data.get('error') and str(data['id']) == userId:
        user = authenticate(username=str(data['name']), password=str(data['id'])) 
        
        #returning user            
        if user is not None:
            if user.is_active:
                login(request, user)
                            
                # @todo: see Instagram Redis session example
                            
                # successful login
                return put_json({'status' : 'success'})
            else:
                # disabled account
                return put_json({'status' : 'error', 'message': 'disabled account'})
                            
        # User could not be authenticated using django auth, may be first login
        else:
            if data.get('email'):
                email = data.get('email')
            else:
                email = None
            
            #create new user 
            user = User.objects.create_user(str(data['name']), str(email), str(data['id']))
            
            #New user so persist the user to the django auth backend
            user.save()
            authenticate(username=user.username, password=user.password)
                        
            if user is not None:
                if user.is_active:
                    login(request, user)

                    # sucesss
                    return put_json({'status' : 'success'})
                else:
                    # Error, new users should be active
                    return put_json({'status' : 'error', 'message' : 'server error'})
                                
            else:
                # Error, new user should authenticate
                return put_json({'status' : 'error', 'message' : 'server error'})
    else:
        return put_json({'status' : 'error', 'message' : 'FB error'})

"""
Logout 
"""
def _logout(request):
    logout(request)
    return put_json({'status' : 'success'})

"""
Persist a new event 
"""
def newEvent(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    address = request.POST.get('address')
    type = request.POST.get('type')
    datetime = request.POST.get('datetime')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    
    
    #If this doesnt work, @todo: does the sessionid cookie correspond to the _id PK
    #of users in the DB? if so simply set the uid field to that PK value
    user = request.session['user']
    
    event = Event(owner=user.id, )
    
    if event is not None:
        return put_json({'status' : 'success'})
    else:
        return put_json({'status' : 'error', 'message' : 'event not saved'})
        
"""
Helper method for returning JSON content
"""
def put_json(context):
    return HttpResponse(json.dumps(context), content_type='application/json')
