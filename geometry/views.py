from django.shortcuts import render, get_object_or_404, redirect, reverse
import numpy as np
import pandas  as pd

from.models import section_type_01,section_type_02,SectionAdded
from cart.models import  Cart
from .forms import Add_section_type_01_form, Add_section_type_02_form
from decimal import Decimal
import csv
from django.http import HttpResponse

# Create your views here.





def HomeGeometry(request):
    cart_obj = Cart.objects.new_or_get(request)
    SectionList = SectionAdded.objects.all()
    context ={
        'SectionList':SectionList,

    }
    return render(request, 'geometry/GeometryHome.html', context)

    


def GeometryDetail(request,slug):
    geometry_detail = get_object_or_404(SectionAdded, slug=slug)
    data = {
        "B": geometry_detail.content_object.B,
        "Z": geometry_detail.content_object.Z,
        "S/Δ": geometry_detail.content_object.S_TO_DELTA,
        "I": geometry_detail.content_object.I,
        "I/Δ": geometry_detail.content_object.I_TO_DELTA,
       
        }

    #load data into a DataFrame object:
    pd.options.display.float_format = '{:.4f}'.format
    df = pd.DataFrame(data)
    html = df.to_html()
    
    
    context ={
        'geometry_detail':geometry_detail,
        'html'           :html,
        
    }
    return render(request, 'geometry/GeometryDetail.html', context)



def AddSection_01(request):
    cart_obj = Cart.objects.new_or_get(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_section_type_01_form(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            
            # get data :
            Title = form.cleaned_data['title']
            Bhourdis= form.cleaned_data['b_hourdis']
            Hhourdis= form.cleaned_data['h_hourdis']
            Hsection= form.cleaned_data['h_section']
            Btabledecompression= form.cleaned_data['b_table_de_compression']
            Htabledecompression= form.cleaned_data['h_table_de_compression']
            Bjonction= form.cleaned_data['b_jonction']
            Hjonction= form.cleaned_data['h_jonction']
            Bgoussetsuperieur= form.cleaned_data['b_gousset_superieur']
            Hgoussetsuperieur= form.cleaned_data['h_gousset_superieur']
            Bame= form.cleaned_data['b_ame']
            Hame= form.cleaned_data['h_ame']
            Bgousset_inferieur= form.cleaned_data['b_gousset_inferieur']
            Hgousset_inferieur= form.cleaned_data['h_gousset_inferieur']
            Btalon= form.cleaned_data['b_talon']
            Htalon= form.cleaned_data['h_talon']
           
            
            # calculate sections :
            B_hourdis = Bhourdis*Hhourdis
            B1             = Btabledecompression*Htabledecompression
            B2             = Bjonction*Hjonction
            B3             = (Bgoussetsuperieur*Hjonction)*2 #la jonction carré
            B4             = Bgoussetsuperieur*Hgoussetsuperieur
            B5             = Bame*(Hame+Hgoussetsuperieur+Hgousset_inferieur+Hjonction)
            B6             = Bgousset_inferieur*Hgousset_inferieur
            B7             = Btalon*Htalon
            B   = np.array([B1,B2,B3,B4,B5,B6,B7],dtype='f')
            B_TOTAL_BRUTE_SANS_HOURDIS = np.sum(B)
            B_TOTAL_NETTE_SANS_HOURDIS    = B_TOTAL_BRUTE_SANS_HOURDIS - 0.05*B_TOTAL_BRUTE_SANS_HOURDIS
            B_TOTAL_BRUTE_AVEC_HOURDIS = B_TOTAL_BRUTE_SANS_HOURDIS + B_hourdis
            B_TOTAL_NETTE_AVEC_HOURDIS = B_TOTAL_BRUTE_AVEC_HOURDIS -0.05*B_TOTAL_BRUTE_AVEC_HOURDIS

            # calculate Z :
            Z1                    =  Hsection-0.5*Htabledecompression
            Z2                    =  Hsection-Htabledecompression-(1/3*Hjonction)
            Z3                    =  Hsection-Htabledecompression-(0.5*Hjonction)
            Z4                    =  Hsection-Htabledecompression-Hjonction-(1/3*Hgoussetsuperieur)
            Z5                    =  Htalon + (Hame+Hgoussetsuperieur+Hgousset_inferieur+Hjonction)*0.5
            Z6                    =  Htalon + (1/3*Hgousset_inferieur)
            Z7                    =  0.5*Htalon
            Z_hourdis             = Hsection +0.5*Hhourdis
             
            Z = np.array([Z1,Z2,Z3,Z4,Z5,Z6,Z7])
            # S/Δ= B*Z
            S_TO_DELTA = np.array([])

            for x in range(0,7):
                s_to_delta = B[x]*Z[x]
                S_TO_DELTA = np.append(S_TO_DELTA, s_to_delta)


            S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS =   np.sum(S_TO_DELTA)
            S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS =   S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS -0.05*S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            S_TO_DELTA_hourdis     =   B_hourdis*Z_hourdis
            S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS + S_TO_DELTA_hourdis
            S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS-0.05*S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS

            # I0

            I1        =  (Btabledecompression*(Htabledecompression**3))/12
            I2        =  ((Bjonction*(Hjonction**3))/36)*2
            I3        =  ((Bgoussetsuperieur*(Hjonction**3))/12)*2
            I4        =  ((Bgoussetsuperieur*(Hgoussetsuperieur**3))/36)*2
            I5        =  (Bame*((Hame+Hgoussetsuperieur+Hgousset_inferieur+Hjonction)**3))/12
            I6        =  ((Bgousset_inferieur*(Hgousset_inferieur**3))/36)*2
            I7        =  (Btalon*(Htalon**3))/12
            I_hourdis =  (Bhourdis*(Hhourdis**3))/12
          
            I         = np.array([I1,I2,I3,I4,I5,I6,I7])
            #  I/Δ=I0+BxZ²
            I_TO_DELTA = np.array([])

            for y in range(0,7):
                i_to_delta = I[y]+(B[y]*(Z[y]**2))
                I_TO_DELTA = np.append(I_TO_DELTA, i_to_delta)

    

            I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = np.sum(I_TO_DELTA)
            I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS -0.1*I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            I_TO_DELTA_hourdis     = I_hourdis +(B_hourdis*(Z_hourdis**2))
            I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS+I_TO_DELTA_hourdis
            I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS =I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS-0.1*I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            
            V_prime_sans_hourdis = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS/B_TOTAL_BRUTE_SANS_HOURDIS
            IG_sans_hourdis     = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS - (S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS* V_prime_sans_hourdis)
            V_sans_hourdis      = Hsection - V_prime_sans_hourdis
            rendement_sans_hourdis = IG_sans_hourdis/(V_sans_hourdis*V_prime_sans_hourdis*B_TOTAL_BRUTE_SANS_HOURDIS )


            V_prime_avec_hourdis = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS/B_TOTAL_BRUTE_AVEC_HOURDIS
            IG_avec_hourdis    = I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS - (S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS* V_prime_avec_hourdis)
            V_avec_hourdis     = (Hsection+Hhourdis) - V_prime_avec_hourdis
            rendement_avec_hourdis = IG_avec_hourdis/(V_avec_hourdis*V_prime_avec_hourdis*B_TOTAL_BRUTE_AVEC_HOURDIS )
         

            
            





            
            
            form.instance.cart = cart_obj
            
            form.instance.B   = B.tolist()
            
            form.instance.B_hourdis = B_hourdis

            form.instance.B_TOTAL_BRUTE_SANS_HOURDIS = B_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.B_TOTAL_NETTE_SANS_HOURDIS = B_TOTAL_NETTE_SANS_HOURDIS
            form.instance.B_TOTAL_BRUTE_AVEC_HOURDIS = B_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.B_TOTAL_NETTE_AVEC_HOURDIS = B_TOTAL_NETTE_AVEC_HOURDIS

            # Z :
            form.instance.Z   = Z.tolist()
            
            form.instance.Z_hourdis = Z_hourdis
            
            # S/Δ= B*Z

            form.instance.S_TO_DELTA   = S_TO_DELTA.tolist()
            
            form.instance.S_TO_DELTA_hourdis = S_TO_DELTA_hourdis

            form.instance.S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS

            # I0

            form.instance.I = I.tolist()
           
            form.instance.I_hourdis = I_hourdis

             #  I/Δ=I0+BxZ²

            form.instance.I_TO_DELTA = I_TO_DELTA.tolist()
            
            form.instance.I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS
            form.instance.I_TO_DELTA_hourdis     = I_TO_DELTA_hourdis 
            form.instance.I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS


            form.instance.V_prime_sans_hourdis = V_prime_sans_hourdis
            form.instance.V_sans_hourdis       = V_sans_hourdis
            form.instance.IG_sans_hourdis      = IG_sans_hourdis
            form.instance.rendement_sans_hourdis =rendement_sans_hourdis 

            form.instance.V_prime_avec_hourdis = V_prime_avec_hourdis
            form.instance.V_avec_hourdis       = V_avec_hourdis
            form.instance.IG_avec_hourdis      = IG_avec_hourdis
            form.instance.rendement_avec_hourdis =rendement_avec_hourdis 

            


          

              

            form.save()
            return redirect(reverse("GeometryDetail", kwargs={
                'slug': form.instance.slug
            }))

            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_section_type_01_form()

    return render(request, 'geometry/Add_section_type_01.html', {'form': form})



def AddSection_02(request):
    cart_obj = Cart.objects.new_or_get(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Add_section_type_02_form(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            
            # get data :
            Title = form.cleaned_data['title']
            Bhourdis= form.cleaned_data['b_hourdis']
            Hhourdis= form.cleaned_data['h_hourdis']
            Hsection= form.cleaned_data['h_section']
            Btabledecompression= form.cleaned_data['b_table_de_compression']
            Htabledecompression= form.cleaned_data['h_table_de_compression']
            Bjonction= form.cleaned_data['b_jonction']
            Hjonction= form.cleaned_data['h_jonction']
            Bame= form.cleaned_data['b_ame']
            Hame= form.cleaned_data['h_ame']
           
           
            
            # calculate sections :
            B_hourdis = Bhourdis*Hhourdis
            B1             = Btabledecompression*Htabledecompression
            B2             = Bjonction*Hjonction
            B3             = Bame*Hame
            B4             = Bame* Hjonction   
           
            B   = np.array([B1,B2,B3,B4])
            B_TOTAL_BRUTE_SANS_HOURDIS = np.sum(B)
            B_TOTAL_NETTE_SANS_HOURDIS    = B_TOTAL_BRUTE_SANS_HOURDIS - 0.05*B_TOTAL_BRUTE_SANS_HOURDIS
            B_TOTAL_BRUTE_AVEC_HOURDIS = B_TOTAL_BRUTE_SANS_HOURDIS + B_hourdis
            B_TOTAL_NETTE_AVEC_HOURDIS = B_TOTAL_BRUTE_AVEC_HOURDIS -0.05*B_TOTAL_BRUTE_AVEC_HOURDIS

            # calculate Z :
            Z1                    =  Hsection-0.5*Htabledecompression
            Z2                    =  Hsection-Htabledecompression-(1/3*Hjonction)
            Z3                    =  Hame/2
            Z4                    = Hame+(Hjonction/2)
            Z_hourdis             = Hsection +0.5*Hhourdis
             
            Z = np.array([Z1,Z2,Z3,Z4])
            # S/Δ= B*Z
            S_TO_DELTA = np.array([])

            for x in range(0,4):
                s_to_delta = B[x]*Z[x]
                S_TO_DELTA = np.append(S_TO_DELTA, s_to_delta)


            S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS =   np.sum(S_TO_DELTA)
            S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS =   S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS -0.05*S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            S_TO_DELTA_hourdis     =   B_hourdis*Z_hourdis
            S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS + S_TO_DELTA_hourdis
            S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS-0.05*S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS

            # I0

            I1        =  (Btabledecompression*(Htabledecompression**3))/12
            I2        =  ((Bjonction*(Hjonction**3))/36)*2
            
            I3       =  (Bame*(Hame**3))/12
            I4       =  (Bame*(Hjonction**3))/12
           
            I_hourdis =  (Bhourdis*(Hhourdis**3))/12
          
            I         = np.array([I1,I2,I3,I4])
            #  I/Δ=I0+BxZ²
            I_TO_DELTA = np.array([])

            for y in range(0,4):
                i_to_delta = I[y]+(B[y]*(Z[y]**2))
                I_TO_DELTA = np.append(I_TO_DELTA, i_to_delta)

    

            I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = np.sum(I_TO_DELTA)
            I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS -0.1*I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            I_TO_DELTA_hourdis     = I_hourdis +(B_hourdis*(Z_hourdis**2))
            I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS+I_TO_DELTA_hourdis
            I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS =I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS-0.1*I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            
            V_prime_sans_hourdis = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS/B_TOTAL_BRUTE_SANS_HOURDIS
            IG_sans_hourdis     = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS - (S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS* V_prime_sans_hourdis)
            V_sans_hourdis      = Hsection - V_prime_sans_hourdis
            rendement_sans_hourdis = IG_sans_hourdis/(V_sans_hourdis*V_prime_sans_hourdis*B_TOTAL_BRUTE_SANS_HOURDIS )


            V_prime_avec_hourdis = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS/B_TOTAL_BRUTE_AVEC_HOURDIS
            IG_avec_hourdis    = I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS - (S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS* V_prime_avec_hourdis)
            V_avec_hourdis     = (Hsection+Hhourdis) - V_prime_avec_hourdis
            rendement_avec_hourdis = IG_avec_hourdis/(V_avec_hourdis*V_prime_avec_hourdis*B_TOTAL_BRUTE_AVEC_HOURDIS )
         

            





            
            
            form.instance.cart = cart_obj
            
            form.instance.B   = B.tolist()
            
            form.instance.B_hourdis = B_hourdis

            form.instance.B_TOTAL_BRUTE_SANS_HOURDIS = B_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.B_TOTAL_NETTE_SANS_HOURDIS = B_TOTAL_NETTE_SANS_HOURDIS
            form.instance.B_TOTAL_BRUTE_AVEC_HOURDIS = B_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.B_TOTAL_NETTE_AVEC_HOURDIS = B_TOTAL_NETTE_AVEC_HOURDIS

            # Z :
            form.instance.Z   = Z.tolist()
            
            form.instance.Z_hourdis = Z_hourdis
            
            # S/Δ= B*Z

            form.instance.S_TO_DELTA   = S_TO_DELTA.tolist()
            
            form.instance.S_TO_DELTA_hourdis = S_TO_DELTA_hourdis

            form.instance.S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = S_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = S_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS

            # I0

            form.instance.I = I.tolist()
           
            form.instance.I_hourdis = I_hourdis

             #  I/Δ=I0+BxZ²

            form.instance.I_TO_DELTA = I_TO_DELTA.tolist()
            
            form.instance.I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_SANS_HOURDIS
            form.instance.I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS = I_TO_DELTA_TOTAL_NETTE_SANS_HOURDIS
            form.instance.I_TO_DELTA_hourdis     = I_TO_DELTA_hourdis 
            form.instance.I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_BRUTE_AVEC_HOURDIS
            form.instance.I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS = I_TO_DELTA_TOTAL_NETTE_AVEC_HOURDIS
            
            form.instance.V_prime_sans_hourdis = V_prime_sans_hourdis
            form.instance.V_sans_hourdis       = V_sans_hourdis
            form.instance.IG_sans_hourdis      = IG_sans_hourdis
            form.instance.rendement_sans_hourdis =rendement_sans_hourdis 

            form.instance.V_prime_avec_hourdis = V_prime_avec_hourdis
            form.instance.V_avec_hourdis       = V_avec_hourdis
            form.instance.IG_avec_hourdis      = IG_avec_hourdis
            form.instance.rendement_avec_hourdis =rendement_avec_hourdis 

            


          

              

            form.save()
            return redirect(reverse("GeometryDetail", kwargs={
                'slug': form.instance.slug
            }))



            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Add_section_type_02_form()

    return render(request, 'geometry/Add_section_type_02.html', {'form': form})




# Simple CSV Write Operation
def geometry_csv_export(request,id):
    cart_obj = Cart.objects.new_or_get(request)
    geometry = Dt_section.objects.get(id=id,cart=cart_obj)
    h_B5 = geometry.h_ame + geometry.h_gousset_superieur + geometry.h_gousset_inferieur +geometry.h_jonction
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'

    writer = csv.writer(response)
    writer.writerow(['section', 'b', 'h', 'B', 'Z', 'S/Δ=BxZ','I0(cm4)','','I/Δ=I0+BxZ²'])
    writer.writerow(['1', geometry.b_table_de_compression, geometry.h_table_de_compression, geometry.B1, geometry.Z1, geometry.S_TO_DELTA_1, geometry.I1, geometry.I_TO_DELTA_1])
    writer.writerow(['2', geometry.b_jonction, geometry.h_jonction, geometry.B2, geometry.Z2, geometry.S_TO_DELTA_2, geometry.I2, geometry.I_TO_DELTA_2])
    writer.writerow(['3', geometry.b_gousset_superieur, geometry.h_gousset_superieur, geometry.B3, geometry.Z3, geometry.S_TO_DELTA_3, geometry.I3, geometry.I_TO_DELTA_3])
    writer.writerow(['4', geometry.b_gousset_superieur, geometry.h_gousset_superieur, geometry.B4, geometry.Z4, geometry.S_TO_DELTA_4, geometry.I4, geometry.I_TO_DELTA_4])
    writer.writerow(['5', geometry.b_table_de_compression, geometry.h_table_de_compression, geometry.B5, geometry.Z5, geometry.S_TO_DELTA_5, geometry.I5, geometry.I_TO_DELTA_5])
    writer.writerow(['6', geometry.b_gousset_inferieur, geometry.h_gousset_inferieur, geometry.B6, geometry.Z6, geometry.S_TO_DELTA_6, geometry.I6, geometry.I_TO_DELTA_6])
    writer.writerow(['1', geometry.b_talon, geometry.h_talon, geometry.B7, geometry.Z7, geometry.S_TO_DELTA_7, geometry.I7, geometry.I_TO_DELTA_7])

  

    return response




    






   

def Mbc_critique(L):
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
    Pi =[]
    Di =[]
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

            else :
                debordement = 'il ya  débordement refaire le calcule avec P1 P2 P3 P4'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)

            


        else :
            critique = 'non critique'
            CRITIQUE = np.append(CRITIQUE, critique)
           



    


    return R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi,Di,SPIDI,M

def repartition_BC(request):
    R,DR ,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi,Di,SPIDI,M = Mbc_critique(24.7)
    print(R)
    print(DR)
    print(C)
    print(Xc)
    print(SPG)
    print(RXL)
    print(SPGPK)
    print(CRITIQUE)
    print(DP1PC)
    print(DPCP6)
    print(Xpc)
    print(DEBORDEMENT)
    print(Pi)
    print(Di)
    print(SPIDI)
    print(M)
   


    return render(request, 'bc.html',)



def MG(L,G):


    Li =[0,L/8,L/4,3*L/8,10.625,L/2]
    A  =[]
    B  =[]
    H  =[]
    A1 =[]
    A2 =[]
    M  =[]
    for x in Li:
        a = x 
        A = np.append(A, a)
        b = L-x 
        B = np.append(B, b)

        h = a*b/L
        H = np.append(H, h)

        a1 = h*a/2
        A1 = np.append(A1, a1)
        a2 = h*b/2
        A2 = np.append(A2, a2)
        m = (a1+a2)*G
        M = np.append(M, m)


    return Li,A,B,H,A1,A2,M


def TG(L,G):
    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H_t  =[]
    A1_t =[]
    T   = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = b_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*b_t/2
            A1_t = np.append(A1_t, a1_t)
            
            t = (a1_t)*G
            T = np.append(T, t)
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = a_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*a_t/2
            A1_t = np.append(A1_t, a1_t)

            t = (a1_t)*G
            T = np.append(T, t)
           

    return Li_t,A_t,B_t,H_t,A1_t,T

    




def MG_view(request):

    Li,A,B,H,A1,A2,M = MG(24.7,19.8)
    Li_t,A_t,B_t,H_t,A1_t,T = TG(24.7,19.8)
    print(T)

    

    context ={

        """ Moment """
        'Li' :Li,
        'A' :A ,
        'B': B ,
        'H' : H,
        'A1' : A1,
        'A2' : A2,
        'M' :M ,
        """ effort tranchant """
        'Li_t' :Li_t,
        'A_t' :A_t ,
        'B_t': B_t ,
        'H_t' : H_t,
        'A1_t' : A1_t,
        'T' :T ,

    }
    

    return render(request, 'MG.html',context)




def qtr(L,Ltr,J):

    qtr = 0.15 * Ltr *J 

    Li =[0,L/8,L/4,3*L/8,10.625,L/2]
    A  =[]
    B  =[]
    H  =[]
    A1 =[]
    A2 =[]
    M  =[]
    for x in Li:
        a = x 
        A = np.append(A, a)
        b = L-x 
        B = np.append(B, b)

        h = a*b/L
        H = np.append(H, h)

        a1 = h*a/2
        A1 = np.append(A1, a1)
        a2 = h*b/2
        A2 = np.append(A2, a2)
        m = (a1+a2)*qtr
        M = np.append(M, m)


    return Li,A,B,H,A1,A2,M



def T_qtr(L,Ltr,J):
    qtr = 0.15 * Ltr *J 
    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H_t  =[]
    A1_t =[]
    T   = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = b_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*b_t/2
            A1_t = np.append(A1_t, a1_t)
            
            t = (a1_t)*qtr
            T = np.append(T, t)
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = a_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*a_t/2
            A1_t = np.append(A1_t, a1_t)

            t = (a1_t)*qtr
            T = np.append(T, t)
           

    return Li_t,A_t,B_t,H_t,A1_t,T




def qtr_view(request):

    Li,A,B,H,A1,A2,M = qtr(24.7,1.5,1)
    Li_t,A_t,B_t,H_t,A1_t,T = T_qtr(24.7,1.5,1)
   

    

    context ={

        """ Moment """
        'Li' :Li,
        'A' :A ,
        'B': B ,
        'H' : H,
        'A1' : A1,
        'A2' : A2,
        'M' :M ,

         """ effort tranchant """
        'Li_t' :Li_t,
        'A_t' :A_t ,
        'B_t': B_t ,
        'H_t' : H_t,
        'A1_t' : A1_t,
        'T' :T ,
        

    }
    

    return render(request, 'qtr.html',context)




def M_A(L,qa,n):

    Qa = qa *n

    Li =[0,L/8,L/4,3*L/8,10.625,L/2]
    A  =[]
    B  =[]
    H  =[]
    A1 =[]
    A2 =[]
    M  =[]
    for x in Li:
        a = x 
        A = np.append(A, a)
        b = L-x 
        B = np.append(B, b)

        h = a*b/L
        H = np.append(H, h)

        a1 = h*a/2
        A1 = np.append(A1, a1)
        a2 = h*b/2
        A2 = np.append(A2, a2)
        m = (a1+a2)*Qa
        M = np.append(M, m)


    return Li,A,B,H,A1,A2,M



def T_A(L,qa,n):
    Qa = qa *n
    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H_t  =[]
    A1_t =[]
    T   = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = b_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*b_t/2
            A1_t = np.append(A1_t, a1_t)
            
            t = (a1_t)*Qa
            T = np.append(T, t)
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h_t = a_t/L
            H_t = np.append(H_t, h_t)

            a1_t = h_t*a_t/2
            A1_t = np.append(A1_t, a1_t)

            t = (a1_t)*Qa
            T = np.append(T, t)
           

    return Li_t,A_t,B_t,H_t,A1_t,T





def A_view(request):

    Li,A,B,H,A1,A2,M = M_A(24.7,4.239,1)
    Li_t,A_t,B_t,H_t,A1_t,T = T_A(24.7,4.239,1)
   

    

    context ={

        """ Moment """
        'Li' :Li,
        'A' :A ,
        'B': B ,
        'H' : H,
        'A1' : A1,
        'A2' : A2,
        'M' :M ,

         """ effort tranchant """
        'Li_t' :Li_t,
        'A_t' :A_t ,
        'B_t': B_t ,
        'H_t' : H_t,
        'A1_t' : A1_t,
        'T' :T ,
        

    }
    

    return render(request, 'A.html',context)


def MC120(L,q,l):

    
    #  la fonction n'est pas tres précise car el place le chargement au milieu de la section  ce qui est valable que pour L/2 plus on s'eloigne de L/2 plus on deplace la charge vers le sens de la plus grande section
    Li =[0,L/8,L/4,3*L/8,10.625,L/2]
    A  =[]
    B  =[]
    H =[]
    H2 =[]
    H2 =[]
    S1  =[]
    S2  =[]
    M  =[]

    area = np.trapz([0,6.175,0], x=[0,12.35,24.7])
    
   
    for x in Li:
        if x == 0:
            A = 0
            B = 0
            H = 0
            H1 = 0
            H2 = 0
            S1= 0
            S2 =0
            M = 0
        else :

            a = x 
            A = np.append(A, a)
            b = L-x 
            B = np.append(B, b)

            h = a*b/L
            H = np.append(H, h)

            h1 = ((a-l/2)*h)/a
            H1 = np.append(H1, h1)

            h2 = ((b-l/2)*h)/b
            H2 = np.append(H2, h2)

            s1 = ((h1+h)* (l/2))/2
            S1 = np.append(S1, s1)

            s2 = ((h2+h)* (l/2))/2
            S2 = np.append(S2, s2)


            m = (s1+s2)*q*1.0989
            M = np.append(M, m)


    return Li,A,B,H,H1,H2,S1,S2,M,area


def T_MC120(L,q,l):
   
    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H1_t  =[]
    H2_t  =[]
    S_t =[]
    T   = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

           

            h1_t = b_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((b_t-l)*h1_t)/b_t
            H2_t = np.append(H2_t, h2_t)

            s_t = ((h1_t+h2_t)*l)/2
            S_t = np.append(S_t, s_t)
            
            t = (s_t)*q*1.0989
            T = np.append(T, t)
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h1_t = a_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((a_t-l)*h1_t)/a_t
            H2_t = np.append(H2_t, h2_t)

            a_t = ((h1_t+h2_t)*l)/2
            A_t = np.append(A_t, a_t)

            t = (a_t)*q
            T = np.append(T, t)
           

    return Li_t,A_t,B_t,H1_t,H2_t,A_t,T







def MC120_view(request):

    Li,A,B,H,H1,H2,S1,S2,M,area = MC120(24.7,18.033,6.1)
    Li_t,A_t,B_t,H1_t,H2_t,A_t,T = T_MC120(24.7,18.033,6.1)
    print(area)
    
    

    

    context ={

        """ Moment """
        'Li' :Li,
        'A' :A ,
        'B': B ,
        'H' : H,
        'H1' : H1,
        'H2' : H2,
        'S1' : S1,
        'S2' : S2,
        'M' :M ,

         """ effort tranchant """
        'Li_t' :Li_t,
        'A_t' :A_t ,
        'B_t': B_t ,
        'H1_t' : H1_t,
        'H2_t' : H2_t,
        'A_t' : A_t,
        'T' :T ,



      
        

    }
    

    return render(request, 'MC120.html',context)





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
    Di =[]
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

            else :
                debordement = 'il ya  débordement refaire le calcule avec P1 P2 P3 P4'
                DEBORDEMENT = np.append(DEBORDEMENT, debordement)

            


        else :
            critique = 'non critique'
            CRITIQUE = np.append(CRITIQUE, critique)
           



    


    return R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi,Di,SPIDI,M
    




def Bt_critique_view(request):

    R,DR,C,Xc,Xpc,SPG,RXL,SPGPK,CRITIQUE,DP1PC,DPCP6,DEBORDEMENT,Pi,Di,SPIDI,M = M_Bt_Critique(24.7)

    print(R)
    print(DR)
    print(C)
    print(Xc)
    print(SPG)
    print(RXL)
    print(SPGPK)
    print(CRITIQUE)
    print(DP1PC)
    print(DPCP6)
    print(Xpc)
    print(DEBORDEMENT)
    print(Pi)
    print(Di)
    print(SPIDI)
    print(M)

    return render(request, 'Bt_critique.html',)





def Bt(L):

    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H1_t  =[]
    H2_t  =[]
    
    M  = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

           

            h1_t = b_t*a_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((b_t-1.35)*h1_t)/b_t
            H2_t = np.append(H2_t, h2_t)

            m = (8 *h1_t+8*h2_t) *2*1.1048
            M = np.append(M, m)
            
            
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h1_t = b_t*a_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((a_t-1.35)*h1_t)/a_t
            H2_t = np.append(H2_t, h2_t)

            m = (8 *h1_t+8*h2_t) *2*1.1048
            M = np.append(M, m)

            
           

    return Li_t,A_t,B_t,H1_t,H2_t,M


def T_Bt(L):

    Li_t =[0,L/8,L/4,3*L/8,10.625,L/2]
    A_t  =[]
    B_t  =[]
    H1_t  =[]
    H2_t  =[]
    
    T  = []
    for x in Li_t:
        if x <= L/2:
            
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

           

            h1_t = b_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((b_t-1.35)*h1_t)/b_t
            H2_t = np.append(H2_t, h2_t)

            t = (8 *h1_t+8*h2_t) *2*1.1048
            T = np.append(T, t)
            
            
        else:
            a_t = x 
            A_t = np.append(A_t, a_t)
            b_t = L-x 
            B_t = np.append(B_t, b_t)

            h1_t = a_t/L
            H1_t = np.append(H1_t, h1_t)

            h2_t = ((a_t-1.35)*h1_t)/a_t
            H2_t = np.append(H2_t, h2_t)

            t = (8 *h1_t+8*h2_t) *2*1.1048
            T = np.append(T,t)

            
           

    return Li_t,A_t,B_t,H1_t,H2_t,T



def Bt_view(request):

    Li_t,A_t,B_t,H1_t,H2_t,M = Bt(24.7)
    Li_t,A_t,B_t,H1_t,H2_t,T = T_Bt(24.7)
    P,critique,Pk,SPGPK,Y,Z = get_p_critique(6.175)
    array,array1,array2,k01,k02,K0 = gyon_massonet(5,5,5,5)
    print(K0)
   

    #print(np.sum(P*Z)*2*1.1048)
    

    return render (request,'Bt.html',)



def get_p_critique(Xc):

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

        rxl =R*Xc/24.7
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
                
                z = (Xc- abs(Up[z]))*(Xc*(24.7-Xc)/24.7)/Xc
                Z = np.append(Z, z)
            else :

                z = ((24.7-Xc)- Up[z])*(Xc*(24.7-Xc)/24.7)/((24.7-Xc))
                Z = np.append(Z, z)
            
            
   
        Y.append(Z)
        
    return P,CRITIQUE,Pk,SPGPK,Y,Z


def gyon_massonet(teta1,teta2,a,b):

    array = {
        '0.65':np.array( [
            [0.1776,	0.8588,	0.9965,	1.1468,	1.231,	1.1468,	0.9965,	0.8588,	0.7485],
            [0.5289,	0.633,	0.7702,	0.9493,	1.1468,	1.2818,	1.2516,	1.1561,	1.0648],
            [0.3823,	0.4734,	0.5966,	0.7702,	0.9965,	1.2516,	1.4559,	1.5073,	1.5005],
            [0.286,	0.3648,	0.4734,	0.633,	0.8588,	1.1561,	1.5073,	1.8418,	2.0659],
            [0.2171,	0.286,	0.3823,	0.5289,	0.7485,	1.0648,	1.5005,	2.0659,	2.7342]
            ]),
        '0.70':np.array( [
            [0.0216,	0.5464,	1.058,	1.4938,	1.6955,	1.4938,	1.058,	0.5464,	0.0216],
            [-0.3589,	0.1095,	0.5862,	1.067,	1.4938,	1.7118,	1.5548,	1.1934,	0.7809],
            [-0.5114,	-0.1756,	0.1798,	0.5862,	1.058,	1.5548,	1.9393,	2.0554,	2.0618],
            [-0.5575,	-0.3794,	-0.1756,	0.1095,	0.5464,	1.1934,	2.0554,	3.0254,	3.9282],
            [-0.5733,	-0.5575,	-0.5114,	-0.3589,	0.0216,	0.7809,	2.0618,	3.9282,	6.2464]
        ]),


    
    }

    array1 =array[str(0.65)]
    array2 =array['0.70']
    k01 = array1[0]
    k02 = array2[0]
    K0  =[]

    for x in range(9):
        k0 = k01[x] + ((k02[x]-k01[x]) *( (0.671-0.650)/(0.70-0.650)))
        K0 = np.append(K0, k0)




    return array,array1,array2,k01,k02,K0








