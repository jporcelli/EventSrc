from django.shortcuts import render
from django.template import RequestContext, loader 
from django.http import HttpResponse

# Create your views here.

def home(request):
    temp = loader.get_template('main.html')
    context = RequestContext(request, {})
    return HttpResponse(temp.render(context))