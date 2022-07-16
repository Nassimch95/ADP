from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cart.models import Cart
from caractéristiquetablier.models import Caractéristique_tablier
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator


class repartition_longitudinal(models.Model):

    title                  = models.CharField(max_length=120)
    slug                   = models.SlugField(blank=True, null=True)
    cart                   = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    caracteristiques       = models.ForeignKey(Caractéristique_tablier,on_delete=models.CASCADE,null=True, blank=True,)
    G = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    A_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    qtr_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    Mc120_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    D240_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    P3_Critique = JSONField(blank=True, null=True,)
    P4_Critique = JSONField(blank=True, null=True,)
    P1_BT       = JSONField(blank=True, null=True,)

    xcritique                 = models.FloatField(blank=True, null=True,)

    

    Br_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    Bt_TOTAL  =ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

   

    

    detail_M_Bc_Total_sense_1 = JSONField(blank=True, null=True,)
    detail_M_Bc_Total_sense_2 = JSONField(blank=True, null=True,)
    T_Bc_detail = JSONField(blank=True, null=True,)

    M_Bc_Total_les_2_sense = ArrayField(models.FloatField(max_length=10, blank=True,null=True,),blank=True, null=True,)

    Bc_TOTAL = ArrayField(
            ArrayField(
                models.FloatField(max_length=10, blank=True),
                blank=True, null=True,
            ),
            blank=True, null=True,
        )

    

    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('repartition_longitudinal_detail', kwargs={'slug': self.slug})

    
def unique_slug_generator_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(unique_slug_generator_pre_save_receiver, sender=repartition_longitudinal)


