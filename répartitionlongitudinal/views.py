from django.shortcuts import render, get_object_or_404, redirect, reverse
from.models import repartition_longitudinal
from cart.models import  Cart
from .forms import Add_repartition_longitudinal_form
import numpy as np
import pandas as pd

# Create your views here.

def Mbc_Critique(L):
    P= np.array([3, 6, 6, 3, 6, 6])
    D= np.array([0, 4.5, 6, 10.5, 15, 16.5])
    R = np.sum(P)
    DR= (np.sum(np.multiply(P,D)))/R
    C = []
    Xc = []
    Xpc =[]
    SPG = []
    RXL = []  # R*X/L
    SPGPK =[]
    CRITIQUE =[]
    DP1PC  = []
    DPCP6  = []
    DEBORDEMENT =[]
    Pi =[] #list  of np array 
    Pi_list=[] #list of array 
    Di =[] #list  of np array 
    Di_list =[] #list of array 
    SPIDI  =[]
    M =[]

    for x in range(2,4):
        c =  abs(DR - D[x])  # distance R et P critique 
        C = np.append(C, c)
        if D[x] > DR:

            xc = (L/2)+(c/2)
            xpc = L-xc
            Xc = np.append(Xc, xc)  # distance  section  critique  et origine 
            Xpc = np.append(Xpc, xpc)
        else :
            xc = (L/2)- (c/2)
            xpc = L-xc
            Xc = np.append(Xc, xc)
            Xpc = np.append(Xpc, xpc)
        
        spg = np.sum(P[:x])            # SOME des P gauche a P critique 
        SPG = np.append(SPG, spg)

        rxl =R*xc/L
        RXL = np.append(RXL, rxl)

        spgpk = spg + P[x]          # SOME des P gauche a P critique  + p critique 
        SPGPK = np.append(SPGPK, spgpk)
        
        if rxl >= spg and rxl <= spgpk:
            critique = "critique"
            CRITIQUE = np.append(CRITIQUE, critique)
            dp1pc = D[x]
            DP1PC = np.append(DP1PC, dp1pc)
            dpcp6 = D[-1]- D[x]
            DPCP6 = np.append(DPCP6, dpcp6)
            if dp1pc < xc and dpcp6 < xpc:
                debordement = 'pas de debordement'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)
                # Pi and Di list are list of np array  so we can multiply between them 
                Pi.append(P[:x])
                Di.append(D[x]-D[:x])
                SPIDI.append(np.sum(Pi[-1] * Di[-1]))
                M.append( (R*xc**2/L) - np.sum(Pi[-1] * Di[-1]) )

                # pi  and di  list of list not list of array  fo storing in database :
                pi =  P[:x].tolist()
                Pi_list.append(pi)
                di = (D[x]-D[:x]).tolist()
                Di_list.append(di)
                

            else :
                debordement = 'il ya un debordement'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)

            


        else :
            critique = 'Non critique'
            CRITIQUE = np.append(CRITIQUE, critique)
           



    


    return R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi_list,Di_list,SPIDI,M

def M_Bt_Critique(L):
    P= np.array([8, 8])
    D= np.array([0, 1.35])
    R = np.sum(P)
    DR= (np.sum(np.multiply(P,D)))/R
    C = []
    Xc = []
    Xpc =[]
    SPG = []
    RXL = []  # R*X/L
    SPGPK =[]
    CRITIQUE =[]
    DP1PC  = []
    DPCP6  = []
    DEBORDEMENT =[]
    Pi =[]
    Pi_list=[] #list of array 
    Di =[]
    Di_list =[] #list  of np array 
    SPIDI  =[]
    M =[]

    for x in range(0,2):
        c =  abs(DR - D[x])  # distance R et P critique 
        C = np.append(C, c)
        if D[x] > DR:

            xc = (L/2)+(c/2)
            xpc = L-xc
            Xc = np.append(Xc, xc)  # distance  section  critique  et origine 
            Xpc = np.append(Xpc, xpc)
        else :
            xc = (L/2)- (c/2)
            xpc = L-xc
            Xc = np.append(Xc, xc)
            Xpc = np.append(Xpc, xpc)
        
        spg = np.sum(P[:x])            # SOME des P gauche a P critique 
        SPG = np.append(SPG, spg)

        rxl =R*xc/L
        RXL = np.append(RXL, rxl)

        spgpk = spg + P[x]          # SOME des P gauche a P critique  + p critique 
        SPGPK = np.append(SPGPK, spgpk)
        
        if rxl >= spg and rxl <= spgpk:
            critique = 'critique'
            CRITIQUE = np.append(CRITIQUE, critique)
            dp1pc = D[x]
            DP1PC = np.append(DP1PC, dp1pc)
            dpcp6 = D[-1]- D[x]
            DPCP6 = np.append(DPCP6, dpcp6)
            if dp1pc < xc and dpcp6 < xpc:
                debordement = 'pas de débordement'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)
                Pi.append(P[:x])
                Di.append(D[x]-D[:x])
                SPIDI.append(np.sum(Pi[-1] * Di[-1]))
                M.append( (R*xc**2/L) - np.sum(Pi[-1] * Di[-1]) )

                # pi  and di  list of list not list of array  fo storing in database :
                pi =  P[:x].tolist()
                Pi_list.append(pi)
                di = (D[x]-D[:x]).tolist()
                Di_list.append(di)

            else :
                debordement = 'il ya  débordement refaire le calcule avec P1 P2 P3 P4'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)

            


        else :
            critique = 'non critique'
            CRITIQUE = np.append(CRITIQUE, critique)
           



    


    return R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi_list,Di_list,SPIDI,M
    

def charge_repartie_sur_L(q,L,x_critique):

    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    M  = np.array([])
    T  = np.array([])
    G  = []

    for x in Li :
        a= x
        b= L-x
        m = 1/2*q*a*b
        M= np.append(M,m)

    for y in Li:
        a= y
        b= L-y 
        Y = 1- (a/L)
        S= np.trapz([Y,0], x=[a,L])
        t = S*q
        T= np.append(T,t)

    
    G.append(M.tolist())
    G.append(T.tolist())

    
    
    return M,T,G


def charge_militaire(q,L,lc,cdmdM,x_critique):

    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    M  = np.array([])
    T  = np.array([])
    for x in Li :
        a= x
        b= L-x
        m1 =1-(a/L)
        m2 = 1-(lc/(2*L))
        m = q*lc*a *m1*m2*cdmdM
        M= np.append(M,m)

    for y in Li :
        a= y
        b= L-y

        if b <= lc :
            y1=1-(a/L)
            S = y1*b/2
            t= S*q*cdmdM
            T= np.append(T,t)

            
            
        if b >lc and b <=(lc+30.5):
            y1=1-(a/L)
            y2 =((b-lc)*y1)/b
            S1= np.trapz([y1,y2], x=[0,lc])
            S2 = 0
            S= S1+S2
            t= S*q*cdmdM
            T= np.append(T,t)
        else:
            if b>(lc+30.5) and b<=(lc+30.5+lc) :
                y1=1-(a/L)
                y2 =((b-lc)*y1)/b
                y3 = ((b-(lc+30.5))*y1)/b
                y4 = 0 
                S1= np.trapz([y1,y2], x=[0,lc])
                S2 =np.trapz([y3,y4], x=[lc+30.5,b])
                S= S1+S2
                t= S*q*cdmdM
                T= np.append(T,t)
            else:
                if b> ((lc+30.5+lc)) :
                    y1=1-(a/L)
                    y2 =((b-lc)*y1)/b
                    y3 = ((b-(lc+30.5))*y1)/b
                    y4 = ((b-(lc+30.5+lc))*y1)/b
                    S1= np.trapz([y1,y2], x=[0,lc])
                    S2 =np.trapz([y3,y4], x=[lc+30.5,lc+30.5+lc])
                    S= S1+S2
                    t= S*q*cdmdM
                    T= np.append(T,t)
    return M,T


def convois_exceptionelle(q,L,lc,x_critique):

    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    M  = np.array([])
    T  = np.array([])
    for x in Li :
        a= x
        b= L-x
        m1 =1-(a/L)
        m2 = 1-(lc/(2*L))
        m = q*lc*a *m1*m2
        M= np.append(M,m)

    for y in Li :
        a= y
        b= L-y

        if b <= lc :
            y1=1-(a/L)
            S = y1*b/2
            t= S*q
            T= np.append(T,t)
        else:
            if b >lc :
                y1=1-(a/L)
                y2 =((b-lc)*y1)/b
                S1= np.trapz([y1,y2], x=[0,lc])
                S2 = 0
                S= S1+S2
                t= S*q
                T= np.append(T,t)
        
                   
    return M,T


def Bt(L,x_critique,cdmdB):

    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    P =np.array([8,8])
    yi_list_for_M =[]
    yi_list_for_T =[]
    M =np.array([])
    T= np.array([])
    for x in range(6) :
        a_m=Li[x] 
        b_m=L-Li[x]  
        y1_m= (a_m*b_m)/L
        y2_m = ((b_m-1.35)*y1_m)/b_m
        yi_m = np.array([y1_m,y2_m])
        yi_list_for_M.append(yi_m)
        m = 2*1*cdmdB* np.sum(P*yi_list_for_M[x])
        M=np.append(M,m)

    for y in range (6):
        a_t=Li[y] 
        b_t=L-Li[y]  
        y1_t= b_t/L
        y2_t = ((b_t-1.35)*y1_t)/b_t
        yi_t = np.array([y1_t,y2_t])
        yi_list_for_T.append(yi_t)
        t = 2*1*cdmdB* np.sum(P*yi_list_for_T[y])
        T =np.append(T,t)

    return M,np.array(yi_list_for_M),T,np.array(yi_list_for_T)


def Br(L,x_critique,cdmdB):

    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    P =10
    yi_list_for_M =[]
    yi_list_for_T =[]
    M =np.array([])
    T= np.array([])
    for x in range(6) :
        a_m=Li[x] 
        b_m=L-Li[x]  
        y1_m= (a_m*b_m)/L
        
        yi_m = np.array([y1_m])
        yi_list_for_M.append(yi_m)
        m = 1*cdmdB* np.sum(P*yi_list_for_M[x])
        M=np.append(M,m)

    for y in range (6):
        a_t=Li[y] 
        b_t=L-Li[y]  
        y1_t= b_t/L
        
        yi_t = np.array([y1_t])
        yi_list_for_T.append(yi_t)
        t = 1*cdmdB* np.sum(P*yi_list_for_T[y])
        T =np.append(T,t)

    return M,np.array(yi_list_for_M),T,np.array(yi_list_for_T)


# moment systeme Bc

def get_p_critique_sense_1(Xc,L,cdmdB):
    P_string = ['P6','P5','P4','P3','P2','P1']
    P = np.array([6,6,3,6,6,3])
    D = np.array([0, 4.5, 6, 10.5, 15, 16.5])
    U = np.array([0, 1.5 ,6, 10.5, 12, 16.5])
    R = np.sum(P)
    CRITIQUE = []
    SPG = []
    RXL = []  # R*X/L
    SPGPK =[]
    Pk =np.array([],dtype=int)
    Z = np.array([])
    Y  =[]
    for x in range (6) :
        spg = np.sum(P[:x])            # SOME des P gauche a P critique 
        SPG = np.append(SPG, spg)

        rxl =R*Xc/L
        RXL = np.append(RXL, rxl)

        spgpk = spg + P[x]          # SOME des P gauche a P critique  + p critique 
        SPGPK = np.append(SPGPK, spgpk)
        
        if rxl >= spg and rxl <= spgpk:
            critique = 'critique'
            CRITIQUE = np.append(CRITIQUE, critique)
            Pk = np.append(Pk, x)
        
        else :
            critique = 'non  critique'
            CRITIQUE = np.append(CRITIQUE, critique)
    
    for y in Pk :
        Up = U-U[y]
        for z in range (0,6):

            if Up[z] <= 0 :
                
                z = (Xc- abs(Up[z]))*(Xc*(L-Xc)/L)/Xc
                Z = np.append(Z, z)
            else :

                z = ((L-Xc)- Up[z])*(Xc*(L-Xc)/L)/((L-Xc))
                Z = np.append(Z, z)
            
            
   
        Y.append(Z)
    
    M = 2* cdmdB*np.sum(P*Y[0])
    detail_Bc_sense_1 ={
        'P_string' :P_string,
        'P' :P.tolist(),
        'critique':CRITIQUE.tolist(),
        'Yi' : Y[0].tolist(),
        'M'   : M.tolist(),
        'section'   :Xc,
    }
        
    return detail_Bc_sense_1,M



def get_p_critique_sense_2(Xc,L,cdmdB):
    P_string = ['P1','P2','P3','P4','P5','P6']
    P = np.array([3,6,6,3,6,6])
    U = np.array([0, 4.5, 6, 10.5, 15, 16.5])
   
    R = np.sum(P)
    CRITIQUE = []
    SPG = []
    RXL = []  # R*X/L
    SPGPK =[]
    Pk =np.array([],dtype=int)
    Z = np.array([])
    Y  =[]
    for x in range (6) :
        spg = np.sum(P[:x])            # SOME des P gauche a P critique 
        SPG = np.append(SPG, spg)

        rxl =R*Xc/L
        RXL = np.append(RXL, rxl)

        spgpk = spg + P[x]          # SOME des P gauche a P critique  + p critique 
        SPGPK = np.append(SPGPK, spgpk)
        
        if rxl >= spg and rxl <= spgpk:
            critique = 'critique'
            CRITIQUE = np.append(CRITIQUE, critique)
            Pk = np.append(Pk, x)
        
        else :
            critique = 'non  critique'
            CRITIQUE = np.append(CRITIQUE, critique)
    
    for y in Pk :
        Up = U-U[y]
        for z in range (0,6):

            if Up[z] <= 0 :
                
                
                z =( ( Xc-abs(Up[z]) )* ( Xc*(L-Xc)  ) )/(L*Xc)
                Z = np.append(Z, z)
            else :

                z = ((L-Xc)- Up[z])*(Xc*(L-Xc)/L)/((L-Xc))
                Z = np.append(Z, z)
            
            
   
        Y.append(Z)
    
    M = 2* cdmdB*np.sum(P*Y[0])
    detail_Bc_sense_2 ={
        'P_string' :P_string,
        'P' :P.tolist(),
        'critique':CRITIQUE.tolist(),
        'Yi' : Y[0].tolist(),
        'M'   : M.tolist(),
        'section'   :Xc,
    }
        
    return detail_Bc_sense_2,M



def detail_M_Bc(L,x_critique,cdmdB):
    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    detail_M_Bc_Total_sense_1 = []
    detail_M_Bc_Total_sense_2 = []
    M_Bc_Total_sense_1 = [0,]
    M_Bc_Total_sense_2 = [0,]

    for l in range(1,6):
        M_BC_detail_sense_1,M_Bc_sense_1 = get_p_critique_sense_1(Li[l],L,cdmdB)
        M_BC_detail_sense_2,M_Bc_sense_2 = get_p_critique_sense_2(Li[l],L,cdmdB)

        detail_M_Bc_Total_sense_1.append(M_BC_detail_sense_1)
        detail_M_Bc_Total_sense_2.append(M_BC_detail_sense_2)

        M_Bc_Total_sense_1.append(M_Bc_sense_1)
        M_Bc_Total_sense_2.append(M_Bc_sense_2)



    return detail_M_Bc_Total_sense_1,detail_M_Bc_Total_sense_2,M_Bc_Total_sense_1,M_Bc_Total_sense_2
    


# T systeme Bc

def get_T_Bc(Xc,L,cdmdB):
    P_string = ['P6','P5','P4','P3','P2','P1']
    P = np.array([6,6,3,6,6,3])
    U = np.array([0, 1.5 ,6, 10.5, 12, 16.5])
    Yi     = np.array([])
    
    a = Xc
    b = L-a 
    y1 = b/L
   
    for u in range(6) :
            
        yi = (y1*(b-U[u]))/b
        Yi=np.append(Yi,yi)
       
    
    T = np.sum(P*Yi)*2*cdmdB
    
        
    T_Bc_detail ={
        'P'       :P_string,
        'Yi_list' : Yi.tolist(),
        'T'        : T,
        'section'   :Xc,
           
        }

    
    return T_Bc_detail,T


def detail_T_Bc(L,x_critique,cdmdB):
    Li = [0,L/8,L/4,3*L/8,x_critique,L/2]
    detail_T_Bc_Total = []
    T_Bc_Total = np.array([])
    
    

    for l in range(0,6):
        T_BC_detail,T_Bc = get_T_Bc(Li[l],L,cdmdB)
        
        detail_T_Bc_Total.append(T_BC_detail)
        T_Bc_Total=np.append(T_Bc_Total,T_Bc)
       

    

    return  detail_T_Bc_Total,T_Bc_Total
   
             
        
        
    



    


def sections_home(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddDtSectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            form.save()
            # redirect to a new URL:
            return redirect("sections_home")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddDtSectionForm()

    return render(request, 'sections_home.html', {'form': form})


def repartition_longitudinal_home(request):

  
    repartition_long = repartition_longitudinal.objects.all()
    context={
        'repartition_longitudinal':repartition_long
    }
    

    return render(request, 'repartition-longitudinal/repartition_longitudinal_home.html', context)



def Add_repartition_longitudinal(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_repartition_longitudinal_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Title = form.cleaned_data['title']
            caracteristiques= form.cleaned_data['caracteristiques']
            
            L =caracteristiques.L
            G= caracteristiques.G
            g= caracteristiques.tab.P_total_tablier_sans_entretoise_linear
            A = caracteristiques.QA
            qtr1 = (caracteristiques.tab.trottoir_gauche.largeur_trottoir)*0.01*0.15
            qtr2 = (caracteristiques.tab.trottoir_droite.largeur_trottoir)*0.01*0.15
            cdmdM = caracteristiques.cdmdM
            cdmdB = caracteristiques.cdmdB
            nv = caracteristiques.nv
            cbc =caracteristiques.cbc
            cbt = caracteristiques.cbt

            
            # systeme B barré :
           
            R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi,Di,SPIDI,M = Mbc_Critique(L)
            R_Bt,DR_Bt,C_Bt,Xc_Bt,Xpc_Bt,SPG_Bt,RXL_Bt,SPGPK_Bt,CRITIQUE_Bt,DP1PC_Bt,DPCP6_Bt,DEBORDEMENT_Bt,Pi_Bt,Di_Bt,SPIDI_Bt,M_Bt =M_Bt_Critique(L)
            D_systeme_B = np.append(Xc,Xc_Bt)
            M_systeme_B = np.append(M,M_Bt)
            max_M_systeme_B_index = np.argmax(M_systeme_B)
            get_x_critique = D_systeme_B[max_M_systeme_B_index]
            if get_x_critique<L/2:
                x_critique = get_x_critique
            else:
                x_critique =0


            

            
            # P3 ET P4 DU systeme Bc in a dictionary to store 

            P3 ={
                'R':R.tolist(),
                'XR': DR.tolist(),
                'C_P3': C[0].tolist(),
                'X_P3_critique': Xc[0].tolist(),
                'X_prime': Xpc[0].tolist(),
                'some_des_p_gauche_a_P3' :SPG[0].tolist(),
                'RXL': RXL[0].tolist(),
                'some_des_p_gauche_plus_p_critique':SPGPK[0].tolist(),
                'critique' :CRITIQUE[0].tolist(),
                'distance_P1_a_P3' : DP1PC[0].tolist(),
                'distance_P3_a_P6': DPCP6[0].tolist(),
                'debordement' :DEBORDEMENT[0].tolist(),
                'Pi'           :Pi[0],
                'Di'           :Di[0],
                'Some_PiDi'   :SPIDI[0].tolist(),
                'M'   :M[0].tolist(),
            }

            P4 ={
                'R':R.tolist(),
                'XR': DR.tolist(),
                'C_P4': C[1].tolist(),
                'X_P4_critique': Xc[1].tolist(),
                'X_prime': Xpc[1].tolist(),
                
                'some_des_p_gauche_a_P4' :SPG[1].tolist(),
                'RXL': RXL[1].tolist(),
                'some_des_p_gauche_plus_p_critique':SPGPK[1].tolist(),
                'critique' :CRITIQUE[1].tolist(),
                'distance_P1_a_P4' : DP1PC[1].tolist(),
                'distance_P4_a_P6': DPCP6[1].tolist(),
                'debordement' :DEBORDEMENT[1].tolist(),
                'Pi'           :Pi[1],
                'Di'           :Di[1],
                'Some_PiDi'   :SPIDI[1].tolist(),
                'M'   :M[1].tolist(),
            }
             
            # P SYSTEME Bt in a dictionary to store  :
            P1_Bt ={
                'R':R_Bt.tolist(),
                'XR': DR_Bt.tolist(),
                'C_P1': C_Bt[0].tolist(),
                'X_P1_critique': Xc_Bt[0].tolist(),
                'X_prime': Xpc_Bt[0].tolist(),
                'some_des_p_gauche_a_P1' :SPG_Bt[0].tolist(),
                'RXL': RXL_Bt[0].tolist(),
                'some_des_p_gauche_plus_p_critique':SPGPK_Bt[0].tolist(),
                'critique' :CRITIQUE_Bt[0].tolist(),
                'distance_P1_a_P1' : DP1PC_Bt[0].tolist(),
                'distance_P1_a_P2': DPCP6_Bt[0].tolist(),
                'debordement' :DEBORDEMENT_Bt[0].tolist(),
                'Pi'           :Pi_Bt[0],
                'Di'           :Di_Bt[0],
                'Some_PiDi'   :SPIDI_Bt[0].tolist(),
                'M'   :M_Bt[0].tolist(),
            }
 

            
            
            #G:

            MG,TG,G_TOTAL = charge_repartie_sur_L(g,L,x_critique)

            # A :
            A_TOTAL =[]
            MA,TA , A_une_voie = charge_repartie_sur_L(A,L,x_critique)  #  A une voie
            MA_n  = MA * nv # MA  sur le nombre de vois
            TA_n  = TA * nv # TA  sur le nombre de vois
            A_TOTAL.append(MA.tolist())
            A_TOTAL.append(TA.tolist())
            A_TOTAL.append(MA_n.tolist())
            A_TOTAL.append(TA_n.tolist())

            #qtr
            Qtr_TOTAL  = []
            Mqtr1,Tqtr1 , q1 = charge_repartie_sur_L(qtr1,L,x_critique)  #  un trottoir
            Mqtr2,Tqtr2 , q2 = charge_repartie_sur_L(qtr2,L,x_critique)
            Mqtr = Mqtr1  + Mqtr2
            Tqtr = Tqtr1+ Tqtr2
            Qtr_TOTAL.append(Mqtr1.tolist())
            Qtr_TOTAL.append(Tqtr1.tolist())
            Qtr_TOTAL.append(Mqtr.tolist())
            Qtr_TOTAL.append(Tqtr.tolist())


            #MC120
            Mc120_TOTAL = []
            M_Mc120,T_Mc120 = charge_militaire(18.033,L,6.1,cdmdM,x_critique)
            Mc120_TOTAL.append(M_Mc120.tolist())
            Mc120_TOTAL.append(T_Mc120.tolist())
            
            #D240
            D240_TOTAL     =[]
            M_D240,T_D240  = convois_exceptionelle(12.903,L,18.6,x_critique)
            D240_TOTAL.append(M_D240.tolist())
            D240_TOTAL.append(T_D240.tolist())
            
            #Bt
            Bt_TOTAL     =[]
            M_Bt_Sur_L,yi_list_for_M,T_Bt_Sur_L,yi_list_for_T = Bt(L,x_critique,cdmdB)
            Bt_TOTAL.append((cbt*M_Bt_Sur_L).tolist())
            Bt_TOTAL.append((cbt*T_Bt_Sur_L).tolist())
            Bt_TOTAL.append((nv*cbt*M_Bt_Sur_L).tolist())
            Bt_TOTAL.append((nv*cbt*T_Bt_Sur_L).tolist())
           

            #Br 
            Br_TOTAL     =[]
            M_Br_Sur_L, Br_yi_list_for_M,  T_Br_Sur_L,  Br_yi_list_for_T = Br(L,x_critique,cdmdB)

            Br_TOTAL.append(M_Br_Sur_L.tolist())
            Br_TOTAL.append(T_Br_Sur_L.tolist())
          
            
            detail_M_Bc_Total_sense_1,detail_M_Bc_Total_sense_2,M_Bc_Total_sense_1,M_Bc_Total_sense_2 = detail_M_Bc(L,x_critique,cdmdB)
           
            

            M_Bc_Total_les_2_sense = (np.amax(np.array([M_Bc_Total_sense_1,M_Bc_Total_sense_2]),axis=0))
            


            detail_T_Bc_total,T_Bc_Total = detail_T_Bc(L,x_critique,cdmdB)
           

            Bc_TOTAL =[]
            Bc_TOTAL.append((M_Bc_Total_les_2_sense*cbc).tolist()),
            Bc_TOTAL.append((T_Bc_Total*cbc).tolist()),
            Bc_TOTAL.append((M_Bc_Total_les_2_sense*nv*cbc).tolist()),
            Bc_TOTAL.append((T_Bc_Total*nv*cbc).tolist()),
           
           
            

          
            
           

            """
            for x in range(5):
                k0_row = np.array([])
                for y in range(9):
                    k0 = k01[x,y] +((k02[x,y]-k01[x,y])*((0.671-0.65)/(0.70-0.65)))
                    k0_row = np.append(k0_row,k0)
                
                print(k0_row)
            """

            
            
            
            

            

           
            

            

          
 
           
            
           



            form.instance.G = G_TOTAL
            form.instance.A_TOTAL = A_TOTAL
            form.instance.qtr_TOTAL = Qtr_TOTAL
            form.instance.Mc120_TOTAL =Mc120_TOTAL
            form.instance.D240_TOTAL =D240_TOTAL
            form.instance.P3_Critique =P3
            form.instance.P4_Critique =P4
            form.instance.P1_BT =P1_Bt
            form.instance.xcritique =x_critique
            form.instance.Bt_TOTAL =Bt_TOTAL
            form.instance.Br_TOTAL =Br_TOTAL
            form.instance.detail_M_Bc_Total_sense_1 =detail_M_Bc_Total_sense_1
            form.instance.detail_M_Bc_Total_sense_2 =detail_M_Bc_Total_sense_2
            form.instance.T_Bc_detail = detail_T_Bc_total
            form.instance.M_Bc_Total_les_2_sense =M_Bc_Total_les_2_sense.tolist()
            form.instance.Bc_TOTAL = Bc_TOTAL
            
            
            
        
            form.save()
            return redirect(reverse("repartition_longitudinal_detail", kwargs={
                'slug': form.instance.slug
            }))
            
            
            # ...
            
            # redirect to a new URL:
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_repartition_longitudinal_form()

    return render(request, 'repartition-longitudinal/Add_repartition_longitudinal.html', {'form': form})


def repartition_longitudinal_detail(request,slug):
    pd.options.display.float_format = '{:.4f}'.format
    repartition_longitudinal_detail = get_object_or_404(repartition_longitudinal,slug=slug)
    G  = repartition_longitudinal_detail.G
    A =  repartition_longitudinal_detail.A_TOTAL
    qtr =  repartition_longitudinal_detail.qtr_TOTAL
    mc120 =  repartition_longitudinal_detail.Mc120_TOTAL
    d240 =  repartition_longitudinal_detail.D240_TOTAL
    BT =  repartition_longitudinal_detail.Bt_TOTAL
    Br =  repartition_longitudinal_detail.Br_TOTAL
    Bc  =  repartition_longitudinal_detail.Bc_TOTAL
    data_G = {
        "M": G[0],
        "T": G[1],
        
        }

    data_A = {
        "M1": A[0],
        "T1": A[1],
        "M2": A[2],
        "T2": A[3],
        
        }
    
    data_qtr  = {
        "M1": qtr[0],
        "T1": qtr[1],
        "M2": qtr[2],
        "T2": qtr[3],

    }

    data_mc120  = {
        "M1": mc120[0],
        "T1": mc120[1],
    
    }

    data_d240  = {
        "M1": d240[0],
        "T1": d240[1],
    
    }

    data_Bt  = {
        "M1": BT[0],
        "T1": BT[1],
        "M2": BT[2],
        "T2": BT[3],

    }

    data_Bc  = {
        "M1": Bc[0],
        "T1": Bc[1],
        "M2": Bc[2],
        "T2": Bc[3],

    }
 
    data_Br  = {
        "M1": Br[0],
        "T1": Br[1],
       

    }

    

    #load data into a DataFrame object:
    
    index = ['0','L/8','L/4','3L/8','Xc','L/2']
    df_G = pd.DataFrame(data_G) 
    df_G.index = index
    html_G = df_G.to_html()

    df_A = pd.DataFrame(data_A)
    df_A.index = index
    html_A = df_A.to_html()

    df_qtr = pd.DataFrame(data_qtr)
    df_qtr.index =index
    html_qtr = df_qtr.to_html()

    df_mc120 = pd.DataFrame(data_mc120)
    df_mc120.index =index
    html_mc120 = df_mc120.to_html()

    df_d240 = pd.DataFrame(data_d240)
    df_d240.index =index
    html_d240 = df_d240.to_html()

    df_Bt = pd.DataFrame(data_Bt)
    df_Bt.index =index
    html_Bt = df_Bt.to_html()

    df_Br = pd.DataFrame(data_Br)
    df_Br.index =index
    html_Br = df_Br.to_html()

    
    df_Bc = pd.DataFrame(data_Bc)
    df_Bc.index =index
    html_Bc = df_Bc.to_html()
    
    context = {
        'html_G':html_G,
        'html_A':html_A,
        'html_qtr':html_qtr,
        'html_mc120':html_mc120,
        'html_d240':html_d240,
        'html_Bt':html_Bt,
        'html_Br':html_Br,
        'html_Bc':html_Bc,

        'repartition_longitudinal_detail':repartition_longitudinal_detail,
        'title_G' :"charge G",
        'title_A' :"charge A",
        'title_qtr' :"charge qtr",
        'title_mc120' :"charge mc120",
        'title_d240' :"charge d240",
        'title_Bt'   :'charge Bt',
        'title_Br'   :'charge Br',
        'title_Bc'   :'charge Bc',
        
    }

    return render(request,'repartition-longitudinal/repartition_longitudinal_detail.html',context)



  