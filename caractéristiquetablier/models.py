from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from cart.models import Cart
from structure.models import tablier


class Caractéristique_tablier(models.Model):

    title         = models.CharField(max_length=120)
    slug          = models.SlugField(blank=True, unique=True)
    cart          = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True, blank=True,)
    tab           = models.ForeignKey(tablier,on_delete=models.CASCADE,null=True, blank=True,)
    L             = models.FloatField(  default=00.0000)
    Lr            = models.FloatField(  default=00.0000)
    Lc            = models.FloatField(  default=00.0000)
    epdr          = models.FloatField(  default=00.0000)
    G             = models.FloatField(  default=00.0000)
    ptp           = models.FloatField(  default=00.0000)
    pte           = models.FloatField(  default=00.0000)

    nv             = models.FloatField(  default=00.0000) # nombre de voies
    lv             = models.FloatField(  default=00.0000) # largeur de la voie
    lv0            = models.FloatField(  default=00.0000) # depend de la classe 
    classe         = models.FloatField(  default=00.0000) # largeur roulable
    Lprime         = models.FloatField(  default=00.0000) # longeur chargé dans la dalle
    Gprime         = models.FloatField(  default=00.0000)

    a1             = models.FloatField(  default=00.0000) # coefficient systeme d charge A
    a2             = models.FloatField(  default=00.0000) # coefficient systeme d charge A
    A              = models.FloatField(  default=00.0000) # coefficient systeme d charge A
    Al             = models.FloatField(  default=00.0000) # coefficient systeme d charge A
    QA             = models.FloatField(  default=00.0000)
 
    cbc            = models.FloatField(  default=00.0000)
    cbt            = models.FloatField(  default=00.0000)
    nBt            = models.FloatField(  default=00.0000)
    nBc            = models.FloatField(  default=00.0000)
    Bc             = models.FloatField(  default=00.0000)
    Bt             = models.FloatField(  default=00.0000)
    Br             = models.FloatField(  default=00.0000)
    QB             = models.FloatField(  default=00.0000)
    qmc120_sur_L   = models.FloatField(  default=00.0000)
    qmc80_sur_L    = models.FloatField(  default=00.0000)
    Qm_sur_L       = models.FloatField(  default=00.0000)
    cdmdB          = models.FloatField(  default=00.0000)
    cdmdM          = models.FloatField(  default=00.0000)
    nBt_sur_L_prime = models.FloatField(  default=00.0000)
    nBc_sur_L_prime = models.FloatField(  default=00.0000)
    Bc_sur_L_prime  = models.FloatField(  default=00.0000)
    Bt_sur_L_prime  = models.FloatField(  default=00.0000)
    Br_sur_L_prime  = models.FloatField(  default=00.0000)
    QB_sur_L_prime  = models.FloatField(  default=00.0000)
    qmc120_sur_L_prime = models.FloatField(  default=00.0000)
    qmc80_sur_L_prime  = models.FloatField(  default=00.0000)
    Qm_sur_L_prime     = models.FloatField(  default=00.0000)
    cdmdBprime         = models.FloatField(  default=00.0000)
    cdmdMprime         = models.FloatField(  default=00.0000)
    
    def __str__(self):
        
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('caracteristique-detail', kwargs={'slug': self.slug})
    




def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(pre_save_receiver, sender=Caractéristique_tablier)
    




