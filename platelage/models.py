from django.db import models
from repartitiontransversale.models import repartition_transversale
from cart.models import Cart
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator


class platelage(models.Model):

    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, null=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    R_transversale       = models.ForeignKey(repartition_transversale,on_delete=models.CASCADE,null=True, blank=True,)
   
  
   
            
    u0 = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    u1 = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    ua = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    u0_3teta = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    u1_3teta = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    ua_3teta = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    matrice_teta_p =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    matrice_teta_n =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    matrice_3teta_p =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    matrice_3teta_n =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    pm =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    M_P =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    M_N =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    combinaison_arr_P =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    combinaison_arr_N =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    M_Max_P = ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            )
    
    M_Max_N = ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            )

    #flexion localise :
    a_lx =  models.FloatField(max_length=12, blank=True,null=True)
    y_lx =  models.FloatField(max_length=12, blank=True,null=True)
    Lx   =  models.FloatField(max_length=12, blank=True,null=True)
    Ly   =  models.FloatField(max_length=12, blank=True,null=True)
    ro   =  models.FloatField(max_length=12, blank=True,null=True)

    G_ET_A_LOCALISE_arr =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    B_Mc120_LOCALISE_arr =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    ELU_LOCALISE_M =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    ELS_LOCALISE_M = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    Max_ELU_ELS_LOCALISE_arr = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
            
        
    




    


    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('platelage_detail', kwargs={'slug': self.slug})

    
def unique_slug_generator_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_pre_save_receiver, sender=platelage)