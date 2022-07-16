from django.shortcuts import render,redirect,reverse,get_object_or_404
from .forms import AddDtCaractéristiqueTablier
from .tableau import coef_a1,lv0_array,coef_bc,coef_bt
from .models import Caractéristique_tablier
from cart.models import Cart
import math
import numpy as np


# Create your views here.

def Ct_view(request):
    
    cart_obj = Cart.objects.new_or_get(request)
    CTList = Caractéristique_tablier.objects.all()
    context ={
        'CTList' :CTList,
    }

   

    return render (request,'caractéristique-tablier/Home-caractéristique-tabliers.html', context)


def Caracteristique_tablier_detail(request,slug):
    caracteristique_tablier_detail = get_object_or_404(Caractéristique_tablier, slug=slug)
    context ={
    'slug' :slug,
    'caracteristique_tablier_detail':caracteristique_tablier_detail
    
    }

    

   

    return render (request,'caractéristique-tablier/Detail-caractéristique-tablier.html',context)



def get_classe(Lr):
    if Lr >= 7 :
        classe = 1 
    else:
        if Lr > 5.5 and Lr < 7:
            classe = 2
        else:
            classe = 3 
    return classe


def get_QB(L,nv,classe):
    P1P6 = [3, 6, 6, 3, 6, 6]
    D1D6 = [0, 4.5, 6, 10.5, 15, 16.5]
    P6P1 = [6, 6, 3, 6, 6, 3]
    D6D1 = [0, 1.5, 6, 10.5, 12, 16.5]
    cbc = coef_bc[classe,nv]
    cbt = coef_bt[classe]
   

    if nv >2:
        nBt = 2
    else:
        nBt = nv

    
    
    nBc =nv

    if L >= 16.5:
        Bc = 30
        Bt = 16
        Br = 10

        QB= max(cbc*Bc*2*nBc,cbt*Bt*2*nBt,Br)
    
    else:
        Bt = 16
        Br = 10
        P1P6_sur_L =[]
        P6P1_sur_L =[]

        for x in range(6):
            if D1D6[x] <= L:
                P1P6_sur_L = np.append(P1P6_sur_L,P1P6[x])

        for y in range(6):
            if D6D1[y] <= L:
                P6P1_sur_L = np.append(P6P1_sur_L,P6P1[y])
        
    
        P1P6_sur_L_total = np.sum(P1P6_sur_L)
        P6P1_sur_L_total = np.sum(P6P1_sur_L)
        Bc  = max(P1P6_sur_L_total,P6P1_sur_L_total)
        QB= max(cbc*Bc*2*nBc,cbt*Bt*2*nBt,Br)
        
    return cbc,cbt,nBt,nBc,Bc,Bt,Br,QB
        

        




    




        


        


    pass

def get_qmc120(L):
    if L <= 6.1 :
        qmc120 = 18.033*L
    else:
        if L >6.1 and L <=36.6:
            qmc120= 110
        else:
            if L>36.6 and L<=42.7 :
                qmc120 = 110 +(18.033 * (L-36.6))
            else:
                if L> 42.7 :
                    qmc120 =220
    
    return qmc120
                
def get_qmc80(L):
    if L <= 4.9 :
        qmc80 = 14.69*L
    else:
        if L >4.9 and L <=35.4:
            qmc80= 72
        else:
            if L>35.4 and L<=40.3 :
                qmc80 = 72 +(14.69 * (L-35.4))
            else:
                if L> 40.3 :
                    qmc80 =144
    
    return qmc80
                

def Ct_add(request):
    cart_obj = Cart.objects.new_or_get(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddDtCaractéristiqueTablier(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            L     = form.cleaned_data['tab'].poutre.L_poutre
            Lr    = form.cleaned_data['tab'].Lr
            Lc    = form.cleaned_data['tab'].Lc
            epdr  =  form.cleaned_data['tab'].poutre.epdr
            G     = form.cleaned_data['tab'].P_total_tablier
            ptp  =  form.cleaned_data['tab'].poutre.ptp
            pte  =  form.cleaned_data['tab'].poutre.pt_e
            
            
            classe = get_classe(Lr)

            nv = math.floor(Lc/3)

            lv = Lc/nv
            
            lv0 = lv0_array[classe]

            Lprime = min(max(Lr,epdr),L)

            Gprime =(G-(ptp+pte))*(Lprime/L)

            #A
            a1 = coef_a1[classe,nv]

            a2 = round(lv0/lv,3)

            Al = round(( 230 + (36000/(L+12)) )*0.001,3)

            A = a1*a2*Al

            QA = round(A*lv,3)
            
            # B poutre 

            cbc,cbt,nBt,nBc,Bc,Bt,Br,QB = get_QB(L,nv,classe)
            qmc120_sur_L =get_qmc120(L)
            qmc80_sur_L =get_qmc80(L)
            Qm_sur_L = max(qmc120_sur_L,qmc80_sur_L)
            cdmdB  = round(1 + (0.4/(1+0.2*L)) + (0.6/(1+(4*G/QB))),4)
            cdmdM  = round(1 + (0.4/(1+0.2*L)) + (0.6/(1+(4*G/Qm_sur_L))),4)
            
            #B dalle
            cbc_sur_L_prime,cbt_sur_L_prime,nBt_sur_L_prime,nBc_sur_L_prime,Bc_sur_L_prime,Bt_sur_L_prime,Br_sur_L_prime,QB_sur_L_prime = get_QB(Lprime,nv,classe)
            qmc120_sur_L_prime =get_qmc120(Lprime)
            qmc80_sur_L_prime =get_qmc80(Lprime)
            Qm_sur_L_prime = max(qmc120_sur_L_prime,qmc80_sur_L_prime)
            cdmdBprime  = round(1 + (0.4/(1+0.2*L)) + (0.6/(1+(4*Gprime/QB_sur_L_prime))),4)
            cdmdMprime  = round(1 + (0.4/(1+0.2*L)) + (0.6/(1+(4*Gprime/Qm_sur_L_prime))),4)
            

            form.instance.L = L
            form.instance.Lr = Lr
            form.instance.Lc = Lc
            form.instance.epdr = epdr
            form.instance.G = G
            form.instance.ptp = ptp 
            form.instance.pte = pte

            form.instance.classe = classe
            form.instance.nv = nv
            form.instance.lv = lv
            form.instance.lv0 = lv0
            form.instance.Lprime = Lprime
            form.instance.Gprime = Gprime
            form.instance.a1 = a1
            form.instance.a2 = a1
            form.instance.Al = Al
            form.instance.A = A
            form.instance.QA = QA


            form.instance.cbc = cbc
            form.instance.cbt = cbt
            form.instance.nBc = nBc
            form.instance.nBt = nBt
            form.instance.Bc= Bc
            form.instance.Bt = Bt
            form.instance.Br = Br
            form.instance.QB = QB
            form.instance.qmc120_sur_L = qmc120_sur_L
            form.instance.qmc80_sur_L= qmc80_sur_L
            form.instance.Qm_sur_L = Qm_sur_L
            form.instance.cdmdB = cdmdB
            form.instance.cdmdM = cdmdM


            form.instance.Bc_sur_L_prime= Bc_sur_L_prime
            form.instance.Bt_sur_L_prime = Bt_sur_L_prime
            form.instance.Br_sur_L_prime = Br_sur_L_prime
            form.instance.QB_sur_L_prime = QB_sur_L_prime
            form.instance.qmc120_sur_L_prime = qmc120_sur_L_prime
            form.instance.qmc80_sur_L_prime= qmc80_sur_L_prime
            form.instance.Qm_sur_L_prime = Qm_sur_L_prime
            form.instance.cdmdBprime = cdmdBprime
            form.instance.cdmdMprime = cdmdMprime

            form.save()
            return redirect(reverse("caracteristique-detail", kwargs={
                'slug': form.instance.slug
            }))

            


             
           

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddDtCaractéristiqueTablier()

    return render(request, 'caractéristique-tablier/Add-caractéristique-tablier.html', {'form': form})