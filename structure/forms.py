from django.forms import ModelForm
from.models import dalle, poutre,corniche,trottoir,glissiere,garde_corps,tablier




class Add_dalle_form(ModelForm):
    class Meta:
        model = dalle
        fields = ['title', 'pvd','b_dalle' ,'h_dalle', 'L_dalle']




class Add_poutre_form(ModelForm):
    class Meta:
        model = poutre
        fields = ['title', 'pvp','L_poutre' ,'sa', 'l_sa',  'l_cs_1','si', 'l_si',  'l_cs_2', 'sm', 'l_sm', 'np', 'ep', 'pve','epaisseur_e','d_chevetre']



class Add_corniche_form(ModelForm):
    class Meta:
        model = corniche
        fields = ['title', 'Pvc','b_rectangle','h_rectangle', 'b_grand_triangle','h_grand_triangle','b_petit_triangle','h_petit_triangle','L_corniche' ]



class Add_trottoir_form(ModelForm):
    class Meta:
        model = trottoir
        fields = ['title', 'Pvt','largeur_trottoir','b_rectangle','h_rectangle', 'pente','L_trottoir']



class Add_glissiere_form(ModelForm):
    class Meta:
        model = glissiere
        fields = ['title', 'Pvg','L_glissiere']



class Add_garde_corps_form(ModelForm):
    class Meta:
        model = garde_corps
        fields = ['title', 'Pvgc','L_garde_corps']



class Add_tablier_form(ModelForm):
    class Meta:
        model = tablier
        fields = ['title', 'dalle','poutre','trottoir_droite','trottoir_gauche','corniche_droite','corniche_gauche','glissiere_droite','glissiere_gauche','garde_corps_droite','garde_corps_gauche','Lr','Lc','pvr','h_revetement']


