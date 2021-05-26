from django.urls import path
from .views import PresentazioneTemplateView
urlpatterns = [
    path('', PresentazioneTemplateView.as_view(), name="presentazione-view")
]
