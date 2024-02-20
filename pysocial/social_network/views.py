from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets, mixins

def index(request):
    return render(request, 'social_network/index.html')

























