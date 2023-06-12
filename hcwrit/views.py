from django.shortcuts import render,redirect
from compliance.models import Advisor
from idtlit.models import Order
from django.contrib import messages
from .forms import *
# Create your views here.
def hcwrit_home(request,pk):
    path=request.path
    path = path.split('/')
    print(path)
    pk = int(path[2])
    try:
        adv =Advisor.objects.filter(advisor=request.user.id).exists()
    except:
        pass
    try:
        th =Advisor.objects.filter(tax_cat='4',advisor=request.user.id).exists()        
    except:
        pass
    return render(request,'hcwrit/hcwritmastertemplate.html',{'pk':pk,'adv':adv,'th':th})

def view_order_for_writ(request,pk):
    order = Order.objects.get(proceeding=pk)
    return render(request,'hcwrit/view_order_for_writ.html',{'order':order,'pk':pk})

def view_order_for_writ_approval(request,pk):
    order = Recommend_Writ.objects.get(order=pk)    
    return render(request,'hcwrit/view_order_for_writ_approval.html',{'order':order,'pk':pk})


def recommend_writ(request,pk):
  path=request.path
  path = path.split('/')
  pk = int(path[3])
#   order = Order.objects.get(proceeding=pk)
  if request.method=='POST':
      form = Recommend_Writ_Form(request.POST)
      if form.is_valid():
        try:
            instance=form.save(commit=False)
            instance.order=Order.objects.get(proceeding=pk)
            instance.recommended_by= Advisor.objects.get(advisor=request.user.id)
            instance.created_by= User.objects.get(id=request.user.id)
            instance.save()
            messages.success(request,'Order Successfully recommended for filing Writ')
            return redirect('hcwrit_home',pk)
        except:
              messages.error(request,'Something Went Wrong Pls Try again')
  else:
      form = Recommend_Writ_Form()
  return render(request,'hcwrit/recommend_writ.html',{'form':form,'pk':pk})

def approve_writ(request,pk):
  path=request.path 
  path = path.split('/')
  pk = int(path[3])
  try:
    if Recommend_Writ.objects.get(order=pk).is_recommended==True:
        try:
            pi = Recommend_Writ.objects.get(order=pk)
            if request.method=='POST':
                form = Approved_Writ_Form(request.POST,instance=pi)
                if form.is_valid():
                    try:
                        instance=form.save(commit=False)            
                        instance.approved_by= User.objects.get(id=request.user.id)
                        instance.save()
                        messages.success(request,'Order Successfully Approved for filing Writ')
                        return redirect('hcwrit_home',pk)
                    except:
                        messages.error(request,'Something Went Wrong Pls Try again')
            else:
                form = Approved_Writ_Form(instance=pi)
            return render(request,'hcwrit/approve_writ.html',{'form':form})
        except:
            pass
    else:
        messages.info(request,'Filing of writ has not been recommended as yet')
        return redirect('view_order_for_writ_approval',pk)
  except:
      pass
  
    

