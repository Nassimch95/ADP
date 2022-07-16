from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cart.models import Cart
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
# Create your models here.







class section_type_01(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
   
    b_hourdis              = models.FloatField(  default=00.0000)
    h_hourdis              = models.FloatField(  default=00.0000)
    h_section              = models.FloatField(  default=00.0000)
    b_table_de_compression = models.FloatField(  default=00.0000)
    h_table_de_compression = models.FloatField(  default=00.0000)
    b_jonction = models.FloatField(  default=00.0000)
    h_jonction = models.FloatField(  default=00.0000)
    b_gousset_superieur   = models.FloatField(  default=00.0000)
    h_gousset_superieur   = models.FloatField(  default=00.0000)
    b_ame  = models.FloatField(  default=00.0000)
    h_ame  = models.FloatField(  default=00.0000)
    b_gousset_inferieur   = models.FloatField(  default=00.0000)
    h_gousset_inferieur   = models.FloatField(  default=00.0000)
    b_talon  = models.FloatField(  default=00.0000)
    h_talon   = models.FloatField(  default=00.0000)

    # sections

    B_hourdis     = models.FloatField( default=00.0000) 
    B             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    B_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)

    # Hauteur des CDG

    Z             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    Z_hourdis     = models.FloatField(  default=00.0000)

    # S/Δ= B*Z

    
    S_TO_DELTA   = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)

    S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)

    S_TO_DELTA_hourdis     = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)


    # I0

    
    I             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    I_hourdis     = models.FloatField(  default=00.0000)

    
    


    #  I/Δ=I0+BxZ²

   
    I_TO_DELTA   = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)

    
    

    I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)

    I_TO_DELTA_hourdis     = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)


    V_prime_sans_hourdis                = models.FloatField(  default=00.0000,null=True, blank=True)
    V_sans_hourdis                      = models.FloatField(  default=00.0000,null=True, blank=True) 
    IG_sans_hourdis                     = models.FloatField(  default=00.0000,null=True, blank=True)
    rendement_sans_hourdis              = models.FloatField(  default=00.0000,null=True, blank=True)

    V_prime_avec_hourdis                = models.FloatField(  default=00.0000,null=True, blank=True)
    V_avec_hourdis                      = models.FloatField(  default=00.0000,null=True, blank=True) 
    IG_avec_hourdis                    = models.FloatField(  default=00.0000,null=True, blank=True)
    rendement_avec_hourdis              = models.FloatField(  default=00.0000,null=True, blank=True)

    def __str__(self):
        
        return str(self.title)

    

    def csv_export_url(self):
        return reverse('geometry_csv_export', kwargs={'id': self.id})

    


      


def unique_slug_generator_section_type_01_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_section_type_01_pre_save_receiver, sender=section_type_01)



class section_type_02(models.Model):
    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    
    b_hourdis              = models.FloatField(  default=00.0000)
    h_hourdis              = models.FloatField(  default=00.0000)
    h_section              = models.FloatField(  default=00.0000)
    b_table_de_compression = models.FloatField(  default=00.0000)
    h_table_de_compression = models.FloatField(  default=00.0000)
    b_jonction = models.FloatField(  default=00.0000)
    h_jonction = models.FloatField(  default=00.0000)
   
    b_ame  = models.FloatField(  default=00.0000)
    h_ame  = models.FloatField(  default=00.0000)
    
    # sections

    B_hourdis     = models.FloatField( default=00.0000) 
    B             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    B_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    B_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)

    # Hauteur des CDG

    Z             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    Z_hourdis     = models.FloatField(  default=00.0000)

    # S/Δ= B*Z

    
    S_TO_DELTA   = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)

    S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)

    S_TO_DELTA_hourdis     = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)


    # I0

    
    I             = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)
    I_hourdis     = models.FloatField(  default=00.0000)

    
    


    #  I/Δ=I0+BxZ²

   
    I_TO_DELTA   = ArrayField(models.FloatField(default=00.0000 ) ,null=True, blank=True)

    
    

    I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = models.FloatField(  default=00.0000)

    I_TO_DELTA_hourdis     = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)
    I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = models.FloatField(  default=00.0000)


    V_prime_sans_hourdis                = models.FloatField(  default=00.0000,null=True, blank=True)
    V_sans_hourdis                      = models.FloatField(  default=00.0000,null=True, blank=True) 
    IG_sans_hourdis                     = models.FloatField(  default=00.0000,null=True, blank=True)
    rendement_sans_hourdis              = models.FloatField(  default=00.0000,null=True, blank=True)

    V_prime_avec_hourdis                = models.FloatField(  default=00.0000,null=True, blank=True)
    V_avec_hourdis                      = models.FloatField(  default=00.0000,null=True, blank=True) 
    IG_avec_hourdis                    = models.FloatField(  default=00.0000,null=True, blank=True)
    rendement_avec_hourdis              = models.FloatField(  default=00.0000,null=True, blank=True)

    def __str__(self):
        
        return str(self.slug)

    

    def csv_export_url(self):
        return reverse('geometry_csv_export', kwargs={'id': self.id})



def unique_slug_generator_section_type_02_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_section_type_02_pre_save_receiver, sender=section_type_02)






class SectionAdded(models.Model):
    slug                   = models.SlugField(blank=True, unique=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE) # User, Product, Order, Cart, Address
    object_id           = models.PositiveIntegerField(null=True) # User id, Product id, Order id,
    content_object      = GenericForeignKey('content_type', 'object_id') # Product instance
    timestamp           = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return "%s added on %s" %(self.content_object, self.timestamp)

    def get_absolute_url(self):
        return reverse('GeometryDetail', kwargs={'slug': self.slug})
    

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'section added'
        verbose_name_plural = 'sections addded'


def section_type_2_add_post_save_receiver(sender, instance, created,*args, **kwargs):
    if created:
        SectionAdded.objects.create(content_object=instance,cart=instance.cart,slug=instance.slug)



post_save.connect(section_type_2_add_post_save_receiver, sender=section_type_02)


def section_type_1_add_post_save_receiver(sender, instance, created,*args, **kwargs):
    if created:
        SectionAdded.objects.create(content_object=instance,cart=instance.cart,slug=instance.slug)



post_save.connect(section_type_2_add_post_save_receiver, sender=section_type_01)