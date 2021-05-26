from django.urls import path
from .views import PresentazioneTemplateView, PythonTemplateView
urlpatterns = [
    path('', PresentazioneTemplateView.as_view(), name="presentazione-view"),
    path('python/', PythonTemplateView.as_view(), name="python-view")
]
