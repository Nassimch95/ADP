from django.shortcuts import render, get_object_or_404, redirect, reverse
import numpy as np
import pandas  as pd
from scipy.optimize import fsolve
from scipy.integrate import quad
from cart.models import  Cart
from .guyonmassonet import u0_teta1,u1_teta1,u0_teta2,u1_teta2,u0_3teta1,u0_3teta2,u1_3teta1,u1_3teta2
import math
from .forms import Add_platelage_form
from .models import platelage

def interpolation_u(k1,k2,teta,teta_1,teta_2):
    k_array =[]
    
    
    for x in range(5):
        k_row = np.array([])
        for y in range(9):
            k = round(k1[x,y] +((k2[x,y]-k1[x,y])*((teta-teta_1)/(teta_2-teta_1))),4)
            k_row = np.append(k_row,k) 
        
        k_array.append(k_row)
    
    return np.array(k_array)


def interpolation_u_alpha(k1,k2,teta,alpha):
    k_array =[]
    exp = 1-math.exp((0.065-0.671)/0.563)
    for x in range(5):
        k_row = np.array([])
        for y in range(9):
            k = round(k1[x,y] +((k2[x,y]-k1[x,y])*(alpha**(exp))),4)
            k_row = np.append(k_row,k) 
        
        k_array.append(k_row)
    
    return np.array(k_array)

def u_alpha_function(k_alpha_active_arr,b):
    K_ALPHA_FUNCTION = []
    x = np.array([-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1])*b
    for y in k_alpha_active_arr:
        k_alpha_function = np.polyfit(x, y, 8)
        K_ALPHA_FUNCTION.append(k_alpha_function)

    return np.array(K_ALPHA_FUNCTION)

# u max G  
def u_alpha_G(functions):
    u_G_p =[]
    u_G_n =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        
        x1 = -5.065
        x2 = 5.065
        
        umax, err = quad(u,x1,x2)
        if umax >=0:
            u_G_p.append(round(np.sum(umax),3))
            u_G_n.append(0)
        else :
            u_G_n.append(round(np.sum(umax),3))
            u_G_p.append(0)
            
        
    return u_G_p,u_G_n
 
# u max pour charge A
def u_alpha_A_gauche(functions):
    u_A_gp =[]
    u_A_gn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = -3.815
        x2 = x1 + 0.01
        while x2 <= -0.315 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        
        u_A_gp.append(round(np.sum(Umax_positive),3))
        u_A_gn.append(round(np.sum(Umax_negative),3))
    return u_A_gp,u_A_gn
     
def u_alpha_A_droite(functions):
    u_A_dp =[]
    u_A_dn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = -0.315
        x2 = x1 + 0.01
        while x2 <= +3.185 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        u_A_dp.append(round(np.sum(Umax_positive),3))
        u_A_dn.append(round(np.sum(Umax_negative),3))
        
    return  u_A_dp,u_A_dn
   
def u_alpha_A_deux_voies(functions):
    u_A_dvp =[]
    u_A_dvn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = -3.185
        x2 = x1 + 0.01
        while x2 <= +3.185 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        u_A_dvp.append(round(np.sum(Umax_positive),3))
        u_A_dvn.append(round(np.sum(Umax_negative),3))
        
    return u_A_dvp,u_A_dvn

# u max pour charge Bc 

   

def u_alpha_Bc_gauche(functions):
    u_Bc_vgp=[]
    u_Bc_vgn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.565 # disposition transversale systeme Bc 
        x2= x1 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x2 <=-0.565:
 
            u1 =u(x1)
            u2 =u(x2)
            umax = (u1+u2)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.1
            x2 =x2 +0.1

        u_Bc_vgp.append(round(np.amax(Umax_positive),3))
        u_Bc_vgn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bc_vgp,u_Bc_vgn
def u_alpha_Bc_droite(functions):
    u_Bc_vdp=[]
    u_Bc_vdn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-0.065 # disposition transversale systeme Bc 
        x2= x1 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x2 <=2.935:
 
            u1 =u(x1)
            u2 =u(x2)
            umax = (u1+u2)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.1
            x2 =x2 +0.1

        u_Bc_vdp.append(round(np.amax(Umax_positive),3))
        u_Bc_vdn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bc_vdp,u_Bc_vdn
def u_alpha_Bc_deux_voies(functions):
    u_Bc_dvp=[]
    u_Bc_dvn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.565 # disposition transversale systeme Bc 
        x2= x1 +2
        x3= x2 +0.5
        x4= x3 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x4 <=2.935:
 
            u1 =u(x1)
            u2 =u(x2)
            u3 =u(x3)
            u4 =u(x4)
            umax = (u1+u2+u3+u4)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.01
            x2 =x2 +0.01
            x3 =x3 +0.01
            x4 =x4 +0.01

        u_Bc_dvp.append(round(np.amax(Umax_positive),3))
        u_Bc_dvn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bc_dvp,u_Bc_dvn

# umax pour Bt 
def u_alpha_Bt_gauche(functions):
    u_Bt_vgp=[]
    u_Bt_vgn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.315 # disposition transversale systeme Bc 
        x2= x1 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x2 <=-0.815:
 
            u1 =u(x1)
            u2 =u(x2)
            umax = (u1+u2)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.1
            x2 =x2 +0.1

        u_Bt_vgp.append(round(np.amax(Umax_positive),3))
        u_Bt_vgn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bt_vgp,u_Bt_vgn
def u_alpha_Bt_droite(functions):
    u_Bt_vdp=[]
    u_Bt_vdn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-0.185 # disposition transversale systeme Bc 
        x2= x1 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x2 <=2.685:
 
            u1 =u(x1)
            u2 =u(x2)
            umax = (u1+u2)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.1
            x2 =x2 +0.1

        u_Bt_vdp.append(round(np.amax(Umax_positive),3))
        u_Bt_vdn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bt_vdp,u_Bt_vdn
def u_alpha_Bt_deux_voies(functions):
    u_Bt_dvp=[]
    u_Bt_dvn=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.315 # disposition transversale systeme Bc 
        x2= x1 +2
        x3= x2 +0.5
        x4= x3 +2
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x4 <=2.685:
 
            u1 =u(x1)
            u2 =u(x2)
            u3 =u(x3)
            u4 =u(x4)
            umax = (u1+u2+u3+u4)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.01
            x2 =x2 +0.01
            x3 =x3 +0.01
            x4 =x4 +0.01

        u_Bt_dvp.append(round(np.amax(Umax_positive),3))
        u_Bt_dvn.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Bt_dvp,u_Bt_dvn

# umax Br 

def u_alpha_Br(functions):
    u_Br_p=[]
    u_Br_n=[]
    
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-4.315 # disposition transversale systeme Bc 
       
        
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x1 <=3.685:
 
            u1 =u(x1)
           
            umax = (u1)
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            x1 =x1 +0.1
           

        u_Br_p.append(round(np.amax(Umax_positive),3))
        u_Br_n.append(round(np.amin(Umax_negative),3))
            
        
        
    
    return u_Br_p,u_Br_n

#umax Mc120

def u_alpha_mc120(functions):
    u_mc120_p=[]
    u_mc120_n=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.815
        x2= x1 +1
        x3= x2+2.3
        x4= x3+1

        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x4 <=3.185:
 
            res1, err = quad(u, x1, x2) 
            res2, err = quad(u, x3, x4)
            umax  = res1+res2
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            
            
            x1 =x1 +0.01
            x2 =x2 +0.01
            x3 = x3 +0.01
            x4 = x4 +0.01
            
        
        u_mc120_p.append(round(np.amax(Umax_positive),3))
        u_mc120_n.append(round(np.amin(Umax_negative),3))
    
    return u_mc120_p,u_mc120_n

def u_alpha_D240(functions):
    u_D240_p=[]
    u_D240_n=[]
    for function in functions:
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]

        x1 =-3.815
        x2= x1 +3.2
       

        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
      
        
        while x2 <=3.185:
 
            res1, err = quad(u, x1, x2) 
            
            umax  = res1
            if umax >=0:
                Umax_positive= np.append(Umax_positive,umax)
                Umax_negative= np.append(Umax_negative,0)
            else :
                Umax_positive= np.append(Umax_positive,0)
                Umax_negative= np.append(Umax_negative,umax)

            
            
            x1 =x1 +0.01
            x2 =x2 +0.01
           
            
        
        u_D240_p.append(round(np.amax(Umax_positive),3))
        u_D240_n.append(round(np.amin(Umax_negative),3))
    
    return u_D240_p,u_D240_n


# Umax Qtr
def u_alpha_Qtr_gauche(functions):
    u_Qtr_gp =[]
    u_Qtr_gn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = -5.065
        x2 = x1 + 0.01
        while x2 <= -4.315 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        
        u_Qtr_gp.append(round(np.sum(Umax_positive),3))
        u_Qtr_gn.append(round(np.sum(Umax_negative),3))
    return u_Qtr_gp,u_Qtr_gn

def u_alpha_Qtr_droite(functions):
    u_Qtr_dp =[]
    u_Qtr_dn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = 3.685
        x2 = x1 + 0.01
        while x2 <=5.065 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        
        u_Qtr_dp.append(round(np.sum(Umax_positive),3))
        u_Qtr_dn.append(round(np.sum(Umax_negative),3))
    return u_Qtr_dp,u_Qtr_dn

def u_alpha_Qtr_deux_voies(functions):
    u_Qtr_dvp =[]
    u_Qtr_dvn =[]
    for function in functions:
        a = function[0]
        b = function[1]
        c = function[2]
        d = function[3]
        e = function[4]
        f = function[5]
        g = function[6]
        h = function[7]
        l = function[8]
        def u(x):
            return  a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x  + l
        Umax_positive = np.array([])
        Umax_negative = np.array([])
        x1 = 3.685
        x2 = x1 + 0.01
        while x2 <=5.065 :
            umax, err = quad(u,x1,x2)
            if umax >=0:
                Umax_positive = np.append(Umax_positive,umax)
            else :
                Umax_negative = np.append(Umax_negative,umax)
                
            x1 =x1+0.01
            x2 =x2+0.01
        
        u_Qtr_dvp.append(round(np.sum(Umax_positive),3))
        u_Qtr_dvn.append(round(np.sum(Umax_negative),3))
    return u_Qtr_dvp,u_Qtr_dvn


def combi_elu_AB(M):
    ELU_AB =np.array([])
    for x in M:
        elu_AB = 1.35*x[0]+ 1.6*(np.amax(x[1:8])+ np.amax(x[10:12]))
        ELU_AB=np.append(ELU_AB,elu_AB)
    
    return ELU_AB

def combi_elu_militaire(M):
    ELU_militaire =np.array([])
    for x in M:
        elu_militaire = 1.35*( x[0]+ np.amax(x[8:10]) )
        ELU_militaire=np.append(ELU_militaire,elu_militaire)
    
    return ELU_militaire


def combi_els_AB(M):
    ELS_AB =np.array([])
    for x in M:
        els_AB = x[0]+ 1.2*(np.amax(x[1:8])+ np.amax(x[10:12]))
        ELS_AB=np.append(ELS_AB,els_AB)
    
    return ELS_AB

def combi_els_militaire(M):
    ELS_militaire =np.array([])
    for x in M:
        els_militaire =  x[0]+ np.amax(x[8:10]) 
        ELS_militaire=np.append(ELS_militaire,els_militaire)
    
    return ELS_militaire

#flexion localisé :

def get_lx_ly(h,tan,b_ame,v,L):
    a_lx = (h)*tan   # math.tan(51.63)=1.263
    y_lx = a_lx + (b_ame/2)
    Lx= round((v-(2*y_lx))*0.01,2)
    Ly = L 
    ro =Lx/Ly
    return a_lx,y_lx,Lx,Ly,ro


def G_ET_A_LOCALISE(Lx,Ly,g_dalle,g_revetement,b_dalle,b_revetement):
    Qg= (g_dalle/b_dalle) + (g_revetement/b_revetement)
    Qa= 0.922

    MOX_G  =  (Qg*(Lx**2))/8
    MOX_A  =  (Qa*(Lx**2))/8

    M_APPUI_G = -0.5*MOX_G
    M_TRAVEE_G = 0.85*MOX_G

    M_APPUI_A = -0.5*MOX_A
    M_TRAVEE_A = 0.85*MOX_A

    Tx_G =  Qg *(Lx*Ly)/((2*Ly)+Lx)
    Ty_G =  Qg * (Lx*Ly)/((2*Ly)+Ly)

    Tx_A =  Qa *(Lx*Ly)/((2*Ly)+Lx)
    Ty_A =  Qa * (Lx*Ly)/((2*Ly)+Ly)

    G_ET_A_LOCALISE_arr = np.array([
       [ M_APPUI_G,M_APPUI_A],
       [M_TRAVEE_G,M_TRAVEE_A],
       [Tx_G ,Tx_A],
       [Ty_G,Ty_A],

    ])

    return G_ET_A_LOCALISE_arr
def B_Mc120_LOCALISE(Lx):
    Tx =  np.array([])
    Ty =  np.array([])
    coef = np.array([1.137, 1.137*1.1, 1.137*1,1.1843 ])
    U0 = np.array([0.6, 0.25, 0.6, 1])
    V0 = np.array([0.3, 0.25, 0.25 ,6.1])
    U  = np.array([0.97 , 0.62, 0.97, 1.37])
    V  =  np.array([0.67 ,0.62 ,0.62 ,6.47])
    Ulx = np.around(U/Lx,3)
    Vlx = np.around(V/Lx,3)
    M1 = np.array([0.083,0.111,0.085,0.040])
    M2  = np.array([0.028,0.043,0.033,0.0009])
    Q   = np.array([10,6,8,55])
    MOX  = Q*(M1+0.15*M2)*coef

    
   
    Ma = -0.5*MOX
    Mt = 0.85*MOX

    for x in range(4):
        if U[x]>V[x]:
            tx =Q[x]/(3*U[x])
            ty = Q[x]/(2*U[x]+V[x])
            Tx= np.append(Tx,tx)
            Ty= np.append(Ty,ty)
        else :
            
            tx = Q[x]/(2*V[x]+U[x])
            ty =Q[x]/(3*V[x])
            Tx= np.append(Tx,tx)
            Ty= np.append(Ty,ty)

    
    B_Mc120_LOCALISE_arr =np.array([
        U0,
        V0,
        U,
        V,
        Ulx,
        Vlx,
        M1,
        M2,
        Q,
        MOX,
        Ma,
        Mt,
        Tx*coef,
        Ty*coef
    ])


    return B_Mc120_LOCALISE_arr

def ELU_LOCALISE_MOMENT(G_ET_A_LOCALISE_arr,B_Mc120_LOCALISE_arr):
    M_APPUI_B_Mc120 = B_Mc120_LOCALISE_arr[10]
    M_TRAVEE_B_Mc120 = B_Mc120_LOCALISE_arr[11]

    M_APPUI_G_ET_A  = G_ET_A_LOCALISE_arr[0]
    M_TRAVEE_G_ET_A = G_ET_A_LOCALISE_arr[1]

    elu_appui_GB = 1.35*M_APPUI_G_ET_A[0]+1.6*np.amin(M_APPUI_B_Mc120[0:3])
    elu_trave_GB = 1.35*M_TRAVEE_G_ET_A[0]+1.6*np.amax(M_TRAVEE_B_Mc120[0:3])

    elu_appui_Gmc120 = 1.35*(M_APPUI_G_ET_A[0]+M_APPUI_B_Mc120[3])
    elu_trave_Gmc120 = 1.35*(M_TRAVEE_G_ET_A[0]+M_TRAVEE_B_Mc120[3])

    ELU_LOCALISE_M  = np.array([
        [elu_appui_GB,elu_trave_GB],
        [elu_appui_Gmc120,elu_trave_Gmc120 ]
    ])

    return ELU_LOCALISE_M
    
            

def ELS_LOCALISE_MOMENT(G_ET_A_LOCALISE_arr,B_Mc120_LOCALISE_arr):
    M_APPUI_B_Mc120 = B_Mc120_LOCALISE_arr[10]
    M_TRAVEE_B_Mc120 = B_Mc120_LOCALISE_arr[11]

    M_APPUI_G_ET_A  = G_ET_A_LOCALISE_arr[0]
    M_TRAVEE_G_ET_A = G_ET_A_LOCALISE_arr[1]

    els_appui_GB = M_APPUI_G_ET_A[0]+1.2*np.amin(M_APPUI_B_Mc120[0:3])
    els_trave_GB = M_TRAVEE_G_ET_A[0]+1.2*np.amax(M_TRAVEE_B_Mc120[0:3])

    els_appui_Gmc120 = M_APPUI_G_ET_A[0]+M_APPUI_B_Mc120[3]
    els_trave_Gmc120 = M_TRAVEE_G_ET_A[0]+M_TRAVEE_B_Mc120[3]

    ELS_LOCALISE_M  = np.array([
        [els_appui_GB,els_trave_GB],
        [els_appui_Gmc120,els_trave_Gmc120 ]
    ])

    return ELS_LOCALISE_M
    
def Max_ELU_ELS_LOCALISE(ELU_LOCALISE_M,ELS_LOCALISE_M):
    elu_max_appui =np.amin(ELU_LOCALISE_M[0:2,0])
    elu_max_trave =np.amax(ELU_LOCALISE_M[0:2,1])
    els_max_appui =np.amin(ELS_LOCALISE_M[0:2,0])
    els_max_trave =np.amax(ELS_LOCALISE_M[0:2,1])

    Max_ELU_ELS_LOCALISE_arr =np.array([

       [elu_max_appui, elu_max_trave ], #elu 
       [els_max_appui ,els_max_trave ], #els

    ])

    return  Max_ELU_ELS_LOCALISE_arr

   
   




def platelage_home(request):
    platelages = platelage.objects.all()
    print(platelages)
    context ={
        'platelages':platelages
    }

    return render(request,'platelage/platelage_home.html',context)


def platelage_add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_platelage_form(request.POST)

        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            repartition_transversale= form.cleaned_data['R_transversale']
    
            u0 = interpolation_u(u0_teta1,u0_teta2,0.563,0.5,0.6)
            u1 = interpolation_u(u1_teta1,u1_teta2,0.563,0.5,0.6)
            u_alpha = interpolation_u_alpha(u0,u1,0.563,0.122)
            

            functions = u_alpha_function(u_alpha,5.40)
            u_G_p,u_G_n = u_alpha_G(functions)
            u_A_gp,u_A_gn = u_alpha_A_gauche(functions)
            u_A_dp,u_A_dn = u_alpha_A_droite(functions)
            u_A_dvp,u_A_dvn = u_alpha_A_deux_voies(functions)
            u_Bc_vgp,u_Bc_vgn = u_alpha_Bc_gauche(functions)
            u_Bc_vdp,u_Bc_vdn = u_alpha_Bc_droite(functions)
            u_Bc_dvp,u_Bc_dvn = u_alpha_Bc_deux_voies(functions)
            u_Bt_vgp,u_Bt_vgn = u_alpha_Bt_gauche(functions)
            u_Bt_vdp,u_Bt_vdn = u_alpha_Bt_droite(functions)
            u_Bt_dvp,u_Bt_dvn = u_alpha_Bt_deux_voies(functions)
            u_Br_p,u_Br_n = u_alpha_Br(functions)
            u_mc120_p,u_mc120_n = u_alpha_mc120(functions)
            u_D240_p,u_D240_n = u_alpha_D240(functions)
            u_Qtr_gp,u_Qtr_gn= u_alpha_Qtr_gauche(functions)
            u_Qtr_dp,u_Qtr_dn= u_alpha_Qtr_droite(functions)
            u_Qtr_dvp  = ( np.array(u_Qtr_gp) + np.array(u_Qtr_dp) ).tolist()
            u_Qtr_dvn  =  ( np.array(u_Qtr_gn) + np.array(u_Qtr_dn) ).tolist()

            
            matrice_teta_p =np.array([
                u_G_p,
                u_A_dp,
                u_A_dvp,
                u_Bc_vdp,
                u_Bc_dvp,
                u_Bt_vdp,
                u_Bt_dvp,
                u_Br_p,
                u_mc120_p,
                u_D240_p,
                u_Qtr_dp,
                u_Qtr_dvp
            

                ])
            
            matrice_teta_n =np.array([
                u_G_n,
                u_A_dn,
                u_A_dvn,
                u_Bc_vdn,
                u_Bc_dvn,
                u_Bt_vdn,
                u_Bt_dvn,
                u_Br_n,
                u_mc120_n,
                u_D240_n,
                u_Qtr_dn,
                u_Qtr_dvn

                ])

            # 3teta
            u0_3teta = interpolation_u(u0_3teta1,u0_3teta2,1.689,1.6,1.8)
            u1_3teta = interpolation_u(u1_3teta1,u1_3teta2,1.689,1.6,1.8)
            u_alpha_3teta = interpolation_u_alpha(u0_3teta,u1_3teta ,1.689,0.122)
            functions_3teta = u_alpha_function(u_alpha_3teta,5.40)
        
            u_G_p_3teta,u_G_n_3teta = u_alpha_G(functions_3teta)
            u_A_gp_3teta ,u_A_gn_3teta = u_alpha_A_gauche(functions_3teta)
            u_A_dp_3teta, u_A_dn_3teta = u_alpha_A_droite(functions_3teta)
            u_A_dvp_3teta, u_A_dvn_3teta = u_alpha_A_deux_voies(functions_3teta)
            u_Bc_vgp_3teta,u_Bc_vgn_3teta = u_alpha_Bc_gauche(functions_3teta)
            u_Bc_vdp_3teta,u_Bc_vdn_3teta = u_alpha_Bc_droite(functions_3teta)
            u_Bc_dvp_3teta,u_Bc_dvn_3teta = u_alpha_Bc_deux_voies(functions_3teta)
            u_Bt_vgp_3teta,u_Bt_vgn_3teta = u_alpha_Bt_gauche(functions_3teta)
            u_Bt_vdp_3teta,u_Bt_vdn_3teta = u_alpha_Bt_droite(functions_3teta)
            u_Bt_dvp_3teta,u_Bt_dvn_3teta = u_alpha_Bt_deux_voies(functions_3teta)
            u_Br_p_3teta, u_Br_n_3teta = u_alpha_Br(functions_3teta)
            u_mc120_p_3teta,u_mc120_n_3teta = u_alpha_mc120(functions_3teta)
            u_D240_p_3teta,u_D240_n_3teta = u_alpha_D240(functions_3teta)
            u_Qtr_gp_3teta,u_Qtr_gn_3teta= u_alpha_Qtr_gauche(functions_3teta)
            u_Qtr_dp_3teta,u_Qtr_dn_3teta= u_alpha_Qtr_droite(functions_3teta)
            u_Qtr_dvp_3teta  = ( np.array(u_Qtr_gp_3teta) + np.array(u_Qtr_dp_3teta) ).tolist()
            u_Qtr_dvn_3teta  =  ( np.array(u_Qtr_gn_3teta) + np.array(u_Qtr_dn_3teta) ).tolist()

            matrice_3teta_p =np.array([
                u_G_p_3teta,
                u_A_dp_3teta,
                u_A_dvp_3teta,
                u_Bc_vdp_3teta,
                u_Bc_dvp_3teta,
                u_Bt_vdp_3teta,
                u_Bt_dvp_3teta,
                u_Br_p_3teta,
                u_mc120_p_3teta,
                u_D240_p_3teta,
                u_Qtr_dp_3teta,
                u_Qtr_dvp_3teta
            

                ])

            matrice_3teta_n =np.array([
                u_G_n_3teta,
                u_A_dn_3teta,
                u_A_dvn_3teta,
                u_Bc_vdn_3teta,
                u_Bc_dvn_3teta,
                u_Bt_vdn_3teta,
                u_Bt_dvn_3teta,
                u_Br_n_3teta,
                u_mc120_n_3teta,
                u_D240_n_3teta,
                u_Qtr_dn_3teta,
                u_Qtr_dvn_3teta,
                ])
            
            
            
            pm =np.array([
                [2.8269],
                [1.1739],
                [1.1739],
                [1.3412],
                [1.3412],
                [0.7986],
                [0.7986],
                [0.5000],
                [2.7238],
                [3.4253],
                [0.1910],
                [0.1910]
            ])

            coef =np.array([
                [1],
                [1],
                [1],
                [1.137*1.1],
                [1.137*1.1],
                [1.137*1.0],
                [1.137*1.0],
                [1.137],
                [1.1843],
                [1],
                [1],
                [1]
            ])

            M_P = np.transpose(np.around(2*5.4*10**-4*pm*coef*( (matrice_teta_p+matrice_3teta_p)/2 ),decimals=4))
            ELU_AB_P = combi_elu_AB(M_P)
            ELU_militaire_P = combi_elu_militaire(M_P)
            ELS_AB_P = combi_els_AB(M_P)
            ELS_militaire_P = combi_els_militaire(M_P)
            
            
            combinaison_arr_P = np.array([
                ELU_AB_P ,
                ELU_militaire_P ,
                ELS_AB_P  ,
                ELS_militaire_P ,

            ])

           

            #M- :
            M_N = np.transpose(np.around(2*5.4*10**-4*pm*coef*( (matrice_teta_n+matrice_3teta_n)/2 ),decimals=4))
            ELU_AB_N = combi_elu_AB(M_N)
            ELU_militaire_N = combi_elu_militaire(M_N)
            ELS_AB_N = combi_els_AB(M_N)
            ELS_militaire_N = combi_els_militaire(M_N)

            combinaison_arr_N = np.array([
                ELU_AB_N ,
                ELU_militaire_N ,
                ELS_AB_N  ,
                ELS_militaire_N ,

            ])

            M_Max_P = np.array([
                np.amax(combinaison_arr_P[0:2]),
                np.amax(combinaison_arr_P[2:4])
            ])

            M_Max_N = np.array([
                np.amin(combinaison_arr_N[0:2]),
                np.amin(combinaison_arr_N[2:4])
            ])
            

            #flexion localisé:
            a_lx,y_lx,Lx,Ly,ro = get_lx_ly(27.4,1.263,25,180,40)
            G_ET_A_LOCALISE_arr = G_ET_A_LOCALISE(Lx,Ly,6.3312,1.4080,10.13,8)
            B_Mc120_LOCALISE_arr = B_Mc120_LOCALISE(Lx)
           
            ELU_LOCALISE_M = ELU_LOCALISE_MOMENT(G_ET_A_LOCALISE_arr,B_Mc120_LOCALISE_arr)
            ELS_LOCALISE_M = ELS_LOCALISE_MOMENT(G_ET_A_LOCALISE_arr,B_Mc120_LOCALISE_arr)

            Max_ELU_ELS_LOCALISE_arr = Max_ELU_ELS_LOCALISE(ELU_LOCALISE_M,ELS_LOCALISE_M)

         
        
     

  
   

    
    
  
           
        
         
            


            
            
           

            
            
            
            form.instance.u0 =u0.tolist()
            form.instance.u1 =u1.tolist()
            form.instance.ua =u_alpha.tolist()

            form.instance.u0_3teta =u0_3teta.tolist()
            form.instance.u1_3teta =u1_3teta.tolist()
            form.instance.ua_3teta =u_alpha_3teta.tolist()

            form.instance.matrice_teta_p =matrice_teta_p.tolist()
            form.instance.matrice_teta_n =matrice_teta_n.tolist()
            form.instance.matrice_3teta_p =matrice_3teta_p.tolist()
            form.instance.matrice_3teta_n =matrice_3teta_n.tolist()

            form.instance.pm =pm.tolist()
            form.instance.M_P =M_P.tolist()
            form.instance.combinaison_arr_P =combinaison_arr_P.tolist()
            form.instance.M_N= M_N.tolist()
            form.instance.combinaison_arr_N =combinaison_arr_N.tolist()
            form.instance.M_Max_P =M_Max_P.tolist()
            form.instance.M_Max_N =M_Max_N.tolist()

            #moment localisé 
            a_lx,y_lx,Lx,Ly,ro
            form.instance.a_lx =a_lx
            form.instance.y_lx =y_lx
            form.instance.Lx =Lx
            form.instance.Ly =Ly 
            form.instance.ro =ro
            form.instance.G_ET_A_LOCALISE_arr = G_ET_A_LOCALISE_arr.tolist()
            form.instance.B_Mc120_LOCALISE_arr =B_Mc120_LOCALISE_arr.tolist()
            form.instance.ELU_LOCALISE_M =ELU_LOCALISE_M.tolist()
            form.instance.ELS_LOCALISE_M =ELS_LOCALISE_M.tolist()
            form.instance.Max_ELU_ELS_LOCALISE_arr =Max_ELU_ELS_LOCALISE_arr.tolist()





            form.save()
            return redirect(reverse("platelage_detail", kwargs={
                'slug': form.instance.slug
            }))
            
           

            

           
           
    else:
        form = Add_platelage_form()
            


    
   

  
    return render(request,'platelage/platelage_add.html',{'form': form})



def platelage_detail(request,slug):

    platelage_detail = get_object_or_404(platelage,slug=slug)

    df_u0 = pd.DataFrame(platelage_detail.u0,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_u0 = df_u0.to_html()

    df_u1 = pd.DataFrame(platelage_detail.u1,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_u1 = df_u1.to_html()

    df_ua = pd.DataFrame(platelage_detail.ua,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_ua = df_ua.to_html()

    #3teta

    df_u0_3teta = pd.DataFrame(platelage_detail.u0_3teta,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_u0_3teta = df_u0_3teta.to_html()

    df_u1_3teta = pd.DataFrame(platelage_detail.u1_3teta,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_u1_3teta = df_u1_3teta.to_html()

    df_ua_3teta = pd.DataFrame(platelage_detail.ua_3teta,index=['0' ,'b/4' ,'b/2' ,'3b/4', 'b'], columns=['-b', '-3b/4', '-b/2', '-b/4', '0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_ua_3teta = df_ua_3teta.to_html()
    
    df_matrice_teta_p = pd.DataFrame(platelage_detail.matrice_teta_p,index=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'], columns=['0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_matrice_teta_p = df_matrice_teta_p.to_html()
    df_matrice_teta_n = pd.DataFrame(platelage_detail.matrice_teta_n,columns=['0' ,'b/4' ,'b/2' ,'3b/4','b'],index=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'],) 
    html_matrice_teta_n = df_matrice_teta_n.to_html()

    df_matrice_3teta_p = pd.DataFrame(platelage_detail.matrice_3teta_p,index=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'], columns=['0' ,'b/4' ,'b/2' ,'3b/4','b']) 
    html_matrice_3teta_p = df_matrice_3teta_p.to_html()
    df_matrice_3teta_n = pd.DataFrame(platelage_detail.matrice_3teta_n,columns=['0' ,'b/4' ,'b/2' ,'3b/4','b'],index=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'],) 
    html_matrice_3teta_n = df_matrice_3teta_n.to_html()

    df_pm= pd.DataFrame(platelage_detail.pm,index=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'],columns=['pm']).transpose() 
    html_pm= df_pm.to_html()

    df_M_P= pd.DataFrame(platelage_detail.M_P,columns=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'], index=['0' ,'b/4' ,'b/2' ,'3b/4','b']).transpose()
    html_M_P= df_M_P.to_html()

    df_M_N= pd.DataFrame(platelage_detail.M_N,columns=['G' ,'A 1V' ,'A 2V' ,'Bc 1V', 'Bc 2V','Bt 1V', 'Bt 2V','Br','Mc120','D240','Qtr D','Qtr D+G'], index=['0' ,'b/4' ,'b/2' ,'3b/4','b']).transpose()
    html_M_N=df_M_N.to_html()

    df_combinaison_arr_P= pd.DataFrame(platelage_detail.combinaison_arr_P,columns=['0' ,'b/4' ,'b/2' ,'3b/4','b'],index=['ELU AB','ELU Militaire','ELS AB','ELS Militaire',])
    html_combinaison_arr_P=df_combinaison_arr_P.to_html()

    df_combinaison_arr_N= pd.DataFrame(platelage_detail.combinaison_arr_N,columns=['0' ,'b/4' ,'b/2' ,'3b/4','b'],index=['ELU AB','ELU Militaire','ELS AB','ELS Militaire',])
    html_combinaison_arr_N=df_combinaison_arr_N.to_html()

    df_M_Max_P= pd.DataFrame(platelage_detail.M_Max_P,columns=['M+' ,],index=['ELU ','ELS ',])
    html_M_Max_P=df_M_Max_P.to_html()

    df_M_Max_N= pd.DataFrame(platelage_detail.M_Max_N,columns=['M-' ,],index=['ELU ','ELS ',])
    html_M_Max_N=df_M_Max_N.to_html()

    #flexion localisé :
    df_lx_ly_arr= pd.DataFrame([platelage_detail.a_lx,platelage_detail.y_lx,platelage_detail.Lx,platelage_detail.Ly,platelage_detail.ro],index=['a' ,'y','Lx','Ly','ro'],columns=['valeur'])
    html_lx_ly_arr= df_lx_ly_arr.to_html()

    df_G_ET_A_LOCALISE_arr= pd.DataFrame(platelage_detail.G_ET_A_LOCALISE_arr,columns=['G' , 'A'],index=['M appui','M travée', 'Tx','Ty'])
    html_G_ET_A_LOCALISE_arr= df_G_ET_A_LOCALISE_arr.to_html()

    df_B_Mc120_LOCALISE_arr= pd.DataFrame(platelage_detail.B_Mc120_LOCALISE_arr,columns=['Br' , 'Bc', 'Bt','Mc120'],index=['U0','V0', 'U','V','U/Lx','U/Lx','M1','M2','Q','MOX','Ma','Mt','Tx','Ty'])
    html_B_Mc120_LOCALISE_arr= df_B_Mc120_LOCALISE_arr.to_html()
    
    df_ELU_LOCALISE_M= pd.DataFrame(platelage_detail.ELU_LOCALISE_M,columns=['Ma' , 'Mt',],index=['1.35G+1.6*max(B)','1.35(G+mc120)', ])
    html_ELU_LOCALISE_M= df_ELU_LOCALISE_M.to_html()

    df_ELS_LOCALISE_M= pd.DataFrame(platelage_detail.ELS_LOCALISE_M,columns=['Ma' , 'Mt',],index=['G+1.2*max(B)','G+mc120', ])
    html_ELS_LOCALISE_M= df_ELS_LOCALISE_M.to_html()

    df_Max_ELU_ELS_LOCALISE_arr= pd.DataFrame(platelage_detail.Max_ELU_ELS_LOCALISE_arr,columns=['Ma' , 'Mt',],index=['ELU','ELS', ])
    html_Max_ELU_ELS_LOCALISE_arr= df_Max_ELU_ELS_LOCALISE_arr.to_html()







    context ={
        'platelage_detail': platelage_detail,
        'html_u0':html_u0,
        'html_u1':html_u1,
        'html_ua':html_ua,

        'html_u0_3teta':html_u0_3teta,
        'html_u1_3teta':html_u1_3teta,
        'html_ua_3teta':html_ua_3teta,
        'html_matrice_teta_p':html_matrice_teta_p,
        'html_matrice_teta_n':html_matrice_teta_n,

        'html_matrice_3teta_p':html_matrice_3teta_p,
        'html_matrice_3teta_n':html_matrice_3teta_n,
        'html_pm':html_pm,
        'html_M_P': html_M_P,
        'html_M_N': html_M_N,
        'html_combinaison_arr_P':html_combinaison_arr_P,
        'html_combinaison_arr_N':html_combinaison_arr_N,
        'html_M_Max_P' :html_M_Max_P,
        'html_M_Max_N':html_M_Max_N,

        # flexion localisé :
        'html_lx_ly_arr':html_lx_ly_arr,
        'html_G_ET_A_LOCALISE_arr': html_G_ET_A_LOCALISE_arr,
        'html_B_Mc120_LOCALISE_arr':html_B_Mc120_LOCALISE_arr,
        'html_ELU_LOCALISE_M' :html_ELU_LOCALISE_M,
        'html_ELS_LOCALISE_M' :html_ELS_LOCALISE_M,
        'html_Max_ELU_ELS_LOCALISE_arr' : html_Max_ELU_ELS_LOCALISE_arr,


    }

    return render(request,'platelage/platelage_detail.html',context)