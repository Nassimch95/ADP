from django.db import models
from répartitionlongitudinal.models import repartition_longitudinal
from cart.models import Cart
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator

# Create your models here.


class repartition_transversale(models.Model):

    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, null=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    R_longitudinal       = models.ForeignKey(repartition_longitudinal,on_delete=models.CASCADE,null=True, blank=True,)
    Ia                   =  models.FloatField(blank=True,null=True)
    Im                   =  models.FloatField(blank=True,null=True)
    Ip                  =  models.FloatField(blank=True,null=True)
    Ie                  =  models.FloatField(blank=True,null=True)
    r                   =  models.FloatField(blank=True,null=True)
    ro_p                =  models.FloatField(blank=True,null=True)
    ro_e                =  models.FloatField(blank=True,null=True)       
    teta                 =  models.FloatField(blank=True,null=True)
    a_SF = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    b_SF = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    Cp = models.FloatField(blank=True,null=True)
    Ce = models.FloatField(blank=True,null=True)
    alpha =  models.FloatField(blank=True,null=True)
    P_reel = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    P_active = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    k0 = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    k1 = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    ka = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    ka_active = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    
    K_ALPHA_FUNCTION = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    K_G  = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    ka_max_mc_120 = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_D240 = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Qtr_UNE_VOIE = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Qtr_DEUX_VOIE = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_A_UNE_VOIE = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_A_DEUX_VOIE = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Bc_1v = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Bc_2v = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Bt_1v = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Bt_2v = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    K_Br  = ArrayField(
                models.FloatField(blank=True,null=True),
                blank=True, null=True,
            )
    
    #POUTRE  :

    poutre_1 =  JSONField(blank=True, null=True,)
    poutre_2 =  JSONField(blank=True, null=True,)
    poutre_3 =  JSONField(blank=True, null=True,)
    
    #combinaison :

    combi_ELU_AB_p1 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELU_Mc120_D240_p1 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_AB_p1 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_Mc120_D240_p1 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    combi_ELU_AB_p2 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELU_Mc120_D240_p2 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_AB_p2 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_Mc120_D240_p2 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    combi_ELU_AB_p3 =   ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELU_Mc120_D240_p3 =   ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_AB_p3 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
    combi_ELS_Mc120_D240_p3 =  ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )
 
    


    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('repartition_transversale_detail', kwargs={'slug': self.slug})

    
def unique_slug_generator_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_pre_save_receiver, sender=repartition_transversale)