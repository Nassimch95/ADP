from django.forms import ModelForm
from.models import platelage




class Add_platelage_form(ModelForm):
    class Meta:
        model = platelage
        fields = ['title','R_transversale']