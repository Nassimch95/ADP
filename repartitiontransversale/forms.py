from django.forms import ModelForm
from.models import repartition_transversale







class Add_repartition_transversale_form(ModelForm):
    class Meta:
        model = repartition_transversale
        fields = ['title','R_longitudinal']