from django.http import HttpResponse
from django.shortcuts import render,redirect
from slider.models import Slider

def index(request):
    slider = Slider.objects.all()

    data = {
        'slider':slider,
    }
    return render (request,'index.html',data)















