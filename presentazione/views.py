from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class PresentazioneTemplateView(TemplateView):
    template_name = 'presentazione/index.html'
