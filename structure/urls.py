
from django.urls import path, include
from .views import add_poutre,poutre_home,poutre_detail,add_corniche,corniche_detail,corniche_home,trottoir_home,trottoir_detail,add_trottoir,glissiere_home,glissiere_detail,add_glissiere,add_garde_corps,garde_corps_detail,garde_corps_home,add_dalle,dalle_detail,dalle_home,add_tablier,tablier_detail,tablier_home



urlpatterns = [
    path('dalles/', dalle_home, name='dalle_home'),
    path('dalle-detail/<slug>/', dalle_detail, name='dalle_detail'),
    path('dalles/add_dalle/', add_dalle, name='add_dalle'),


    path('poutres/', poutre_home, name='poutre_home'),
    path('poutres-detail/<slug>/', poutre_detail, name='poutre_detail'),
    path('poutres/add_poutre/', add_poutre, name='add_poutre'),

    path('corniches/', corniche_home, name='corniche_home'),
    path('corniche/add_corniche/', add_corniche, name='add_corniche'),
    path('corniche-detail/<slug>/', corniche_detail, name='corniche_detail'),

    path('trottoirs/', trottoir_home, name='trottoir_home'),
    path('trottoirs/add_trottoir/', add_trottoir, name='add_trottoir'),
    path('trottoirs-detail/<slug>/', trottoir_detail, name='trottoir_detail'),

    path('glissiere/', glissiere_home, name='glissiere_home'),
    path('glissiere/add_glissiere/', add_glissiere, name='add_glissiere'),
    path('glissiere-detail/<slug>/', glissiere_detail, name='glissiere_detail'),

    path('garde_corps/', garde_corps_home, name='garde_corps_home'),
    path('garde_corps/add_garde_corps/', add_garde_corps, name='add_garde_corps'),
    path('garde_corps-detail/<slug>/', garde_corps_detail, name='garde_corps_detail'),

    path('tablier/add_tablier/', add_tablier, name='add_tablier'),
    path('tablier-detail/<slug>/', tablier_detail, name='tablier_detail'),
    path('tablier/', tablier_home, name='tablier_home'),
  
   
]