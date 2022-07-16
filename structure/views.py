from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import Add_dalle_form, Add_poutre_form,Add_corniche_form,Add_trottoir_form,Add_glissiere_form,Add_garde_corps_form,Add_tablier_form
from .models import poutre, dalle, corniche,trottoir,glissiere,garde_corps,tablier

import numpy as np
import pandas as pd


#dalle 

def add_dalle(request):
   
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_dalle_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            pvd= form.cleaned_data['pvd']
            b_dalle= form.cleaned_data['b_dalle']
            h_dalle= form.cleaned_data['h_dalle']
            L_dalle= form.cleaned_data['L_dalle']
            
           

            S_dalle = b_dalle*h_dalle
            V_dalle = S_dalle*L_dalle
            P_dalle = V_dalle*pvd

            form.instance.S_dalle=S_dalle
            form.instance.V_dalle=V_dalle
            form.instance.P_dalle=P_dalle
            
            
            


            form.save()
            return redirect(reverse("dalle_detail", kwargs={
                'slug': form.instance.slug
                 }))
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_dalle_form()
        info =' la largeur de la dale  = entre-axe poutre de rive  + d1 +d2, d = distance entreaxe et et extremité de la dalle :0.56 et 0.57 pour notre pont =9+0.56+0.57=10.13m  '

    return render(request, 'structures/add_dalle.html', {'form': form,'info':info})

def dalle_detail(request,slug):

    dalle_detail = get_object_or_404(dalle,slug=slug)
    
    

    context = {
        'dalle_detail':dalle_detail,
        
    }

    return render(request,'structures/dalle_detail.html',context)

def dalle_home(request):
    dalles = dalle.objects.all()
    context = {
        'dalles':dalles
    }

    return render(request,'structures/dalles_home.html',context)



# poutres



def poutre_home(request):
    poutres = poutre.objects.all()
    context = {
        'poutres':poutres
    }

    return render(request,'structures/poutres_home.html',context)


def poutre_detail(request,slug):

    poutre_detail = get_object_or_404(poutre,slug=slug)
    data = {
        "S": poutre_detail.S,
        "L": poutre_detail.L,
        "V": poutre_detail.V,  
        }

    index = ['Section dabout', 'changement de section 1', 'section intermediare', 'changement de section 2', 'section mediane']
    pd.options.display.float_format = '{:.4f}'.format
    #load data into a DataFrame object:
    

    df = pd.DataFrame(data) 
    df.index = index
    html = df.to_html()

    

    context = {
        'poutre_detail':poutre_detail,
        'html'         :html,
    }

    return render(request,'structures/poutres_detail.html',context)




def add_poutre(request):
   
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_poutre_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            sa= form.cleaned_data['sa']
            si= form.cleaned_data['si']
            sm= form.cleaned_data['sm']
            pvp= form.cleaned_data['pvp']
            L_poutre= form.cleaned_data['L_poutre']
            npoutres= form.cleaned_data['np']
            ep= form.cleaned_data['ep']

            pve= form.cleaned_data['pve']
            epaisseur_e= form.cleaned_data['epaisseur_e']
            d_chevetre= form.cleaned_data['d_chevetre']

            L_SA = form.cleaned_data['l_sa']
            L_SI = form.cleaned_data['l_si']
            L_SM = form.cleaned_data['l_sm']

            L_CS_1 = form.cleaned_data['l_cs_1']
            L_CS_2 = form.cleaned_data['l_cs_2']
            
            

            SA= (sa.content_object.B_TOTAL_BRUTE_SANS_HOURDIS)*0.0001
            SI= (si.content_object.B_TOTAL_BRUTE_SANS_HOURDIS)*0.0001
            SM= (sm.content_object.B_TOTAL_BRUTE_SANS_HOURDIS)*0.0001

            CS_1 =( SA+SI)/2
            CS_2 =( SI+SM)/2
            
            
            S=np.array([SA,CS_1,SI,CS_2,SM])
            L=np.array([L_SA,L_CS_1,L_SI,L_CS_2,L_SM])
            V =np.array([])
            for x in range(0,5):
                v = S[x]*L[x]
                V = np.append(V,v)

            

            L_total_sections = (np.sum(L))*2
            VP = np.sum(V)*2
            Pp =VP*pvp
            Ptp = npoutres*Pp

           

            
            form.instance.L_poutre = L_poutre
            form.instance.L_total_sections=L_total_sections
            form.instance.np = npoutres
            form.instance.ep = ep
            form.instance.pvp = pvp
            form.instance.epdr = ep*(npoutres-1)

            

            form.instance.cs_1 = CS_1
            form.instance.cs_2 = CS_2
            form.instance.l_cs_1 = L_CS_1
            form.instance.l_cs_2 = L_CS_2
           
            form.instance.l_sa = L_SA
            form.instance.l_si = L_SI
            form.instance.l_sm = L_SM

            form.instance.S = S.tolist()
            form.instance.L = L.tolist()
            form.instance.V = V.tolist() 
            form.instance.vtp = VP




            form.instance.pp = Pp
            form.instance.ptp = Ptp

            # entretoise 
            b_jonction = (sa.content_object.b_jonction)*0.01
            h_jonction = (sa.content_object.h_jonction)*0.01
            b_table_de_compression =( sa.content_object.b_table_de_compression)*0.01
            h_table_de_compression = (sa.content_object.h_table_de_compression)*0.01
            b_ame = (sa.content_object.b_ame)*0.01
            h_ame = (sa.content_object.h_ame)*0.01
            h_section = (sa.content_object.h_section)*0.01


            B1 = b_jonction*h_jonction
            B2 = (ep-b_table_de_compression)*(h_table_de_compression+h_jonction)
            B3 = (ep-b_ame)*(h_section-h_table_de_compression-h_jonction-d_chevetre)

            B = np.array([B1,B2,B3])
            Bt = np.sum(B)
            Ve =Bt*epaisseur_e *(npoutres-1)

            Pe = Ve*pve
            Pte = Pe*2
            print(Bt,Pe,Pte)

            form.instance.S_e = B.tolist()
            form.instance.S_e_total = Bt
            form.instance.V_e = Ve
            form.instance.P_e = Pe
            form.instance.pt_e = Pte

            #pre dalle :

            b_pre_dalle = ep - (sa.content_object.b_table_de_compression*0.01)+0.04
            h_pre_dalle = 0.04 
            S_pre_dalle = b_pre_dalle*h_pre_dalle
            S_total_pre_dalle = S_pre_dalle *(npoutres-1)
            V_total_pre_dalle = S_total_pre_dalle*(L_poutre)
            P_pre_dalle         =V_total_pre_dalle *pvp

            form.instance.b_pre_dalle = b_pre_dalle
            form.instance.h_pre_dalle= h_pre_dalle
            form.instance.S_pre_dalle = S_pre_dalle
            form.instance.S_total_pre_dalle=S_total_pre_dalle
            form.instance.V_total_pre_dalle=V_total_pre_dalle
            form.instance.P_pre_dalle = P_pre_dalle



            form.save()
            return redirect(reverse("poutre_detail", kwargs={
                'slug': form.instance.slug
                 }))
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_poutre_form()

    return render(request, 'structures/add_poutre.html', {'form': form})



#corniche 

def add_corniche(request):
   
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_corniche_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            Pvc= form.cleaned_data['Pvc']
            b_rectangle= form.cleaned_data['b_rectangle']
            h_rectangle= form.cleaned_data['h_rectangle']
            b_grand_triangle= form.cleaned_data['b_grand_triangle']
            h_grand_triangle= form.cleaned_data['h_grand_triangle']
            b_petit_triangle= form.cleaned_data['b_petit_triangle']
            h_petit_triangle= form.cleaned_data['h_petit_triangle']
            L_corniche= form.cleaned_data['L_corniche']

            B1 = (b_rectangle*h_rectangle)*0.0001
            B2  = ((b_grand_triangle*h_grand_triangle)/2)*0.0001
            B3  = ((b_petit_triangle*h_petit_triangle)/2)*0.0001
            S_corniche   =    np.array([B1,B2,B3])
            S_total_corniche  = np.sum(S_corniche)
            V_corniche        = S_total_corniche*L_corniche
            P_corniche         = V_corniche * Pvc

            print(S_corniche)
            form.instance.S_corniche = S_corniche.tolist()
            form.instance.S_total_corniche = S_total_corniche
            form.instance.V_corniche = V_corniche
            form.instance.P_corniche = P_corniche
            
            form.save()
            return redirect(reverse("corniche_detail", kwargs={
                'slug': form.instance.slug
            }))

            


           

            
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_corniche_form()

    return render(request, 'structures/add_corniche.html', {'form': form})




def corniche_detail(request,slug):

    corniche_detail = get_object_or_404(corniche,slug=slug)

    

    
    #load data into a DataFrame object:
    

    

    context = {
        'corniche_detail':corniche_detail,
    }

    return render(request,'structures/corniche_detail.html',context)



def corniche_home(request):
    corniches = corniche.objects.all()
    context = {
        'corniches':corniches
    }

    return render(request,'structures/corniche_home.html',context)



# trottoir 

def add_trottoir(request):
   
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_trottoir_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            Pvt= form.cleaned_data['Pvt']
            b_rectangle= form.cleaned_data['b_rectangle']
            h_rectangle= form.cleaned_data['h_rectangle']
            pente= form.cleaned_data['pente']
            
            L_trottoir = form.cleaned_data['L_trottoir']


            h_triangle = b_rectangle*pente/100
            B1  = (b_rectangle*h_rectangle)*0.0001
            B2  = ((b_rectangle *h_triangle)/2)*0.0001
            S_trottoir   =    np.array([B1,B2])
            S_total_trottoir  = np.sum(S_trottoir)
            V_trottoir       = S_total_trottoir*L_trottoir
            P_trottoir       = V_trottoir * Pvt

            print(S_trottoir)
            form.instance.S_trottoir = S_trottoir.tolist()
            form.instance.S_total_trottoir = S_total_trottoir
            form.instance.V_trottoir = V_trottoir
            form.instance.P_trottoir = P_trottoir
            
            form.save()
            return redirect(reverse("trottoir_detail", kwargs={
                'slug': form.instance.slug
            }))

            


           

            
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_trottoir_form()
        info  ="largeur du trottoir =de l'exrimité de la corniche jusqu'adebut chaussé = 150cm pour tr droite et 75 cm tr gauche (pour ce pont),b_rectangle =largeur_tr - largeur corniche_corncihe,b_rectangle_droite =150-24=126,b_rectangle_gauche =75-0 (pas de corniche)"

    return render(request, 'structures/add_trottoir.html', {'form': form,'info':info})




def trottoir_detail(request,slug):

    trottoir_detail = get_object_or_404(trottoir,slug=slug)

    

    
    #load data into a DataFrame object:
    

    

    context = {
        'trottoir_detail':trottoir_detail,
    }

    return render(request,'structures/trottoir_detail.html',context)



def trottoir_home(request):
    trottoirs = trottoir.objects.all()
    context = {
        'trottoirs':trottoirs,
    }

    return render(request,'structures/trottoir_home.html',context)

#  glissiere 



def add_glissiere(request):

        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_glissiere_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            Pvg= form.cleaned_data['Pvg']
            L_glissiere = form.cleaned_data['L_glissiere']


           
            
            P_glissiere      = L_glissiere * Pvg

            
            
            form.instance.P_glissiere = P_glissiere
            
            form.save()
            return redirect(reverse("glissiere_detail", kwargs={
                'slug': form.instance.slug
            }))

            


           

            
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_glissiere_form()

    return render(request, 'structures/add_glissiere.html', {'form': form})



def glissiere_home(request):
    glissieres = glissiere.objects.all()
    context = {
        'glissieres':glissieres,
    }

    return render(request,'structures/glissiere_home.html',context)


def glissiere_detail(request,slug):

    glissiere_detail = get_object_or_404(glissiere,slug=slug)

    

    
    #load data into a DataFrame object:
    

    

    context = {
        'glissiere_detail':glissiere_detail,
    }

    return render(request,'structures/glissiere_detail.html',context)



#garde corps :

def add_garde_corps(request):

        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_garde_corps_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            Pvgc= form.cleaned_data['Pvgc']
            L_garde_corps = form.cleaned_data['L_garde_corps']


           
            
            P_garde_corps     = L_garde_corps * Pvgc

            
            
            form.instance.P_garde_corps = P_garde_corps
            
            form.save()
            return redirect(reverse("garde_corps_detail", kwargs={
                'slug': form.instance.slug
            }))

            


           

            
            

            
            
           
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_garde_corps_form()

    return render(request, 'structures/add_garde_corps.html', {'form': form})


def garde_corps_home(request):
    gardes_corps = garde_corps.objects.all()
    context = {
        'gardes_corps':gardes_corps,
    }

    return render(request,'structures/garde_corps_home.html',context)


def garde_corps_detail(request,slug):

    garde_corps_detail = get_object_or_404(garde_corps,slug=slug)

    

    
    #load data into a DataFrame object:
    

    

    context = {
        'garde_corps_detail':garde_corps_detail,
    }

    return render(request,'structures/garde_corps_detail.html',context)


#tablier

def add_tablier(request):

        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_tablier_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']

            dalle = form.cleaned_data['dalle']
            poutre = form.cleaned_data['poutre']
            trottoir_droite = form.cleaned_data['trottoir_droite']
            trottoir_gauche = form.cleaned_data['trottoir_gauche']
            corniche_droite = form.cleaned_data['corniche_droite']
            corniche_gauche = form.cleaned_data['corniche_gauche']
            glissiere_droite = form.cleaned_data['glissiere_droite']
            glissiere_gauche = form.cleaned_data['glissiere_gauche']
            garde_corps_droite = form.cleaned_data['garde_corps_droite']
            garde_corps_gauche = form.cleaned_data['garde_corps_gauche']
            Lr = form.cleaned_data['Lr']
            Lc = form.cleaned_data['Lc']
            pvr = form.cleaned_data['pvr']
            h_revetement = form.cleaned_data['h_revetement']

            P_dalle = dalle.P_dalle
            P_poutre = poutre.ptp
            P_entretoise = poutre.pt_e
            P_pre_dalle  = poutre.P_pre_dalle 
            
            #revetement 
            S_revetement = Lr*(h_revetement*0.01)
            V_revetement = S_revetement* poutre.L_poutre
            P_revetement = V_revetement *pvr


            if trottoir_droite:
                P_trottoir_droite = trottoir_droite.P_trottoir
            else:
                P_trottoir_droite = 0



            if trottoir_gauche:
                P_trottoir_gauche = trottoir_gauche.P_trottoir
            else :
                P_trottoir_gauche =0
            


            if glissiere_droite:
                    P_glissiere_droite = glissiere_droite.P_glissiere
            else :
                P_glissiere_droite = 0


            if glissiere_gauche:

                P_glissiere_gauche = glissiere_gauche.P_glissiere
            else:
                P_glissiere_gauche =  0

            
            if corniche_droite:
                P_corniche_droite = corniche_droite.P_corniche   
            else :
                P_corniche_droite = 0


            if corniche_gauche:
                P_corniche_gauche = corniche_gauche.P_corniche
            else :
                P_corniche_gauche = 0

            
            if garde_corps_droite:
                P_garde_corps_droite = garde_corps_droite.P_garde_corps
            else :
                P_garde_corps_droite = 0


            if garde_corps_gauche:
                P_garde_corps_gauche = garde_corps_gauche.P_garde_corps
            else :
                P_garde_corps_gauche = 0

                
            P_tablier = np.array([P_dalle,P_poutre,P_entretoise,P_pre_dalle ,P_revetement ,P_trottoir_droite,P_trottoir_gauche,P_glissiere_droite,P_glissiere_gauche,P_corniche_droite,P_corniche_gauche,P_garde_corps_droite,P_garde_corps_gauche])
            P_total_tablier = np.sum(P_tablier)
            P_tablier_sans_entretoise = np.array([P_dalle,P_poutre,0,P_pre_dalle ,P_revetement,P_trottoir_droite,P_trottoir_gauche,P_glissiere_droite,P_glissiere_gauche,P_corniche_droite,P_corniche_gauche,P_garde_corps_droite,P_garde_corps_gauche])
            P_total_tablier_sans_entretoise = np.sum(P_tablier_sans_entretoise)
            P_tablier_sans_entretoise_linear = P_tablier_sans_entretoise/poutre.L_poutre
            P_total_tablier_sans_entretoise_linear = np.sum(P_tablier_sans_entretoise_linear)


            form.instance.S_revetement = S_revetement
            form.instance.V_revetement = V_revetement
            form.instance.P_revetement = P_revetement

            form.instance.P_tablier = P_tablier.tolist()
            form.instance.P_tablier_sans_entretoise = P_tablier_sans_entretoise.tolist()
            form.instance.P_tablier_sans_entretoise_linear = P_tablier_sans_entretoise_linear.tolist()

            form.instance.P_total_tablier = P_total_tablier
            form.instance.P_total_tablier_sans_entretoise = P_total_tablier_sans_entretoise
            form.instance.P_total_tablier_sans_entretoise_linear = P_total_tablier_sans_entretoise_linear


            form.save()
            return redirect(reverse("tablier_detail", kwargs={
                'slug': form.instance.slug
            }))
            
            
           
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_tablier_form()

    return render(request, 'structures/add_tablier.html', {'form': form})



def tablier_detail(request,slug):

    tablier_detail = get_object_or_404(tablier,slug=slug)
    
    data = {
        "G (t) ": tablier_detail.P_tablier,
        "g (t/ml)": tablier_detail.P_tablier_sans_entretoise_linear,
        }

    index = ['dalle', 'poutre', 'entretoise', 'predalle', 'revetement','trottoir droit','trottoir gauche','glissiere droite','glissiere gauche','corniche droite','corniche gauche','garde corps droite','garde corps gauche']

    #load data into a DataFrame object:
    

    df = pd.DataFrame(data) 
    df.index = index
    html = df.to_html()

    

    
    #load data into a DataFrame object:
    

    

    context = {
        'tablier_detail':tablier_detail,
        'html'          : html,
    }

    return render(request,'structures/tablier_detail.html',context)


def tablier_home(request):
    tabliers = tablier.objects.all()
    context = {
        'tabliers':tabliers,
    }

    return render(request,'structures/tablier_home.html',context)
