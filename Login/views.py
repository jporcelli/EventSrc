from django.shortcuts import render
from django.template import RequestContext, loader 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Main.models import Event
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import View
from django.shortcuts import redirect
import urllib2
import json

"""
    Form to authenticate a user
"""
class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

"""
    Authenticate a user for EventSrc using standard django login
"""
class Login(View):
    
    def get(self, request, *args, **kwargs):
        entries = {}
        
        temp = loader.get_template('login.html')
        context = RequestContext(request, entries)
        return HttpResponse(temp.render(context))
        
    def post(self, request, *args, **kwargs):
        entries = {}
        form = loginForm(request.POST)
        
        if form.is_valid():                        
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = django_login(request, username, password)
            
            if user is not None:
                temp = loader.get_template('main.html')
                
                # @todo: Should provide a routine for getting the client cordinates which uses a fallback
                # to GeoIp database lookup by client IP address if GeoLocation HTML5 is not enabled
                
                # @todo: Consider using the client session to store the clients lat, lng, cordinates instead
                # of passing them as request GET parameters which then become part of the Home URI
                
                # Get the client position cordinates
                lat = request.GET.get('lat')
                lng = request.GET.get('lng')
                
                # Add HTTP GET parameters for geolocation current lat,lng            
                return redirect('/Home/?lat=' + lat + '&lng=' + lng)
            else:
                temp = loader.get_template('login.html')
        else:
            messages.error(request, 'Invalid Username/Password')
            temp = loader.get_template('login.html')
            
        context = RequestContext(request, entries)
        return HttpResponse(temp.render(context))

"""
    Login using username, password with Djangos Auth system
"""
def django_login(request, username, password):
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, 'Account Has Been Deactivated')
            return None
    else:
        messages.error(request, 'Invalid Username/Password')
        return None
    
    return user

"""
    Login to Djangos Auth system by authenticating with Facebook
"""
def djangoFb_login(request):
    entries = {}
    
    # Handle facebook Oauth
    accessToken = request.GET.get('accessToken')
    userId = request.GET.get('userId')
    
    # validate the access token recieved form the javascript facebook login api
    fb_res = urllib2.urlopen('https://graph.facebook.com/me?access_token=' + accessToken)
    data = json.load(fb_res)
    
    # Process the FB login results through Django auth
    if not data.get('error') and str(data['id']) == userId:
        user = django_login(request, username=str(data['name']), password=str(data['id']))
        
        if user is None:
            # If FB login credentials are not in the Django auth, register them with Django auth and
            # process the login
            
            # If the email field (not required) was provided get it and include it with the registration
            if data.get('email'):
                email = data.get('email')
            else:
                email = None 
                
            # create new user 
            # @todo: Is storing FB users password as their FB id secure?
            user = User.objects.create_user(str(data['name']), str(email), str(data['id']))
            
            # New user so persist the user to the django auth backend
            user.save()         
        else:
            # FB credentials are in Django Auth, proceed with login
            pass

        temp = loader.get_template('main.html')   
        
        # @todo: Should provide a routine for getting the client cordinates which uses a fallback
        # to GeoIp database lookup by client IP address if GeoLocation HTML5 is not enabled
        
        # @todo: Consider using the client session to store the clients lat, lng, cordinates instead
        # of passing them as request GET parameters which then become part of the Home URI
        
        # Get the client position cordinates
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
                
        # Add HTTP GET parameters for geolocation current lat,lng and redirect to Main.home           
        return redirect('/Home/?lat=' + lat + '&lng=' + lng)   
    
    else:
        # FB login returned error
        messages.error(request, 'Facebook Login Error')
        temp = loader.get_template('login.html')     
        context = RequestContext(request, entries)
        return HttpResponse(temp.render(context))

"""
    Facebook django login extension for use with facebook javascript login api
"""
@csrf_protect
def fbLogin(request):
    return djangoFb_login(request)

"""
    Logout 
"""
def _logout(request):
    logout(request)
    
    temp = loader.get_template('login.html')
    entries = {}
    
    context = RequestContext(request, entries) 
    return HttpResponse(temp.render(context))

    
    
