from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import precontrainte_home,precontrainte_add,precontrainte_detail

urlpatterns = [
    
    path('home/', precontrainte_home,name="precontrainte_home"),
    path('precontrainte_add/', precontrainte_add,name="precontrainte_add"),
    path('detail_precontrainte/<slug>',precontrainte_detail, name='precontrainte_detail'),
    
]
