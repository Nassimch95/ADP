from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import platelage_home,platelage_add,platelage_detail

urlpatterns = [
    
    path('home/', platelage_home,name="platelage_home"),
    path('platelage_add/', platelage_add,name="platelage_add"),
    path('detail_platelage/<slug>',platelage_detail, name='platelage_detail'),
    
]