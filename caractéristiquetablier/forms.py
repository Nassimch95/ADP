from django.forms import ModelForm
from.models import Caractéristique_tablier








class AddDtCaractéristiqueTablier(ModelForm):
    class Meta:
        model = Caractéristique_tablier
        fields = ['title','tab']