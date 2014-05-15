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
Form for new event submission
"""
class NewEventForm(forms.Form):
    title = forms.CharField()
    address = forms.CharField()
    type = forms.CharField()
    datetime = forms.CharField()

"""
Persist a new event 
"""
def newEvent(request):
    newEvent = NewEventForm(request.POST)
    event = newEvent.save()
    
    if event is not None:
        
"""
Helper method for returning JSON content
"""
def put_json(context):
    return HttpResponse(json.dumps(context), content_type='application/json')
