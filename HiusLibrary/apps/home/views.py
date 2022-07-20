from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render({}, request))