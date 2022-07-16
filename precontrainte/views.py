from django.shortcuts import render, get_object_or_404, redirect, reverse
import numpy as np
import pandas  as pd
from scipy.optimize import fsolve
from scipy.integrate import quad
from cart.models import  Cart

import math
"""
from .forms import Add_precontrainte_form
from .models import precontrainte
# Create your views here.
"""

def get_section_nette(section):
  Bn = 0.95*section[0]
  V_prime  = section[1]
  V  = section[2]
  In =0.9*section [3]
  ro = In/(Bn*V*V_prime)
  h = section[5]
  
  section_nette = np.array([Bn,V_prime,V,In,ro,h])
  
  return section_nette 

def get_P1_P2(delta_M,M_max_els,Sbt1,Sbt2,d_prime,section):
  
  P1 = (delta_M+(section[4]*section[0]*(section[2]*Sbt2+section[1]*Sbt1)))/(section[4]*section[5])
  P2 = ((section[4]*section[2]*section[0] *Sbt2)+ M_max_els)/( (section[4]*section[2])+(section[1]-d_prime) )
  Pmin = max(P1,P2)
  critique =""
  if P2> P1 :
    critique = "la section  est surcritique,le segment de passage du câble à une de ses frontières qui coupe la zone d’enrobage, donc l’effort de précontrainte économique P1 n’est plus suffisant, la précontrainte doit reprendre 100 pour cent du poids propre"
    
  return P1,P2,Pmin,critique

def get_nombre_de_cable(Pmin,fprg,fpeg,A_cable):
  
  P0 = min(0.8*fprg*A_cable,0.9*fpeg*A_cable)
  n= Pmin/(0.68*P0)
  
  note_P0 = "P0 = min( 0.8*{}*{},0.9*{}* {} )".format(fprg,A_cable,fpeg,A_cable)
  note_n = " n>= {}/(0.68*{})".format(Pmin,P0)
  
  return P0,n,note_P0,note_n

def verification_borne_superieur_precontrainte(n,P0,Sbc1,delta_M,section):
  Pcmu = n*P0 *0.68
  Pmax = Sbc1*section[0] -(delta_M/(section[4]*section[5]))
  if Pcmu < Pmax :
    verif_bsp = "verifie"
  return Pcmu,Pmax,verif_bsp
  

def nombre_de_cable_section_about(P0,g_poutre,d_prime,L,section):
    e0 = -( section[1]- d_prime)
    Mg= ((g_poutre*L**2)/(8))/100
    Sbt =-4.5
    Sbc = 24

    nsup= (Sbt -((Mg*section[2])/section[3]))/((0.9*P0/section[0])+(0.9*P0*e0*section[2]/section[3]))
    ninf= (Sbc +((Mg*section[2])/section[3]))/((0.9*P0/section[0])-(0.9*P0*e0*section[2]/section[3]))
    
    



   
    return nsup,ninf,e0,Mg

def verification_contrainte(jours,pourcentage,fc28,P0,n,e0,Mg,section):
    # verication avec estimation de perte de tension de 1/10
    Result = []
    for j in range(0,2):
        P= 0.9*P0*n *pourcentage[j]
        fc = (jours[j]/(4.76+(0.83*jours[j])))*fc28
        ft =( 0.06*fc) +0.6
        S_bare_c = 0.6*fc
        S_bare_t = -1.5 *ft
        Ssup = (P/section[0])+((section[2]/section[3])*((P*e0)+Mg))
        Sinf = (P/section[0])-((section[2]/section[3])*((P*e0)+Mg))
        result = np.array([Ssup,S_bare_t,Sinf,S_bare_c,j])
        Result.append(result)
      
    
    conclusion = "une famille de 4 cable  tiré a 50pc  en premiere phase sur le banc eet a 100 pc sur l'appui"
    
    return Result,conclusion

def get_angle_de_relevage(n_about,diametre_gaine,ft28,Vm,VM,P0,section):

  b0 = 0.60 # largeur ame
  m= 1 # nombre de gain par lit 
  k= 0.5 # gaines injectes au coulis de ciment 
  bn = b0-m*k*diametre_gaine
  P = 0.68*P0*n_about
  B_brute = section[0]
  B_nette = B_brute-(3.14*n_about*diametre_gaine**2)/4
  sigma_x = P/B_nette
  tau_bare =( 0.4*ft28*(ft28+((2/3)*sigma_x)))**(1/2)
  V_bare =  tau_bare*bn*0.8*section[5]

  alpha_1 = (math.asin((VM-V_bare)/P))*(180/3.14)
  alpha_2 = (math.asin((Vm+V_bare)/P))*(180/3.14)
  alpha_adp =math.asin((VM+Vm)/(2*P))*(180/3.14)
  
  angle_de_relevage ={
    
    'b0' : b0,
    'm':  m,
    'k':  k,
    'bn' :bn,
    'P' : P,
    'B_brute' : B_brute,
    'B_nette' : B_nette,
    'sigma_x' : sigma_x,
    'tau_bare' :tau_bare,
    'V_bare' :  V_bare,

    'alpha_1' : alpha_1,
    'alpha_2' : alpha_2,
    'alpha_adp' :alpha_adp,

  }

  


  return angle_de_relevage

def get_xk(angle_arr,yk_arr):
  
  xk_arr =np.array([])
  xd_arr =np.array([])
  a_arr = np.array([])
  for i in range(4):
    alpha = angle_arr[i]
    yk = yk_arr[i]
    a = 1 
    b =-((2*yk/math.tan(alpha*3.14/180))-0.9)
    c = 0.203
    coef= np.array([a,b,c])
    xk= np.max(np.roots(coef))
    xd =20-xk
    a =yk/((xk+0.5)**2)
    xk_arr =np.append(xk_arr,xk)
    xd_arr =np.append(xd_arr,xd)
    a_arr =np.append(a_arr,a)

    
    
  
  return xk_arr,xd_arr,a_arr

def get_position_cable(Caractéristiques_cables,L):
  position_r = np.array([0, 0.45, 4.075, 4.075, L/4, 3*L/8, L/2])
  position = position_r-0.45
  y_arr = []
  alpha_arr =[]
  for i in range(4):
    y_row = np.array([])
    alpha_row =np.array([])
    a = Caractéristiques_cables[5,i]
    xk = Caractéristiques_cables[3,i]
    d = Caractéristiques_cables[6,i]
    for x in position :
      y = a*(xk-x)**2 +d
      tanalpha= 2*a*(xk-x)
      alpha = math.atan(tanalpha)*(180/math.pi)


      y_row = np.append(y_row,y)
      alpha_row = np.append(alpha_row,alpha)
    
    y_arr.append(y_row)
    alpha_arr.append(alpha_row)

    

    
  return np.array(y_arr),np.array(alpha_arr)


def get_caracterisitique_poutre_nette(section_about,section_intermediare,section_mediane,y_arr,n,L):
  position_r = np.array([0, 0.45, 4.075, 4.075, L/4, 3*L/8, L/2])
  position = position_r-0.45
  B_list=np.array([])
  Vs_list=np.array([])
  V_list=np.array([])
  I_list=np.array([])
  ro_list=np.array([])

  for x in range(7):

    if position[x]<2.325:

      section = section_about

    else:

      if position[x]>= 2.325 and position[x]<=4.075:

        section =section_intermediare

      else:

        section =section_mediane

          
    B= section[0]
    V= section[2]
    Vs = section[1]
    IG=section[3]
    h = section[5]
    yi = y_arr[0:,x]   
    B_gaine = 50.24*10**(-4)
    

    Bn = B - (n*B_gaine)

    Vs_nette =((Vs*B)-(B_gaine*np.sum(yi)))/Bn
    V_nette =  h-Vs_nette
    In = IG -(B*(Vs_nette-Vs)**2) - (B_gaine*np.sum((yi-Vs_nette)**2))
    ro_nette = In/(Vs_nette*V_nette*Bn)

    B_list= np.append(B_list,Bn)
    Vs_list=np.append(Vs_list,Vs_nette)
    V_list= np.append(V_list,V_nette)
    I_list=np.append(I_list,In)
    ro_list= np.append(ro_list,ro_nette)




  return B_list, Vs_list, V_list ,I_list ,ro_list

def get_caracterisitique_poutre_homogene(section_nette,y_arr,n,L,h):
  B_list_homogene = np.array([])
  V_list_homogene = np.array([])
  Vs_list_homogene = np.array([])
  IG_list_homogene = np.array([])
  ro_list_homogene = np.array([])


  B_list= section_nette[0]
  V_list= section_nette[2]
  Vs_list = section_nette[1]
  IG_list= section_nette[3]
  K=5
  
  
  Ap = 1668*10**(-6) # section du cable 

  for x in range(7):
    B= B_list[x]
    V= V_list[x]
    Vs= Vs_list [x]
    IG= IG_list[x]
    yi = y_arr[0:,x]   

    Bh = B + (K*n*Ap)

    Vs_h = ((Vs*B)+(K*Ap*np.sum(yi)))/Bh 

    V_h=  h-Vs_h

    Ih = IG +(B*(Vs_h-Vs)**2) + (K*Ap*np.sum((Vs_h-yi)**2))
    ro_h = Ih/(Vs_h*V_h*Bh)

    B_list_homogene = np.append(B_list_homogene,Bh)
    V_list_homogene = np.append(V_list_homogene,V_h)
    Vs_list_homogene =np.append(Vs_list_homogene,Vs_h)
    IG_list_homogene =np.append(IG_list_homogene,Ih)
    ro_list_homogene =np.append(ro_list_homogene,ro_h)

  
  return B_list_homogene,Vs_list_homogene,V_list_homogene,IG_list_homogene,ro_list_homogene

# perte de tension 

#instantanée
def get_perte_par_frottement(P0,alpha_arr,f,fi,A_cable,L):
  alpha_frottement_arr = []
  Sigma_px_frottment_arr= []
  delta_sigma_frottement_arr =[]
  
  
  position = np.array([0, 0, 4.075, 4.075, (L/4)-0.45, (3*L/8)-0.45, (L/2)-0.45])
  angle_origine = alpha_arr[0:,0]  # a x = -0.5

  Sigma_P0 =( P0/A_cable)
  

  for x in range (4):
    alpha = abs(alpha_arr[x]-angle_origine[x])*(math.pi/180)
    Sigma_px  = Sigma_P0*(1-(f*alpha)-(fi* position))
    delta_sigma_frottement = Sigma_P0-Sigma_px

    alpha_frottement_arr.append(alpha)
    Sigma_px_frottment_arr.append(Sigma_px)
    delta_sigma_frottement_arr.append(delta_sigma_frottement)

  

  return np.array(alpha_frottement_arr),np.array(Sigma_px_frottment_arr),np.array(delta_sigma_frottement_arr)


def get_perte_par_recule(Sigma_px_frottment_arr,xk_arr,Ep):
  Sigma_P_Prime=[]
  g = 6*10**(-3)
  L_AB = xk_arr + 0.45
 
  Sigma_a = Sigma_px_frottment_arr[0:,0]
  Sigma_b = Sigma_px_frottment_arr[0:,-1]
  Sigma_c = Sigma_px_frottment_arr[0:,-1]

  d =(( g*Ep*L_AB)/(Sigma_a-Sigma_b))**0.5

  

  # pour ce cas  on d a peu pres = 20 donc a L/2 donc le pont M(d,Sigma_M) est confondu avec le point C(L/2,Simga(L/2))
  # donc simga_M =Simga_C 
  # pour d'autre cas  Simga est derterminer avec le theoreme de theme si M apartien au segment [AB] ou bien  les triangle semblable si M apartien au segment [AB]
  
  Sigma_m= Sigma_c
  Sigma_P =Sigma_px_frottment_arr
  for i in range(4):
    
    sigma_p_prime = Sigma_P[i]-2*(Sigma_P[i]-Sigma_m[i])
    Sigma_P_Prime.append(sigma_p_prime)
  
  delta_Sigma_recule_arr = Sigma_P - np.array(Sigma_P_Prime)
  return Sigma_m,Sigma_P,np.array(Sigma_P_Prime),np.around(delta_Sigma_recule_arr,3)
  
def get_effet_premiere_famille_sur_elle_meme(Ep,Eb,P0,A_cable,g_poutre,y_arr,delta_sigma_frottement_arr,delta_Sigma_recule_arr,poutre_nette,L,n):
  position = np.array([0, 0, 4.075, 4.075, (L/4)-0.45, (3*L/8)-0.45, (L/2)-0.45])
  
  
  K= (n-1)/(2*n)
  Bn = poutre_nette[0]
  Vs_n = poutre_nette[1]
  Vn  = poutre_nette[2]
  In  = poutre_nette[3]
  Sigma_P0 =( P0/A_cable)
  delta_sigma_frottement= np.average(delta_sigma_frottement_arr,axis=0)
  delta_Sigma_recule = np.average(delta_Sigma_recule_arr,axis=0)
  yi = np.average(y_arr, axis=0)
  gp =g_poutre/100 # MN
  Mg = gp*((L-position)/2)*position
  ep1 = -Vs_n+ yi

  alpha = (ep1**2/In) + (1/Bn)
  Beta = (Mg/In)*ep1
  gama =n*A_cable*(Sigma_P0-(delta_sigma_frottement+delta_Sigma_recule))
  delta_sigma_cj = Beta +( gama*alpha)
  delta_sigma_racc = K*(Ep/Eb)*delta_sigma_cj
  
  effet_premiere_famille = np.array([
    Mg,
    ep1,
    In,
    Bn,
    Vs_n,
    Beta,
    alpha,
    delta_sigma_cj,
    delta_sigma_racc

  ])

  
  return effet_premiere_famille

def get_effet_dalle_sur_premiere_famille_(Ep,Eb,g_dalle,g_pre_dalle,y_arr,poutre_nette,L,n):
  position = np.array([0, 0, 4.075, 4.075, (L/4)-0.45, (3*L/8)-0.45, (L/2)-0.45])
  
 
  Bn = poutre_nette[0]
  Vs_n = poutre_nette[1]
  Vn  = poutre_nette[2]
  In  = poutre_nette[3]
  
  yi = np.average(y_arr, axis=0)
  gdalle =g_dalle/100 # MN
  gpredalle = g_pre_dalle/100
  gt = gdalle+gpredalle
  Mg = gt*((L-position)/2)*position
  ep1 = -Vs_n+ yi

  
  delta_sigma_racc = (Mg/In)*ep1 *(Ep/Eb)
  
  
 
  
  effet_dalle_sur_premiere_famille = np.array([
    Mg,
    ep1,
    In,
    delta_sigma_racc

  ])

  
  return effet_dalle_sur_premiere_famille

       
def get_effet_complement_sur_premiere_famille_(Ep,Eb,g_complement,y_arr,poutre_nette,L,n):
  position = np.array([0, 0, 4.075, 4.075, (L/4)-0.45, (3*L/8)-0.45, (L/2)-0.45])
  
 
  Bn = poutre_nette[0]
  Vs_n = poutre_nette[1]
  Vn  = poutre_nette[2]
  In  = poutre_nette[3]
  
  yi = np.average(y_arr, axis=0)
  gc =g_complement/100 # MN
 
 
  Mg = gc*((L-position)/2)*position
  ep1 = -Vs_n+ yi

  
  delta_sigma_racc = (Mg/In)*ep1 *(Ep/Eb)
  
  
 
  
  effet_complement_sur_premiere_famille = np.array([
    Mg,
    ep1,
    In,
    delta_sigma_racc

  ])

  
  return effet_complement_sur_premiere_famille

def verification_contrainte_a_28_jours(P0,A_cable,effet_premiere_famille,delta_sigma_frottement_arr,delta_Sigma_recule_arr):
  # verication avec  les vrai p.tension
  SP0= P0/A_cable
  delta_sigma_frottement = np.average(delta_sigma_frottement_arr)
  delta_Sigma_recule =np.average(delta_Sigma_recule_arr)
  delta_sigma_racc = effet_premiere_famille[8]#on prend que l'effet de la premiere famille sur elle meme les autres effet  son sont pas present a 28 jours 
  p_frotemment = delta_sigma_frottement*A_cable
  P_racc = delta_sigma_racc*A_cable
  P = ((SP0)-((delta_sigma_frottement+delta_sigma_racc +delta_Sigma_recule)))*4*A_cable
  Mg= effet_premiere_famille[0]
  ep1=effet_premiere_famille[1]
  In= effet_premiere_famille[2]
  Bn=effet_premiere_famille[3]
  Vs_n=effet_premiere_famille[4]
  V_n =2-Vs_n

  sigma_sup = (P/Bn)+((P*Vs_n*ep1)/In)+((Mg*Vs_n)/In)
  sigma_inf= (P/Bn)-((P*Vs_n*ep1)/In)-((Mg*Vs_n)/In)
  #
  fc28 = 40 # MPA 
  ft28 = 0.06*fc28 +0.6 # MPA 
  S_bare_c = 0.6*fc28
  S_bare_t = -1.5 *ft28
  
 
 
  return sigma_inf,S_bare_c

#différées : 

def get_retrait_béton(poutre_nette,poutre_nette_dalle,L,Ep):
  t0_p = 28
  er = 0.0003
  t0_pd= 63
  
  Périmètre_P = np.array([6.02,6.02,6.27,6.27,6.34,6.34,6.34])
  Périmètre_PD = Périmètre_P+ 2.02
  Bn =poutre_nette[0]
  Bn_d = poutre_nette_dalle[0]
  rm_p = Bn*100/Périmètre_P # cm
  rm_pd =  Bn_d*100/Périmètre_PD # cm
  rto_p = t0_p/(t0_p+9*rm_p)
  rto_pd = t0_pd/(t0_pd+9*rm_pd)
  delta_sigma_retrait = er*(1-rto_p)*Ep
  delta_sigma_retrait_pd = er*(1-rto_pd)*Ep

  return delta_sigma_retrait,delta_sigma_retrait_pd

def get_relaxation_des_armatures(P0,A_cable,fprg,delta_sigma_frottement_arr,delta_Sigma_recule_arr,effet_premiere_famille,effet_dalle_sur_premiere_famille,effet_complement_sur_premiere_famille):
  u_0 =0.43
  ro_1000 = 2.5
  Sigma_P0 = P0/A_cable
  delta_sigma_frottement = np.average(delta_sigma_frottement_arr,axis=0)
  delta_Sigma_recule = np.average(delta_Sigma_recule_arr,axis=0)
  sigma_p  = Sigma_P0 -(delta_sigma_frottement+delta_Sigma_recule+effet_premiere_famille[-1]+effet_dalle_sur_premiere_famille[-1]+effet_complement_sur_premiere_famille[-1])
  u = sigma_p/fprg
  delta_sigma_relax= 0.06*ro_1000*sigma_p*(u-u_0)
  return sigma_p,u,delta_sigma_relax


#fuseau de passage 

def get_fuseau_de_passage(alpha_arr,y_arr,P0,A_cable,delta_sigma_some,poutre_homogene_dalle,poutre_nette_dalle):
  fc28 = 40
  ft28= -3 
  sigma_bare_t  = 1.5*ft28
  sigma_bare_c  = 0.6*fc28
  Vs_nette = poutre_nette_dalle[1]
  some_cos_ai = np.sum(np.cos(np.radians(alpha_arr)),axis=0)
  P1    = (1.02*P0)-(0.8*A_cable*delta_sigma_some)
  P2    = (0.98*P0)-(1.2*A_cable*delta_sigma_some)
  P1_P2 =  np.array([P1*some_cos_ai,P2*some_cos_ai])
  PI = np.amax(P1_P2,axis=0)
  Bh    = poutre_homogene_dalle[0]
  V_h     = poutre_homogene_dalle[2]
  Vs_h    = poutre_homogene_dalle[1]
  ro_h  = poutre_homogene_dalle[4]
  C     = ro_h*V_h*(1-(Bh*ft28/PI))
  C_prime     = ro_h*Vs_h*(1-(Bh*sigma_bare_t/PI))
  y_prime     =ro_h*V_h*((Bh*sigma_bare_c)/PI-1)
  y    =ro_h*Vs_h*((Bh*sigma_bare_c)/PI-1)
  Mmin = np.array([0.000, 0.000, 323.230, 323.230, 554.108, 692.635 , 738.811])/100
  Mmax = np.array([0.000, 0.000 , 545.916, 545.916, 935.856, 1169.820 , 1247.808])/100
  

  
  
 
  
  

  fuseau = np.array([
    some_cos_ai,
    P1,
    P2,
    P1*some_cos_ai,
    P2*some_cos_ai,
    PI,#PI
    Bh   ,
    V_h  ,  
    Vs_h ,
    ro_h  ,
    C,
    C_prime,
    y_prime,
    y,
    Mmin,
    Mmax,
    Mmin/PI,
    Mmax/PI,
    -(Mmin/PI)-y_prime,
    -(Mmin/PI)-C_prime,
    -(Mmax/PI)+y,
    -(Mmax/PI)+C,
    np.amin(np.array([ -(Mmax/PI)+y,-(Mmax/PI)+C]),axis=0),
    np.amax(np.array([-(Mmin/PI)-y_prime, -(Mmin/PI)-C_prime]),axis=0),
    -Vs_nette + np.average(y_arr)
    
    

   
    
    
    


   
   
    
    
  ])
  return fuseau

  
def precontrainte_home(request):
    #béton :
    fc28 = 40 # MPA 
    ft28 = 0.06*fc28 +0.6 # MPA 
    Ep = 190000
    Eb = 11000*((fc28)**(1/3))
    #poutre 
    g_poutre =2.019025 #t/ml
    L = 40
    g_dalle=6.3312
    g_pre_dalle=0.4000
    g_complement = 3.3109 # corniche reverment trottoir ...
    #contrainte admissible de la section 
    Sbc1 = 0.6*fc28
    Sbc2 = 0.5*fc28
    Sbt1= -1.5*ft28
    Sbt2 =-ft28


    diametre_gaine = 0.08 # 0.08 metre
    fprg=1860
    fpeg=1600
    A_cable=1668*10**-6
    d_prime = 0.138 # distance d'enrobage 
    nombre_cable = 4 # nombre de cable a a dopter 
    f = 0.18 # Coefficient de frottement en courbe et vaut 0,18 rad−1.
    fi = 0.002 #Coefficient de frottement par unité de longueur (2×10−3 𝑚−1).

    # disposition cable section mediane :
    disposition_mediane=np.array([0.138,0.232,0.416,0.514])
    # disposition cable section about:
    disposition_about= np.array([0.531,0.87,1.309,1.648])
    

    M_max_els = 12.47808 # M(G+240)  Mn.m 
    M_min_els  = 7.38811 # = M(G)
    delta_M = M_max_els-M_min_els
    Vm = 0.73881# T(G+240)  Mn.m 
    VM = 1.24781 # = T(G)

    #Caractéristiques Géométriques de la Section Médiane.(poutre + dalle).
    about = np.array([1.2570 ,1.0424 ,0.9576,0.4476,0.3568,2])
    about_dalle =np.array([1.7070, 1.3278 ,0.9222 ,0.8384, 0.4011, 2.25])

    intermediaire = np.array([0.8693,1.0336,0.9664,0.3692,0.4252,2])
    intermediare_dalle = np.array([1.3193, 1.4059, 0.8441 ,0.7247, 0.4629,2.25])
    

    mediane = np.array([0.7309, 1.0274, 0.9726, 0.3466,0.4746, 2])
    mediane_dalle = np.array([1.1809, 1.4456, 0.8044, 0.6845, 0.4985, 2.25])


    mediane_dalle_nette = get_section_nette(mediane_dalle)
    mediane_nette = get_section_nette(mediane)

    P1,P2 ,Pmin,critique = get_P1_P2(delta_M,M_max_els,Sbt1,Sbt2,d_prime,mediane_dalle_nette)
    P0,n,note_P0,note_n = get_nombre_de_cable(Pmin,fprg,fpeg,A_cable)
    Pcmu,Pmax,verif_bsp = verification_borne_superieur_precontrainte(n,P0,Sbc1,delta_M,mediane_dalle_nette)
    nsup,ninf,e0,Mg=  nombre_de_cable_section_about(P0,g_poutre,d_prime,L,mediane_nette)
    
    Result ,conclusion= verification_contrainte(np.array([7,28]),np.array([0.5,1]),fc28,P0,nombre_cable,e0,Mg,mediane_nette)
    angle_de_relevage = get_angle_de_relevage(nombre_cable,diametre_gaine,ft28,Vm,VM,P0,about_dalle)
    # angle de relevage adopter
    angle_arr = np.array([2.2,3.5,5.2,6.2])
    yk_arr = disposition_about-disposition_mediane
    xk_arr,xd_arr,a_arr  = get_xk(angle_arr,yk_arr)

    Caractéristiques_cables=np.array([
      angle_arr,
      disposition_about,
      yk_arr,
      xk_arr,
      xd_arr,
      a_arr,
      disposition_mediane

    ])
    

    y_arr,alpha_arr = get_position_cable(Caractéristiques_cables,L)

    B_list, Vs_list, V_list ,I_list ,ro_list =get_caracterisitique_poutre_nette(about,intermediaire,mediane,y_arr,4,L)
    poutre_nette= np.array([
       B_list,
       Vs_list,
       V_list ,
       I_list ,
       ro_list,
       

    ])

    B_list_dalle, Vs_list_dalle, V_list_dalle ,I_list_dalle ,ro_list_dalle =get_caracterisitique_poutre_nette(about_dalle,intermediare_dalle,mediane_dalle,y_arr,4,L)
    poutre_nette_dalle= np.array([
       B_list_dalle,
       Vs_list_dalle,
       V_list_dalle,
       I_list_dalle,
       ro_list_dalle,
       

    ])
    
    #poutre seul 
    B_list_homogene_d,Vs_list_homogene_d,V_list_homogene_d,IG_list_homogene_d,ro_list_homogene_d= get_caracterisitique_poutre_homogene(poutre_nette_dalle,y_arr,4,L,2)
  
    poutre_homogene_dalle = np.array([
      B_list_homogene_d,
      Vs_list_homogene_d,
      V_list_homogene_d,
      IG_list_homogene_d,
      ro_list_homogene_d,

    ])

    alpha_frottement_arr,Sigma_px_frottment_arr,delta_sigma_frottement_arr =  get_perte_par_frottement(P0,alpha_arr,f,fi,A_cable,L)
    
    Sigma_m,Sigma_P,Sigma_P_Prime,delta_Sigma_recule_arr = get_perte_par_recule(Sigma_px_frottment_arr,xk_arr,Ep)
 

  

  

 
    effet_premiere_famille =  get_effet_premiere_famille_sur_elle_meme(Ep,Eb,P0,A_cable,g_poutre,y_arr,delta_sigma_frottement_arr,delta_Sigma_recule_arr,poutre_nette,L,4)
  
    effet_dalle_sur_premiere_famille = get_effet_dalle_sur_premiere_famille_(Ep,Eb,g_dalle,g_pre_dalle,y_arr,poutre_nette,L,4)
    
    effet_complement_sur_premiere_famille =  get_effet_complement_sur_premiere_famille_(Ep,Eb,g_complement,y_arr,poutre_nette,L,4)
  
    delta_sigma_racc_arr = np.array([
      effet_premiere_famille[8],
      effet_dalle_sur_premiere_famille[3],
      effet_complement_sur_premiere_famille[3],

    ])

    sigma_sup,S_bare_c=  verification_contrainte_a_28_jours(P0,A_cable,effet_premiere_famille,delta_sigma_frottement_arr,delta_Sigma_recule_arr)
 
    delta_sigma_retrait,delta_sigma_retrait_pd=  get_retrait_béton(poutre_nette,poutre_nette_dalle,L,Ep)

    sigma_relaxation,u_relaxation,delta_sigma_relax = get_relaxation_des_armatures(P0,A_cable,fprg,delta_sigma_frottement_arr,delta_Sigma_recule_arr,effet_premiere_famille,effet_dalle_sur_premiere_famille,effet_complement_sur_premiere_famille)
    
    delta_sigma_fluage = np.array([80.90,	100.90,	131.95,	128.71,	171.52,	147.53,	137.58])
    
    #resume resulat :
    
    #instantane
    delta_sigma_frottement = np.average(delta_sigma_frottement_arr,axis=0)
    delta_Sigma_recule = np.average(delta_Sigma_recule_arr,axis=0)
    delta_Sigma_effet_premiere_famille = effet_premiere_famille[8]
    delta_Sigma_effet_dalle_sur_premiere_famille =effet_dalle_sur_premiere_famille[3]
    delta_Sigma_effet_complement_sur_premiere_famille = effet_complement_sur_premiere_famille[3]

    delta_sigma_insta= np.array([
      delta_sigma_frottement,
      delta_Sigma_recule,
      delta_Sigma_effet_premiere_famille,
      delta_Sigma_effet_dalle_sur_premiere_famille,
      delta_Sigma_effet_complement_sur_premiere_famille,

    ])
    #deferer 
    delta_sigma_diff = np.array([
      delta_sigma_retrait,
      delta_sigma_relax,
      delta_sigma_fluage
    ])
    

    #some insta :
    some_insta = np.sum(delta_sigma_insta,axis=0)
    some_diff   = delta_sigma_retrait +((5/6)*delta_sigma_relax)+delta_sigma_fluage

    delta_sigma_some = np.around(some_insta+some_diff,3)

    #FUSEAU DE PASSAGE 
    fuseau =  get_fuseau_de_passage(alpha_arr,y_arr,P0,A_cable,delta_sigma_some,poutre_homogene_dalle,poutre_nette_dalle)
    
    
    
    print(np.around(effet_premiere_famille[1],3))

  
    

    
    
   

    
  
    
  
 





    
    
    
  
  


    
    
    




    

    return render(request,"precontrainte/precontrainte_home.html")
    
    
    


 






    
def precontrainte_add(request):
    pass
def precontrainte_detail(request):
    pass

