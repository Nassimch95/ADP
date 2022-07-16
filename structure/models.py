from django.db import models
from geometry.models import SectionAdded,  section_type_01,section_type_02
from cart.models import Cart
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class dalle(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    pvd                    = models.FloatField(  default=00.0000)
    b_dalle                = models.FloatField(  default=00.0000)
    h_dalle                = models.FloatField(  default=00.0000)
    L_dalle                = models.FloatField(  default=00.0000,null=True, blank=True)
    h_dalle                = models.FloatField(  default=00.0000)
    S_dalle                = models.FloatField(  default=00.0000,null=True, blank=True)
    V_dalle                = models.FloatField(  default=00.0000,null=True, blank=True)
    P_dalle                = models.FloatField(  default=00.0000,null=True, blank=True)
    


    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('dalle_detail', kwargs={'slug': self.slug})



def unique_slug_generator_dalle_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_dalle_pre_save_receiver, sender=dalle)


    


class poutre (models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    pvp                    = models.FloatField(  default=00.0000)
    sa                     = models.ForeignKey(SectionAdded,on_delete=models.CASCADE,null=True, blank=True,related_name='section_about')
    L_poutre               = models.FloatField(  default=00.0000,null=True, blank=True)
    l_sa                   = models.FloatField(  default=00.0000)

    cs_1              = models.FloatField(  default=00.0000)
    l_cs_1            = models.FloatField(  default=00.0000)

    si                = models.ForeignKey(SectionAdded,on_delete=models.CASCADE,null=True, blank=True,related_name='section_intermediaire')
    l_si              = models.FloatField(  default=00.0000)

    cs_2              = models.FloatField(  default=00.0000)
    l_cs_2            = models.FloatField(  default=00.0000)


    sm                = models.ForeignKey(SectionAdded,on_delete=models.CASCADE,null=True, blank=True,related_name='section_mediane')
    l_sm              = models.FloatField(  default=00.0000)

    S                 = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    L                 = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    L_total_sections  = models.FloatField(  default=00.0000,null=True, blank=True)
    V                 = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    vtp               = models.FloatField(  default=00.0000)
    

    np                = models.FloatField(  default=00.0000) #nombre de poutre

    ep                = models.FloatField(  default=00.0000) #entreaxe des poutre

    epdr              = models.FloatField(  default=00.0000) #entreaxe des poutre de rives 

    pp                = models.FloatField(  default=00.0000) #poids de la poutre

    ptp               = models.FloatField(  default=00.0000,null=True, blank=True,) #poind total

    # entretoise 
    pve                = models.FloatField( null=True, blank=True,) # masse volumique entretoise
    epaisseur_e        = models.FloatField(  default=0.3000,null=True, blank=True,) #poind total
    d_chevetre                 = models.FloatField(  default=0.5000,null=True, blank=True,) #poind total
    S_e                        = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    S_e_total                  = models.FloatField(  default=00.0000,null=True, blank=True,) #poind total
    
    V_e                         = models.FloatField(  default=00.000,null=True, blank=True,) #poind total
    P_e              = models.FloatField(  default=00.000,null=True, blank=True,) #poind total  
    pt_e                        = models.FloatField(  default=00.000,null=True, blank=True,) #poind total
    
    #pre_dale 

    b_pre_dalle          = models.FloatField(  default=00.0000,null=True, blank=True,)
    h_pre_dalle          = models.FloatField(  default=00.0000,null=True, blank=True,)
    S_pre_dalle          = models.FloatField(  default=00.0000,null=True, blank=True,)
    S_total_pre_dalle    = models.FloatField(  default=00.0000,null=True, blank=True,)
    V_total_pre_dalle    = models.FloatField(  default=00.0000,null=True, blank=True,)
    P_pre_dalle           = models.FloatField(  default=00.0000,null=True, blank=True,)



    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('poutre_detail', kwargs={'slug': self.slug})



def unique_slug_generator_poutre_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_poutre_pre_save_receiver, sender=poutre)



class corniche(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    Pvc                    =  models.FloatField(  default=00.0000,null=True, blank=True,)
    b_rectangle = models.FloatField(  default=00.0000)
    h_rectangle = models.FloatField(  default=00.0000)

    b_grand_triangle =  models.FloatField(  default=00.0000)
    h_grand_triangle = models.FloatField(  default=00.0000)

    b_petit_triangle = models.FloatField(  default=00.0000)
    h_petit_triangle = models.FloatField(  default=00.0000)

    S_corniche       = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    S_total_corniche = models.FloatField(  default=00.0000)
    L_corniche       = models.FloatField(  default=00.0000)
    V_corniche       = models.FloatField(  default=00.0000)
    P_corniche        = models.FloatField(  default=00.0000)

    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('corniche_detail', kwargs={'slug': self.slug})



def unique_slug_generator_corniche_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(unique_slug_generator_corniche_pre_save_receiver, sender=corniche)
    


class trottoir(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    Pvt                   =  models.FloatField(  default=00.0000,null=True, blank=True,)
    largeur_trottoir      = models.FloatField(  default=00.0000,null=True, blank=True,)
    b_rectangle = models.FloatField(  default=00.0000)
    h_rectangle = models.FloatField(  default=00.0000)

    pente =  models.FloatField(  default=00.0000)
   

    S_trottoir       = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    S_total_trottoir= models.FloatField(  default=00.0000)
    L_trottoir       = models.FloatField(  default=00.0000)
    V_trottoir       = models.FloatField(  default=00.0000)
    P_trottoir        = models.FloatField(  default=00.0000)

    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('trottoir_detail', kwargs={'slug': self.slug})



def unique_slug_generator_trottoir_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(unique_slug_generator_trottoir_pre_save_receiver, sender=trottoir)
    


class glissiere(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    Pvg                   =  models.FloatField(  default=00.0000,null=True, blank=True,)
    L_glissiere            = models.FloatField(  default=00.0000)
    P_glissiere        = models.FloatField(  default=00.0000)

    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('glissiere_detail', kwargs={'slug': self.slug})



def unique_slug_generator_glissiere_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(unique_slug_generator_glissiere_pre_save_receiver, sender=glissiere)



class garde_corps(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    Pvgc                   =  models.FloatField(  default=00.0000,null=True, blank=True,)
    L_garde_corps            = models.FloatField(  default=00.0000)
    P_garde_corps        = models.FloatField(  default=00.0000)

    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('garde_corps_detail', kwargs={'slug': self.slug})



def unique_slug_generator_garde_corps_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(unique_slug_generator_garde_corps_pre_save_receiver, sender=garde_corps)
    


# tablier 


class tablier (models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True)
    
    dalle                     = models.ForeignKey(dalle,on_delete=models.CASCADE,null=True, blank=True)
    poutre                    = models.ForeignKey(poutre,on_delete=models.CASCADE,null=True, blank=True)
    trottoir_droite           = models.ForeignKey(trottoir,on_delete=models.CASCADE,null=True, blank=True,related_name='trottoir_droite')
    trottoir_gauche           = models.ForeignKey(trottoir,on_delete=models.CASCADE,null=True, blank=True,related_name='trottoir_gauche')
    corniche_droite           = models.ForeignKey(corniche,on_delete=models.CASCADE,null=True, blank=True,related_name='corniche_droite')
    corniche_gauche           = models.ForeignKey(corniche,on_delete=models.CASCADE,null=True, blank=True,related_name='corniche_gauche')
    glissiere_droite           = models.ForeignKey(glissiere,on_delete=models.CASCADE,null=True, blank=True,related_name='glissiere_droite')
    glissiere_gauche           = models.ForeignKey(glissiere,on_delete=models.CASCADE,null=True, blank=True,related_name='glissiere_gauche')
    garde_corps_droite         = models.ForeignKey(garde_corps,on_delete=models.CASCADE,null=True, blank=True,related_name='garde_corps_droite')
    garde_corps_gauche         = models.ForeignKey(garde_corps,on_delete=models.CASCADE,null=True, blank=True,related_name='garde_corps_gauche')
    Lr                         = models.FloatField(  default=00.0000,null=True, blank=True)
    Lc                         = models.FloatField(  default=00.0000)
    pvr                        = models.FloatField(  default=00.0000)
    h_revetement               = models.FloatField(  default=00.0000)
    S_revetement               = models.FloatField(  default=00.0000,null=True, blank=True)
    V_revetement               = models.FloatField(  default=00.0000,null=True, blank=True)
    P_revetement               = models.FloatField(  default=00.0000,null=True, blank=True)

    P_tablier       = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    P_tablier_sans_entretoise       = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    P_tablier_sans_entretoise_linear = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    P_total_tablier                  = models.FloatField(  default=00.0000,null=True, blank=True)
    P_total_tablier_sans_entretoise = models.FloatField(  default=00.0000,null=True, blank=True)
    P_total_tablier_sans_entretoise_linear = models.FloatField(  default=00.0000,null=True, blank=True)


    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('tablier_detail', kwargs={'slug': self.slug})



def unique_slug_generator_tablier_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(unique_slug_generator_tablier_pre_save_receiver, sender=tablier)
    


