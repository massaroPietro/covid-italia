from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage_view'),
    path('regione/<slug:codice_istat>/', views.regione_detail, name='regione_detail'),
    path('notizie/', views.notizie_list_view, name='notizie_list_view'),
]


