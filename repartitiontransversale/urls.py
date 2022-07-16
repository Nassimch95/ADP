from django.urls import path, include

from .views import repartition_transversale_home,add_repartition_transversale,repartition_transversale_detail
urlpatterns = [
   
    path('',repartition_transversale_home, name='repartition_transversale_home'),
    path('add_repartition_transversale/',add_repartition_transversale, name='add_repartition_transversale'),
    path('detail_repartition_transversale/<slug>',repartition_transversale_detail, name='repartition_transversale_detail'),
    
   
]
