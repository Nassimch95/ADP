
from django.urls import path, include
from .views import HomeGeometry,AddSection_01, AddSection_02, GeometryDetail,geometry_csv_export, repartition_BC,MG_view,qtr_view,A_view,MC120_view,Bt_critique_view,Bt_view


urlpatterns = [
   
    path('', HomeGeometry, name='GeometryHome'),
    path('add/type_01/', AddSection_01, name='AddSection_01'),
     path('add/type_02/', AddSection_02, name='AddSection_02'),
    path('section/<slug>/', GeometryDetail , name='GeometryDetail'),
    path('geometry_csv_export/<id>/', geometry_csv_export , name='geometry_csv_export'),
    path('repartition_BC/', repartition_BC , name='repartition_BC'),
    path('MG/', MG_view, name='MG_view'),
    path('qtr/', qtr_view, name='qtr_view'),
    path('A/', A_view, name='A_view'),
    path('MC120/', MC120_view, name='MC120'),
    path('BtC/', Bt_critique_view, name='BtC'),
    path('Bt/', Bt_view, name='Bt'),

   
]