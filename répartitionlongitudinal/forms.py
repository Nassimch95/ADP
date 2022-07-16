from django.forms import ModelForm
from.models import repartition_longitudinal







class Add_repartition_longitudinal_form(ModelForm):
    class Meta:
        model = repartition_longitudinal
        fields = ['title','caracteristiques']