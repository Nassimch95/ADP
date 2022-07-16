from django.forms import ModelForm
from.models import section_type_01
from.models import section_type_02








class Add_section_type_01_form(ModelForm):
    class Meta:
        model = section_type_01
        fields = ['title', 'b_hourdis', 'h_hourdis', 'h_section', 'b_table_de_compression', 'h_table_de_compression','b_jonction', 'h_jonction', 'b_gousset_superieur', 'h_gousset_superieur', 'b_ame', 'h_ame', 'b_gousset_inferieur', 'h_gousset_inferieur', 'b_talon', 'h_talon']




class Add_section_type_02_form(ModelForm):
     class Meta:
        model = section_type_02
        fields = ['title', 'b_hourdis', 'h_hourdis', 'h_section', 'b_table_de_compression', 'h_table_de_compression','b_jonction','h_jonction', 'b_ame', 'h_ame', ]



