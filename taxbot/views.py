from django.shortcuts import render
from .forms import PosForm, PosformSS
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def findpos(request):
    if request.method=='POST':
        fm=PosForm(request.POST)         
        if fm.is_valid():
            supplier = fm.cleaned_data['supplier_name']
            registered=fm.cleaned_data['registered']
            record_address=fm.cleaned_data['add_on_record']
            rec_location=fm.cleaned_data['rec_location']
            supp_location=fm.cleaned_data['supp_location']
            if registered=='Yes' or record_address=='Yes':
                pos=rec_location                
            else:
                pos=supp_location
        return HttpResponse(f'Place of Supply for this transaction and supplier {supplier} is {pos}')        
    else:
        fm=PosForm()
        return render(request,'chatbot/pos.html',{'form':fm})

def findposs(request):
    if request.method=='POST':
        fm=PosformSS(request.POST)         
        if fm.is_valid():
            supplier = fm.cleaned_data['supplier_name']
            registered=fm.cleaned_data['registered']
            record_address=fm.cleaned_data['add_on_record']
            rec_location=fm.cleaned_data['rec_location']
            supp_location=fm.cleaned_data['supp_location']
            service_name=fm.cleaned_data['service_name']
            state=fm.cleaned_data['state']   
            event_loc=fm.cleaned_data['event_loc']
            print(supplier,service_name,registered,record_address,rec_location,supp_location)     
            if service_name=='1' or service_name=='2' or '4':
                pos=state
            if service_name=='3':
                if registered=='Yes':
                    pos=rec_location
                else:
                    pos=state
            if service_name=='5':
                supplier=supplier
                if registered=='Yes' or event_loc == True:
                    pos=rec_location
                else:
                    pos=state
            if service_name=='6':
                supplier=supplier
                if registered=='Yes': 
                    pos=rec_location
                elif event_loc==True:
                    pos='This Transaction is not Taxable in India'
                else:
                    pos=state
            return HttpResponse(f'Place of Supply for this transaction is {pos}')        
    else:
        fm=PosformSS()
    return render(request,'chatbot/pos.html',{'form':fm})