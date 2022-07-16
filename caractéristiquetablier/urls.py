
from django.urls import path, include
from .views import Ct_view,Ct_add,Caracteristique_tablier_detail

urlpatterns = [
   
    path('', Ct_view, name='Ct_view'),
    path('caracteristique-detail/<slug>/', Caracteristique_tablier_detail, name='caracteristique-detail'),
    path('options/add/', Ct_add, name='Ct_add'),
   
]