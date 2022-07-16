from django.urls import path, include
from .views import sections_home,repartition_longitudinal_home,Add_repartition_longitudinal,repartition_longitudinal_detail
urlpatterns = [
   
    path('',sections_home, name='sections_home'),
    path('repartition_longitudinal_home/',repartition_longitudinal_home, name='repartition_longitudinal_home'),
    path('repartition_longitudinal-detail/<slug>/',repartition_longitudinal_detail, name='repartition_longitudinal_detail'),
    path('Add_repartition_longitudinal/',Add_repartition_longitudinal, name='Add_repartition_longitudinal'),
    

    

   
]