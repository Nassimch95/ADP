from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import Add_repartition_transversale_form
from .models import repartition_transversale
import numpy as np
import pandas as pd
from .guyonmassonet import k01,k02,k11,k12
import math
from scipy.integrate import quad

np.set_printoptions(suppress=True)



# teta et alpha :

# teta 

def get_Ip(Ia,Im):
  Ip = Ia + ((Im-Ia)*8/(3*3.14))
  
  return Ip 
  
def get_Ie(b,h):
    Ie = (b*h**3)/12
    return (Ie*10**(-8))
def get_r(Ip,Ie,n,v,L):
  r = ((n*v)/(2*L))*((Ip/Ie)**(1/4))
  return r 
  
def get_ro_p(E,Ip,v):
  ro_p =( E*Ip)/v
  return ro_p
  
def get_ro_e(E,Ie,u):
  ro_e =( E*Ie)/u
  return ro_e


def get_teta(b,L,ro_p,ro_e):
  teta = (b/L)* ((ro_p/ro_e)**(1/4))
  return round(teta,3 )
  
# alpha :

def get_section_fictive(h1,b1,b2,b3,h,S):# h1=15 ,b1,b2,b3,S largeur table de compression,ame,talon, et surface section mediane
    h_SF = np.array([h1])
    b_SF= np.array([b1,b2,b3])
    equation_SF = np.array([[1, 1], [b2, b3]]) # equation 1 equation 2
    resultat_SF = np.array([(h-h1), S-(b1*h1)]) # resultat 1 resultat 2
    h2_h3 = np.linalg.solve(equation_SF, resultat_SF)
    h_SF = np.append(h_SF,h2_h3)
    a_SF      = np.amax((np.array([h_SF,b_SF])),axis=0)
    b_SF      = np.amin((np.array([h_SF,b_SF])),axis=0)
    a_SF_sur_b_SF  = a_SF/b_SF
    k_a_sur_b =[]
    for x in a_SF_sur_b_SF :
        if x >= 1 and x<1.5 :
            k =round( ((( x-1)*(0.196-0.141))/(1.5-1))+0.141 ,3)
            k_a_sur_b.append(k)
        else:
            if  x >= 1.5 and x<2 :
                k =round( ((( x-1.5)*(0.229-0.196))/(2-1.5))+0.196 ,3)
                k_a_sur_b.append(k)
            else:
                if  x >= 2 and x<3 :
                    k =round( ((( x-2)*(0.263-0.229))/(3-2))+0.229 ,3)
                    k_a_sur_b.append(k)
                else:
                    if x >= 3 and x<4 :

                        k =round( ((( x-3)*(0.281-0.263))/(4-3))+0.263 ,3)
                        k_a_sur_b.append(k)
                    else:
                        if x > 4:
                            k=1/3
                            k_a_sur_b.append(k)

    
    return np.array(k_a_sur_b),a_SF,b_SF

def get_cp(k_a_sur_b,a_SF,b_SF,b_hourdis,h_hourdis):
    Cp = np.sum(k_a_sur_b*(a_SF*0.01)*(b_SF*0.01)**3) + ((1/6)*((b_hourdis*0.01)*(h_hourdis*0.01)**3))
    return Cp

def get_ce(h_entretoise):# la dalle joue le role d'entretoise 1m* h_hourdis
    Ce =  (1/6)*1*(h_entretoise*0.01)**3
    return Ce

def get_alpha (Cp,Ce,ro_p,ro_e,v,u):
    G = 1/(2*(1+0.15))
    gama_p =Cp/v
    gama_e =Ce/u
    alpha =( (gama_p+gama_e)/(2*(ro_p*ro_e)**(1/2)) )*G
    return round(alpha,3)

    

# teta et alpha 


def position (npoutres,ep):
    P_reel = np.array([])
    
    if  (npoutres % 2) == 0:
        P_positive = np.array([])
        i= math.floor((npoutres/2)+1)
        for x in range(1,i):
            p_positive = x - (1/2)
            P_positive =np.append(P_positive,p_positive)
        
        P_negative = (np.flip(P_positive))*(-1)

        P_reel=np.append(P_reel,P_negative)
        P_reel=np.append(P_reel,P_positive)

    else :
        P_positive = np.array([])
        i= math.floor((npoutres/2)+1)
       
        for x in range(1,i):
            p_positive = x 
            P_positive =np.append(P_positive,p_positive)
        
        P_negative = (np.flip(P_positive))*(-1)

        P_reel=np.append(P_reel,P_negative)
        P_reel=np.append(P_reel,0)
        P_reel=np.append(P_reel,P_positive)
    

    P_active = (P_reel *( (npoutres-1)/(npoutres) )*(2/npoutres))

    
    


    
    return P_reel,P_active
    
def interpolation_k(k1,k2,teta,teta_1,teta_2):
    k_array =[]
    
    
    for x in range(5):
        k_row = np.array([])
        for y in range(9):
            k = round(k1[x,y] +((k2[x,y]-k1[x,y])*((teta-teta_1)/(teta_2-teta_1))),4)
            k_row = np.append(k_row,k) 
        
        k_array.append(k_row)
    
    return np.array(k_array)


def interpolation_k_alpha(k1,k2,teta,alpha):
    k_array =[]
    exp = 1-math.exp((0.065-0.671)/0.563)
    for x in range(5):
        k_row = np.array([])
        for y in range(9):
            k = round(k1[x,y] +((k2[x,y]-k1[x,y])*(alpha**(exp))),4)
            k_row = np.append(k_row,k) 
        
        k_array.append(k_row)
    
    return np.array(k_array)


def interpolation_k_alpha_active(ka,yp):
    y =[0,0.25,0.5,0.75,1]
    if(yp) ==0:
        index_1=0
        index_2 =1
    else:
        index_1 = math.floor(abs(yp)*4)
        index_2 = math.ceil(abs(yp)*4)
    k_row_1 = ka[index_1]
    k_row_2 =ka[index_2]
    k_alpha_active_row=[]

    for x in range(9):
        k_alpha_active = round(
            ( ( (abs(yp)-y[index_1]) / (y[index_2]-y[index_1]) )* (k_row_2[x]-k_row_1[x]) ) + k_row_1[x]
            ,4)
        k_alpha_active_row.append(k_alpha_active)  
    
    if yp <0:
        kalpha_active_row = np.flip(np.array(k_alpha_active_row))

        
        
    else:
        kalpha_active_row =np.array(k_alpha_active_row)
    
    return  kalpha_active_row


def k_alpha_active_arr(P_active,ka):
    k_alpha_active_array =[]
    for x in P_active:
        kalpha_active_row = interpolation_k_alpha_active(ka,x)
        k_alpha_active_array.append(kalpha_active_row)
    
    return np.array(k_alpha_active_array)


def k_alpha_function(k_alpha_active_arr,b):
    K_ALPHA_FUNCTION = []
    x = np.array([-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1])*b
    for y in k_alpha_active_arr:
        k_alpha_function = np.polyfit(x, y, 2)
        K_ALPHA_FUNCTION.append(k_alpha_function)

    return np.array(K_ALPHA_FUNCTION)



# k alpha max 

def get_ka_max_for_mc120(K_ALPHA_FUNCTION):
    S_list=[]
    for f in K_ALPHA_FUNCTION[:3]:
        S= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.815
        x2= x1 +1
        x3= x2+2.3
        x4= x3+1
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x4 <=3.185:
 
            res1, err = quad(function, x1, x2) 
            res2, err = quad(function, x3, x4) 
            
            x1 =x1 +0.1
            x2 =x2 +0.1
            x3 = x3 +0.1
            x4 = x4 +0.1
            S= np.append(S,np.sum([res1,res2]))
        
        S_list.append(round(np.amax(S)/2,3))
    
    return S_list


                
def get_ka_max_for_D240(K_ALPHA_FUNCTION):
    K_D240=[]
    for f in K_ALPHA_FUNCTION[:3]:
        S= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.815
        x2= x1 +3.2
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x2 <=3.185:
 
            res1, err = quad(function, x1, x2) 
            
            x1 =x1 +0.1
            x2 =x2 +0.1
            S= np.append(S,res1)
        
        K_D240.append(round(np.amax(S)/3.20,3))
    
    return K_D240


def get_ka_max_for_A(K_ALPHA_FUNCTION):
    K_A_UNE_VOIE=[]
    K_A_DEUX_VOIE=[]
    for f in K_ALPHA_FUNCTION[:3]:
        S= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        res1, err = quad(function,-3.815,-0.315) 
        res2, err = quad(function,-3.815, 3.185) 
        
        K_A_UNE_VOIE.append(round(res1/3.5,3))
        K_A_DEUX_VOIE.append(round(res2/7,3))
    return K_A_UNE_VOIE,K_A_DEUX_VOIE

def get_ka_max_for_Qtr(K_ALPHA_FUNCTION):
    Qtr_UNE_VOIE=[]
    Qtr_DEUX_VOIE=[]
    for f in K_ALPHA_FUNCTION[:3]:
        S= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        res1, err = quad(function,-5.065, -4.315) 
        res2, err = quad(function,3.685, 5.065) 
        
        Qtr_UNE_VOIE.append(round(res1/0.75,3))
        Qtr_DEUX_VOIE.append(round((res1+res2)/2.13,3))
    return Qtr_UNE_VOIE,Qtr_DEUX_VOIE


def get_ka_max_for_Bc_1v(K_ALPHA_FUNCTION):
    K_Bc_1v=[]
    for f in K_ALPHA_FUNCTION[:3]:
        Y= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.565 # disposition transversale systeme Bc 
        x2= x1 +2
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x2 <=-0.565:
 
            y1 =function(x1)
            y2 =function(x2)
            y = (y1+y2)
            Y= np.append(Y,y)
            x1 =x1 +0.1
            x2 =x2 +0.1

        K_Bc_1v.append(round(np.amax(Y)/2,3))
            
        
        
    
    return K_Bc_1v

def get_ka_max_for_Bc_2v(K_ALPHA_FUNCTION):
    K_Bc_2v=[]
    for f in K_ALPHA_FUNCTION[:3]:
        Y= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.565 # disposition transversale systeme Bc 
        x2= x1 +2
        x3= x2 +0.5
        x4= x3 +2
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x4 <=2.935:
 
            y1 =function(x1)
            y2 =function(x2)
            y3 =function(x3)
            y4 =function(x4)
            y = (y1+y2+y3+y4)
            Y= np.append(Y,y)
            x1 =x1 +0.1
            x2 =x2 +0.1
            x3 =x3 +0.1
            x4 =x4 +0.1

        K_Bc_2v.append(round(np.amax(Y)/4,3))
            
        
        
    
    return K_Bc_2v

def get_ka_max_for_Bt_1v(K_ALPHA_FUNCTION):
    K_Bt_1v=[]
    for f in K_ALPHA_FUNCTION[:3]:
        Y= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.315 # disposition transversale systeme Bt 
        x2= x1 +2
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x2 <=-0.815:
 
            y1 =function(x1)
            y2 =function(x2)
            y = (y1+y2)
            Y= np.append(Y,y)
            x1 =x1 +0.1
            x2 =x2 +0.1

        K_Bt_1v.append(round(np.amax(Y)/2,3))
            
        
        
    
    return K_Bt_1v

def get_ka_max_for_Bt_2v(K_ALPHA_FUNCTION):
    K_Bt_2v=[]
    for f in K_ALPHA_FUNCTION[:3]:
        Y= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-3.315 # disposition transversale systeme Bc 
        x2= x1 +2
        x3= x2 +0.5
        x4= x3 +2
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x4 <=2.685:
 
            y1 =function(x1)
            y2 =function(x2)
            y3 =function(x3)
            y4 =function(x4)
            y = (y1+y2+y3+y4)
            Y= np.append(Y,y)
            x1 =x1 +0.1
            x2 =x2 +0.1
            x3 =x3 +0.1
            x4 =x4 +0.1

        K_Bt_2v.append(round(np.amax(Y)/4,3))
            
        
        
    
    return K_Bt_2v

def get_ka_max_for_Br(K_ALPHA_FUNCTION):
    K_Br=[]
    for f in K_ALPHA_FUNCTION[:3]:
        Y= np.array([])
        a = f[0]
        b = f[1]
        c = f[2]

        x1 =-4.315 # disposition transversale systeme Br 
       
        
        def function(x): 
            return a*x**2 +b*x + c 
        
        while x1 <=3.685:
 
            y1 =function(x1)
          
            y = round(y1,3)
            Y= np.append(Y,y)
            x1 =x1 +0.1
           

        K_Br.append(np.amax(Y))
            
        
        
    
    return K_Br

def repartition_transversale_home(request):
    repartition_transversale_list = repartition_transversale.objects.all()
    context ={
        'repartition_transversale_list':repartition_transversale_list

    }
   


    return render(request,'repartition-transversale/repartition_transversale_home.html',context)

def add_repartition_transversale(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_repartition_transversale_form(request.POST)

        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            repartition_longitudinal= form.cleaned_data['R_longitudinal']
            caracteristiques = repartition_longitudinal.caracteristiques
            lc =caracteristiques.Lc
            L = caracteristiques.L
            nv =caracteristiques.nv
            n_poutres = caracteristiques.tab.poutre.np
            Ia =round(caracteristiques.tab.poutre.sa.content_object.IG_avec_hourdis*10**-8,4)
            Im =round(caracteristiques.tab.poutre.sm.content_object.IG_avec_hourdis*10**-8,4)

            b1 = caracteristiques.tab.poutre.sm.content_object.b_table_de_compression
            b2 = caracteristiques.tab.poutre.sm.content_object.b_ame
            b3  = caracteristiques.tab.poutre.sm.content_object.b_talon
            b_hourdis  = caracteristiques.tab.poutre.sm.content_object.b_hourdis
            h_hourdis  = caracteristiques.tab.poutre.sm.content_object.h_hourdis
            h_section  = caracteristiques.tab.poutre.sm.content_object.h_section
            Am =  round(caracteristiques.tab.poutre.sm.content_object.B_TOTAL_BRUTE_SANS_HOURDIS,4)

            epdr =  caracteristiques.epdr
            v= epdr/(n_poutres-1)
            u=1
            b = (n_poutres*v)/2

            #repartition longitudidnal :

            A_TOTAL =  np.array(repartition_longitudinal.A_TOTAL)
            G_TOTAL =  np.array(repartition_longitudinal.G)
            qtr_TOTAL =  np.array(repartition_longitudinal.qtr_TOTAL)
            Mc120_TOTAL =  np.array(repartition_longitudinal.Mc120_TOTAL)
            D240_TOTAL =  np.array(repartition_longitudinal.D240_TOTAL)
            Br_TOTAL =  np.array(repartition_longitudinal.Br_TOTAL)
            Bt_TOTAL =  np.array(repartition_longitudinal.Bt_TOTAL)
            Bc_TOTAL =  np.array(repartition_longitudinal.Bc_TOTAL)
            
            
            # teta 

            Ip = get_Ip(Ia,Im)
            Ie = get_Ie(100,h_hourdis)# 100 cm = 1 m = (1m de dalle c'est l'entretoise)
            r = get_r(Ip,Ie,n_poutres,v,L)
            ro_p = get_ro_p(1,Ip,v)
            ro_e = get_ro_e(1,Ie,u)

            teta = get_teta(b,L,ro_p,ro_e)
            k_a_sur_b,a_SF,b_SF = get_section_fictive(15,b1,b2,b3,h_section,Am) 
            Cp  = get_cp (k_a_sur_b,a_SF,b_SF,b_hourdis,h_hourdis)
            Ce  = get_ce (25)
            alpha =get_alpha(Cp,Ce,ro_p,ro_e,v,u)
            
            P_reel,P_active = position(n_poutres,v)
            k0 = interpolation_k(k01,k02,teta,0.55,0.60)
            k1 = interpolation_k(k11,k12,teta,0.55,0.60)
            ka = interpolation_k_alpha(k0,k1,teta,alpha)

            k_alpha_active_array= k_alpha_active_arr(P_active,ka)
            K_ALPHA_FUNCTION = k_alpha_function(k_alpha_active_array,b)
            

            ka_max_mc_120 = get_ka_max_for_mc120(K_ALPHA_FUNCTION)
            K_D240  =     get_ka_max_for_D240(K_ALPHA_FUNCTION)
            K_Qtr_UNE_VOIE,K_Qtr_DEUX_VOIE = get_ka_max_for_Qtr(K_ALPHA_FUNCTION)
            
            K_A_UNE_VOIE,K_A_DEUX_VOIE = get_ka_max_for_A(K_ALPHA_FUNCTION)
            K_Bc_1v                       = get_ka_max_for_Bc_1v(K_ALPHA_FUNCTION)
            K_Bc_2v                       = get_ka_max_for_Bc_2v(K_ALPHA_FUNCTION)
            K_Bt_1v                       = get_ka_max_for_Bt_1v(K_ALPHA_FUNCTION)
            K_Bt_2v                       = get_ka_max_for_Bt_2v(K_ALPHA_FUNCTION)
            K_Br                          = get_ka_max_for_Br(K_ALPHA_FUNCTION)
           
            
            #poutre 1 
            p1_G = G_TOTAL*1/6

            p1_Mc120 = Mc120_TOTAL*ka_max_mc_120[0]/6
            p1_D240 = D240_TOTAL*K_D240[0]/6
            

            p1_A_1V  = A_TOTAL[:2]*K_A_UNE_VOIE[0]/6
            p1_A_2V  = A_TOTAL[2:4]*K_A_DEUX_VOIE[0]/6

            p1_Bc_1V  = Bc_TOTAL[:2]*K_Bc_1v[0]/6
            p1_Bc_2V  = Bc_TOTAL[2:4]*K_Bc_2v[0]/6

            p1_Bt_1V  = Bt_TOTAL[:2]*K_Bt_1v[0]/6
            p1_Bt_2V  = Bt_TOTAL[2:4]*K_Bt_2v[0]/6

            p1_Br =   Br_TOTAL*K_Br[0]/6   

            p1_qtr_1V  = qtr_TOTAL[:2]*K_Qtr_UNE_VOIE[0]/6
            p1_qtr_2V  = qtr_TOTAL[2:4]*K_Qtr_DEUX_VOIE[0]/6
         
            poutre_1 ={
               'G' :p1_G.tolist(),
               'Mc120':p1_Mc120.tolist(),
               'D240' : p1_D240.tolist(),
               'A1V'  :p1_A_1V.tolist(),
               'A2V'  :p1_A_2V.tolist(),
               'Bc1V' :p1_Bc_1V.tolist(),
               'Bc2V' :p1_Bc_2V.tolist(),
               'Bt1V' :p1_Bt_1V.tolist(),
               'Bt2V' :p1_Bt_2V.tolist(),
               'Br'   :p1_Br.tolist(),
               'qtr1V':p1_qtr_1V.tolist(),
               'qtr2V':p1_qtr_2V.tolist(),
            }

            # poutre 2 
            p2_G = G_TOTAL*1/6
            p2_Mc120 = Mc120_TOTAL*ka_max_mc_120[1]/6
            p2_D240 = D240_TOTAL*K_D240[1]/6
            

            p2_A_1V  = A_TOTAL[:2]*K_A_UNE_VOIE[1]/6
            p2_A_2V  = A_TOTAL[2:4]*K_A_DEUX_VOIE[1]/6

            p2_Bc_1V  = Bc_TOTAL[:2]*K_Bc_1v[1]/6
            p2_Bc_2V  = Bc_TOTAL[2:4]*K_Bc_2v[1]/6

            p2_Bt_1V  = Bt_TOTAL[:2]*K_Bt_1v[1]/6
            p2_Bt_2V  = Bt_TOTAL[2:4]*K_Bt_2v[1]/6

            p2_Br =   Br_TOTAL*K_Br[1]/6   

            p2_qtr_1V  = qtr_TOTAL[:2]*K_Qtr_UNE_VOIE[1]/6
            p2_qtr_2V  = qtr_TOTAL[2:4]*K_Qtr_DEUX_VOIE[1]/6

            poutre_2 ={
               'G' :p2_G.tolist(),
               'Mc120':p2_Mc120.tolist(),
               'D240' : p2_D240.tolist(),
               'A1V'  :p2_A_1V.tolist(),
               'A2V'  :p2_A_2V.tolist(),
               'Bc1V' :p2_Bc_1V.tolist(),
               'Bc2V' :p2_Bc_2V.tolist(),
               'Bt1V' :p2_Bt_1V.tolist(),
               'Bt2V' :p2_Bt_2V.tolist(),
               'Br'   :p2_Br.tolist(),
               'qtr1V':p2_qtr_1V.tolist(),
               'qtr2V':p2_qtr_2V.tolist(),
            }

            # poutre 3 
            p3_G = G_TOTAL*1/6
            p3_Mc120 = Mc120_TOTAL*ka_max_mc_120[2]/6
            p3_D240 = D240_TOTAL*K_D240[2]/6
            

            p3_A_1V  = A_TOTAL[:2]*K_A_UNE_VOIE[2]/6
            p3_A_2V  = A_TOTAL[2:4]*K_A_DEUX_VOIE[2]/6

            p3_Bc_1V  = Bc_TOTAL[:2]*K_Bc_1v[2]/6
            p3_Bc_2V  = Bc_TOTAL[2:4]*K_Bc_2v[2]/6

            p3_Bt_1V  = Bt_TOTAL[:2]*K_Bt_1v[2]/6
            p3_Bt_2V  = Bt_TOTAL[2:4]*K_Bt_2v[2]/6

            p3_Br =   Br_TOTAL*K_Br[2]/6   

            p3_qtr_1V  = qtr_TOTAL[:2]*K_Qtr_UNE_VOIE[2]/6
            p3_qtr_2V  = qtr_TOTAL[2:4]*K_Qtr_DEUX_VOIE[2]/6

            poutre_3 ={
               'G' :p3_G.tolist(),
               'Mc120':p3_Mc120.tolist(),
               'D240' : p3_D240.tolist(),
               'A1V'  :p3_A_1V.tolist(),
               'A2V'  :p3_A_2V.tolist(),
               'Bc1V' :p3_Bc_1V.tolist(),
               'Bc2V' :p3_Bc_2V.tolist(),
               'Bt1V' :p3_Bt_1V.tolist(),
               'Bt2V' :p3_Bt_2V.tolist(),
               'Br'   :p3_Br.tolist(),
               'qtr1V':p3_qtr_1V.tolist(),
               'qtr2V':p3_qtr_2V.tolist(),
            }
            
            # combinaison p1
            AB_P1 = np.array([
                p1_A_1V,
                p1_A_2V,
                p1_Bc_1V,
                p1_Bc_2V,
                p1_Bt_1V,
                p1_Bt_2V,
                p1_Br,

            ])

            Mc120_D240_P1 = np.array([
                p1_Mc120 ,
                p1_D240 ,
            ])

            Qtr_P1 = np.array([
                p1_qtr_1V,
                p1_qtr_2V,

            ])

            max_Qtr_p1 = np.amax(Qtr_P1,axis=0)
            max_AB_p1 =np.amax(AB_P1,axis=0)
            max_Mc120_D240_p1 =np.amax(Mc120_D240_P1,axis=0)

            combi_ELU_AB_p1 = 1.35*p1_G + 1.6*(max_AB_p1 + max_Qtr_p1)
            combi_ELU_Mc120_D240_p1 = 1.35*(p1_G + max_Mc120_D240_p1)
            combi_ELS_AB_p1 = p1_G + 1.2*(max_AB_p1 + max_Qtr_p1)
            combi_ELS_Mc120_D240_p1 = (p1_G + max_Mc120_D240_p1)
           

            print(combi_ELS_Mc120_D240_p1)

            #combinaison P2
            AB_P2 = np.array([
                p2_A_1V,
                p2_A_2V,
                p2_Bc_1V,
                p2_Bc_2V,
                p2_Bt_1V,
                p2_Bt_2V,
                p2_Br,

            ])

            Mc120_D240_P2 = np.array([
                p2_Mc120 ,
                p2_D240 ,
            ])

            Qtr_P2 = np.array([
                p2_qtr_1V,
                p2_qtr_2V,

            ])

            max_Qtr_p2 = np.amax(Qtr_P2,axis=0)
            max_AB_p2 =np.amax(AB_P2,axis=0)
            max_Mc120_D240_p2 =np.amax(Mc120_D240_P2,axis=0)


            combi_ELU_AB_p2 = 1.35*p2_G + 1.6*(max_AB_p2 + max_Qtr_p2)
            combi_ELU_Mc120_D240_p2 = 1.35*(p2_G + max_Mc120_D240_p2)
            combi_ELS_AB_p2 = p1_G + 1.2*(max_AB_p2 + max_Qtr_p2)
            combi_ELS_Mc120_D240_p2 = (p2_G + max_Mc120_D240_p2)
       

                        #combinaison P3
            AB_P3 = np.array([
                p3_A_1V,
                p3_A_2V,
                p3_Bc_1V,
                p3_Bc_2V,
                p3_Bt_1V,
                p3_Bt_2V,
                p3_Br,

            ])

            Mc120_D240_P3 = np.array([
                p3_Mc120 ,
                p3_D240 ,
            ])

            Qtr_P3 = np.array([
                p3_qtr_1V,
                p3_qtr_2V,

            ])

            max_Qtr_p3 = np.amax(Qtr_P3,axis=0)
            max_AB_p3 =np.amax(AB_P3,axis=0)
            max_Mc120_D240_p3 =np.amax(Mc120_D240_P3,axis=0)


            combi_ELU_AB_p3 = 1.35*p3_G + 1.6*(max_AB_p3 + max_Qtr_p3)
            combi_ELU_Mc120_D240_p3 = 1.35*(p3_G + max_Mc120_D240_p3)
            combi_ELS_AB_p3 = p3_G + 1.2*(max_AB_p3 + max_Qtr_p3)
            combi_ELS_Mc120_D240_p3 = (p3_G + max_Mc120_D240_p3)
            
           


            
            
            
            



            
            
            
            

            
            
            form.instance.Ia = Ia
            form.instance.Im = Im
            form.instance.Ip = Ip
            form.instance.Ie = Ie
            form.instance.r = r
            form.instance.ro_p = ro_p
            form.instance.ro_e = ro_e
            form.instance.teta = teta
            form.instance.a_SF = a_SF.tolist()
            form.instance.b_SF = b_SF.tolist()
            form.instance.K =  k_a_sur_b.tolist()
            form.instance.Cp = Cp
            form.instance.Ce = Ce
            form.instance.alpha = alpha
            form.instance.P_reel= P_reel.tolist()
            form.instance.P_active = P_active.tolist()
            form.instance.k0 = k0.tolist()
            form.instance.k1 = k1.tolist()
            form.instance.ka = ka.tolist()
            form.instance.ka_active = k_alpha_active_array.tolist()
            form.instance.K_ALPHA_FUNCTION = K_ALPHA_FUNCTION.tolist()
            form.instance.ka_max_mc_120 =ka_max_mc_120
            form.instance.K_D240=K_D240
            form.instance.K_Qtr_UNE_VOIE = K_Qtr_UNE_VOIE
            form.instance.K_Qtr_DEUX_VOIE = K_Qtr_DEUX_VOIE
            form.instance.K_A_UNE_VOIE = K_A_UNE_VOIE
            form.instance.K_A_DEUX_VOIE =K_A_DEUX_VOIE
            form.instance.K_Bc_1v   = K_Bc_1v 
            form.instance.K_Bc_2v   = K_Bc_2v 
            form.instance.K_Bt_1v   = K_Bt_1v 
            form.instance.K_Bt_2v   = K_Bt_2v 
            form.instance.K_Br   = K_Br
            #poutre 1 
            form.instance.poutre_1   = poutre_1
            form.instance.poutre_2   = poutre_2
            form.instance.poutre_3   = poutre_3
             
            #combinaison
            form.instance.combi_ELU_AB_p1 = combi_ELU_AB_p1.tolist()
            form.instance.combi_ELU_Mc120_D240_p1 = combi_ELU_Mc120_D240_p1.tolist()
            form.instance.combi_ELS_AB_p1 = combi_ELS_AB_p1.tolist()
            form.instance.combi_ELS_Mc120_D240_p1 = combi_ELS_Mc120_D240_p1.tolist()

            form.instance.combi_ELU_AB_p2 = combi_ELU_AB_p2.tolist()
            form.instance.combi_ELU_Mc120_D240_p2 = combi_ELU_Mc120_D240_p2.tolist()
            form.instance.combi_ELS_AB_p2 = combi_ELS_AB_p2.tolist()
            form.instance.combi_ELS_Mc120_D240_p2 = combi_ELS_Mc120_D240_p2.tolist()


            form.instance.combi_ELU_AB_p3 = combi_ELU_AB_p3.tolist()
            form.instance.combi_ELU_Mc120_D240_p3 = combi_ELU_Mc120_D240_p3.tolist()
            form.instance.combi_ELS_AB_p3 = combi_ELS_AB_p3.tolist()
            form.instance.combi_ELS_Mc120_D240_p3 = combi_ELS_Mc120_D240_p3.tolist()


                                




            form.save()
            return redirect(reverse("repartition_transversale_detail", kwargs={
                'slug': form.instance.slug
            }))
            
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_repartition_transversale_form()

    return render(request, 'repartition-transversale/add-repartition-transversale.html', {'form': form})



def repartition_transversale_detail(request,slug):
    repartition_longitudinal_detail = get_object_or_404(repartition_transversale,slug=slug)
    pd.options.display.float_format = '{:.3f}'.format
    Ia= repartition_longitudinal_detail.Ia
    Im= repartition_longitudinal_detail.Ip
    Ip= repartition_longitudinal_detail.Ip
    Ie= repartition_longitudinal_detail.Ie
    r= repartition_longitudinal_detail.r
    ro_p= repartition_longitudinal_detail.ro_p
    ro_e= repartition_longitudinal_detail.ro_e
    teta= repartition_longitudinal_detail.teta
    a_SF= repartition_longitudinal_detail.a_SF
    b_SF= repartition_longitudinal_detail.b_SF
    K= repartition_longitudinal_detail.K
    Cp= repartition_longitudinal_detail.Cp
    Ce= repartition_longitudinal_detail.Ce
    alpha= repartition_longitudinal_detail.alpha
    P_reel =repartition_longitudinal_detail.P_reel
    P_active =repartition_longitudinal_detail.P_active

    



    k0= repartition_longitudinal_detail.k0
    k1= repartition_longitudinal_detail.k1
    ka= repartition_longitudinal_detail.ka
    ka_active= repartition_longitudinal_detail.ka_active



    ka_max_mc_120 = repartition_longitudinal_detail.ka_max_mc_120
    K_D240 = repartition_longitudinal_detail.K_D240
    K_Qtr_UNE_VOIE = repartition_longitudinal_detail.K_Qtr_UNE_VOIE
    K_Qtr_DEUX_VOIE = repartition_longitudinal_detail.K_Qtr_DEUX_VOIE
    K_A_UNE_VOIE = repartition_longitudinal_detail.K_A_UNE_VOIE
    K_A_DEUX_VOIE = repartition_longitudinal_detail.K_A_DEUX_VOIE
    K_Bc_1v = repartition_longitudinal_detail.K_Bc_1v
    K_Bc_2v = repartition_longitudinal_detail.K_Bc_2v
    K_Bt_1v = repartition_longitudinal_detail.K_Bt_1v
    K_Bt_2v = repartition_longitudinal_detail.K_Bt_2v
    K_Br = repartition_longitudinal_detail.K_Br


    K_alpha_max = [[1,1,1],K_A_UNE_VOIE,K_A_DEUX_VOIE,K_Bc_1v,K_Bc_2v,K_Bt_1v,K_Bt_2v,K_Br,ka_max_mc_120,K_D240,K_Qtr_UNE_VOIE,K_Qtr_DEUX_VOIE]
    
    #poutre 1 
    poutre_1 = repartition_longitudinal_detail.poutre_1
    poutre_2 = repartition_longitudinal_detail.poutre_2
    poutre_3 = repartition_longitudinal_detail.poutre_3

    combi_ELU_AB_p1 = repartition_longitudinal_detail.combi_ELU_AB_p1
    combi_ELU_Mc120_D240_p1  = repartition_longitudinal_detail.combi_ELU_Mc120_D240_p1
    combi_ELS_AB_p1 = repartition_longitudinal_detail.combi_ELS_AB_p1
    combi_ELS_Mc120_D240_p1 = repartition_longitudinal_detail.combi_ELS_Mc120_D240_p1
    
    combi_ELU_AB_p2 = repartition_longitudinal_detail.combi_ELU_AB_p2
    combi_ELU_Mc120_D240_p2 = repartition_longitudinal_detail.combi_ELU_Mc120_D240_p2
    combi_ELS_AB_p2 = repartition_longitudinal_detail.combi_ELS_AB_p2
    combi_ELS_Mc120_D240_p2 = repartition_longitudinal_detail.combi_ELS_Mc120_D240_p2
   

    combi_ELU_AB_p3 = repartition_longitudinal_detail.combi_ELU_AB_p3
    combi_ELU_Mc120_D240_p3 = repartition_longitudinal_detail.combi_ELU_Mc120_D240_p3
    combi_ELS_AB_p3 = repartition_longitudinal_detail.combi_ELS_AB_p3
    combi_ELS_Mc120_D240_p3 = repartition_longitudinal_detail.combi_ELS_Mc120_D240_p3
   
   







    
    df_k0 = pd.DataFrame(k0,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_k0 = df_k0.to_html()

    df_k1 = pd.DataFrame(k1,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_k1 = df_k1.to_html()

    df_ka = pd.DataFrame(ka,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_ka = df_ka.to_html()

    df_ka_active = pd.DataFrame(ka_active,index=['P1' ,'P2' ,'P3' ,'P4', 'P5','P6'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_ka_active = df_ka_active.to_html()

    df_ka_max = pd.DataFrame(K_alpha_max,index=['G' ,'A 1' ,'A 2' ,'Bc 1', 'Bc 2','Bt 1','Bt 2','Br','Mc120','D240','Qtr gauche','Qtr D + G'],columns=['Poutre 1', 'Poutre 2', 'Poutre 3', ]) 
    html_ka_max = df_ka_max.to_html()
    
    #Combi 1 
    df_combi_ELU_AB_p1 = pd.DataFrame(combi_ELU_AB_p1,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELU_Mc120_D240_p1 = pd.DataFrame(combi_ELU_Mc120_D240_p1,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_AB_p1 = pd.DataFrame(combi_ELS_AB_p1,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_Mc120_D240_p1 = pd.DataFrame(combi_ELS_Mc120_D240_p1,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
   
    df_combi_1 = [df_combi_ELU_AB_p1,df_combi_ELU_Mc120_D240_p1,df_combi_ELS_AB_p1,df_combi_ELS_Mc120_D240_p1]
    df_combi_1_result = pd.concat(df_combi_1)
    html_df_combi_1_result= df_combi_1_result.to_html()
    
    #Combi 2
    df_combi_ELU_AB_p2 = pd.DataFrame(combi_ELU_AB_p2,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELU_Mc120_D240_p2 = pd.DataFrame(combi_ELU_Mc120_D240_p2,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_AB_p2 = pd.DataFrame(combi_ELS_AB_p2,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_Mc120_D240_p2 = pd.DataFrame(combi_ELS_Mc120_D240_p2,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_2 = [df_combi_ELU_AB_p2,df_combi_ELU_Mc120_D240_p2,df_combi_ELS_AB_p2,df_combi_ELS_Mc120_D240_p2]
    df_combi_2_result = pd.concat(df_combi_2)
    html_df_combi_2_result= df_combi_2_result.to_html()
    

    #Combi 3
    df_combi_ELU_AB_p3 = pd.DataFrame(combi_ELU_AB_p3,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELU_Mc120_D240_p3 = pd.DataFrame(combi_ELU_Mc120_D240_p3,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_AB_p3 = pd.DataFrame(combi_ELS_AB_p3,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_ELS_Mc120_D240_p3 = pd.DataFrame(combi_ELS_Mc120_D240_p3,index=['M' ,'T'],columns=['0', 'L/8', 'L/4','3L/8','Xc','L/2' ]) 
    df_combi_3 = [df_combi_ELU_AB_p3,df_combi_ELU_Mc120_D240_p3,df_combi_ELS_AB_p3,df_combi_ELS_Mc120_D240_p3]
    df_combi_3_result = pd.concat(df_combi_3)
    html_df_combi_3_result= df_combi_3_result.to_html()
     
  

    
    

    context ={
        'html_k0' :html_k0,
        'html_k1' :html_k1,
        'html_ka' :html_ka,
        'html_ka_active' :html_ka_active,
        'html_ka_max':html_ka_max,
        'Ia': Ia,
        'Im':Im,
        'Ip': Ip,
        'Ie': Ie,
        'r': r,
        'ro_p': ro_p,
        'ro_e':ro_e,
        'teta': teta,
        'a_SF':a_SF,
        'b_SF':b_SF,
        'K':K,
        'Cp':Cp,
        'Ce':Ce,
        'alpha' : alpha,
        'P_reel' :P_reel,
        'P_active' :P_active,

        'poutre_1':poutre_1,
        'poutre_2':poutre_2,
        'poutre_3':poutre_3,

       
        'html_df_combi_1_result':html_df_combi_1_result,
        'html_df_combi_2_result':html_df_combi_2_result,
        'html_df_combi_3_result':html_df_combi_3_result,
    }

    return render(request, 'repartition-transversale/detail-repartition-transversale.html',context)


