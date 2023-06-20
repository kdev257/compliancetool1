from django.shortcuts import render,redirect
from django.contrib import messages
from compliance.models import Advisor
from django.contrib.auth.decorators import login_required
from idtlit.models import Order,Issue,User,Initial_Notice,ProposedAddition,Addition
from idtlit.functions import check_total_additions,sum_addition
from .forms import *
from idtlit.forms import Additions_Form_Edit
from .models import *
from django.db.models import Q
# Create your views here.
@login_required
def action(request,pk): #This View triggers master template for appeal proceedings\
    try:
        adv =Advisor.objects.filter(advisor=request.user.id).exists()
    except:
        pass
    try:
        th =Advisor.objects.filter(Q(tax_cat='4') &Q(advisor=request.user.id)).exists()        
    except:
        th.DoesNotExist
        th = None
    try:
        pi = Order.objects.get(order__proceeding=pk)
    except:
        Order.DoesNotExist
        pi = None
    try:
        notice = Hearing_Notice.objects.get(order__proceeding=pk)
    except:
        Hearing_Notice.DoesNotExist
        notice= None
    try:    
        hearing = App_Appeal_Hearing.objects.filter(order__proceeding=pk).last().hearing_date
    except:
        App_Appeal_Hearing.DoesNotExist
        hearing= None
    try:
        order= Appellate_Order.objects.get(order__proceeding=pk)
    except:
        Appellate_Order.DoesNotExist
        order=None
    pad = ProposedAddition.objects.filter(proceeding=pk).order_by('id')   
    addition = Addition.objects.filter(order__proceeding=pk).order_by('issue')
    aa = Appellate_Order_Details.objects.filter(order__proceeding=pk).order_by('issue')   
    cash = Payment.objects.filter(order__proceeding=pk)           
    return render(request,('app_appeal/master_template_appeal.html'),{'pi':pi,'pk':pk,'adv':adv,'th':th,'notice':notice,'hearing':hearing,'order':order,'pad':pad,'addition':addition,'aa':aa,'cash':cash   })

@login_required
def appeal_action(request,pk): 
    ''' This View show list of issue in order as uploaded by location to funtional head. The function mananger decided whether appeal is to be filed and recommend the action to tax head'''
    add = Addition.objects.filter(order__proceeding=pk)     
    return render(request,"app_appeal/appeal_action.html",{'add':add,'pk':pk,'add':add})

@login_required
def view_appeal_action(request,pk): 
    ''' This View is similar to above but it is meant for tax head to approve the recommendation given by functional manager show list of issue in order as uploaded by location to funtional head duly recommended by for approval to tax head.'''
    add = Addition.objects.filter(order__proceeding=pk)     
    return render(request,"app_appeal/view_appeal_action.html",{'add':add,'pk':pk,'add':add})

@login_required
def update_appeal_action(request,pk,id):
    '''Indirect Tax head recommend the action againt the order'''
    path=request.path
    path = path.split('/')
    pk = int(path[3])    
    add = Addition.objects.get(id=id)
    if Advisor.objects.filter(advisor=request.user.id).exists():
        if request.method =='POST':
            form = Update_Appeal_Action_Form(request.POST,instance=add)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.disputed_additions=instance.total_additions-instance.admitted_additions
                instance.recommended_by= User.objects.get(id=request.user.id)
                instance.save()
                return redirect('appeal_action',pk)
        else:        
            form=Update_Appeal_Action_Form(instance=add)
        return render(request,'app_appeal/update_appeal_action.html',{'form':form,'pk':pk,'add':add})
    else:
        messages.error(request,'You are not authorized to perform this action')
    return redirect('view_appeal_action',pk)

@login_required
def approve_appeal_action(request,pk,id):
    '''Tax head approve the action as recommended by functional head'''    
    path=request.path
    path = path.split('/')
    pk = int(path[3])    
    add = Addition.objects.get(id=id)
    if add.is_recommended:
        if request.method =='POST':
            form = Approve_Appeal_Actions_Form(request.POST,instance=add)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.approved_by= User.objects.get(id=request.user.id)
                instance.save()
                return redirect('view_appeal_action',pk)
        else:
            form=Approve_Appeal_Actions_Form(instance=add)
        return render(request,'app_appeal/approve_appeal_action.html',{'form':form,'pk':pk,'add':add})
    else:
         messages.error(request,'This issue yet to be recommeded for action by Functional Head')
    return redirect('view_appeal_action',pk)

@login_required       
def draft_appeal(request,pk):
        approved =list(Addition.objects.filter(order__proceeding=pk).values_list('is_approved',flat=True))
        if not False in approved: 
            if request.method=='POST':
                form = Draft_Appeal_Form(request.POST,request.FILES)
                if form.is_valid():
                    try:
                        instance=form.save(commit=False)
                        instance.created_by=User.objects.get(id=request.user.id)
                        instance.order = Order.objects.get(proceeding=pk)
                        instance.save()
                        messages.success(request,'Draft Appeal Successfully Saved to database')
                        return redirect('runmastertemp',pk)
                    except:
                        messages.error(request,'Something Went Wrong, Pls Try Again')
            else:
                form = Draft_Appeal_Form()
            return render(request,'app_appeal/draft_appeal.html',{'form':form})
        else:
            messages.warning(request,'One or all issue are awaiting approval from Tax Head')
        return redirect('runmastertemp',pk)

@login_required
def as_filed_appeal(request,pk):
    try:
        if Appellate_Appeal_Draft.objects.get(order__proceeding=pk) is not None:       
            if request.method=='POST':
                form = As_Filed_Appeal_Form(request.POST,request.FILES)
                if form.is_valid():
                    try:
                        instance=form.save(commit=False)
                        instance.created_by=User.objects.get(id=request.user.id)
                        instance.order = Order.objects.get(proceeding=pk)
                        instance.save()
                        messages.success(request,'As Filed Appeal Successfully Saved to database')
                        return redirect('payment',pk)
                    except:
                        messages.error(request,'Something Went Wrong, Pls Try Again')
            else:
                form = As_Filed_Appeal_Form()
            return render(request,'app_appeal/as_filed_appeal.html',{'form':form})
        else:
            messages.warning(request,'Draft Appeal for this order has not been sent')
    except:
        messages.warning(request,'There is no Draft Appeal against this order')
        return redirect('runmastertemp',pk)
        
def create_hearing_notice(request,pk):
    try:
        if Appellate_Appeal_Final.objects.get(order__proceeding=pk):
            if request.method=='POST':
                form = Hearing_Notice_Form(request.POST,request.FILES)
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.order = Order.objects.get(proceeding=pk)
                    instance.created_by= User.objects.get(id=request.user.id)
                    instance.save()
                    messages.success(request,'Hearing Notice Successfully Added to Database')
                    return redirect('runmastertemp',pk)
            else:
                form = Hearing_Notice_Form()
            return render(request,'app_appeal/create_hearing_notice.html',{'form':form})
        else:
            pass            
    except:
        messages.error(request,'As filed Appeal against this Hearing notice not uploaded')
    return redirect('runmastertemp',pk)

@login_required
def appeal_hearing(request,pk):
    pi = Hearing_Notice.objects.get(order__proceeding=pk)
    if App_Appeal_Hearing.objects.last() is None:
        la= pi.hearing_date
    else:
        la = App_Appeal_Hearing.objects.filter(order__proceeding=pk).last()
        la= la.next_date
    if request.method =='POST':
        form = Appeal_Hearing_Form(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.created_by=User.objects.get(id=request.user.id)
            instance.order = Order.objects.get(proceeding=pk)
            try:
                instance.save()
                messages.success(request,'Hearing Successfully updated..!!')
                return redirect('runmastertemp',pk)
            except:
                messages.error(request,'Something Went Wrong, Pls Try Again')
    else:
        initial = {'hearing_date':la}
        form = Appeal_Hearing_Form(initial=initial)
    return render(request,'app_appeal/appeal_hearing.html',{'form':form,'la':la})
                
        
@login_required
def appeal_order(request,pk):
    demand = Order.objects.get(proceeding=pk).total_demand
    if App_Appeal_Hearing.objects.filter(order__proceeding=pk).last().is_complete:
        if request.method =='POST':
            form = Appellate_Order_Form(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.created_by=User.objects.get(id=request.user.id)
                instance.order = Order.objects.get(proceeding=pk)
                try:
                    instance.save()
                    messages.success(request,'Appeal Order Successfully Saved to  database')
                    return redirect('view_additions',pk)
                except:
                    messages.error(request,'Something Went Wrong, Pls Try Again')
        else:
            form = Appellate_Order_Form()
        return render(request,'app_appeal/appellate_order.html',{'form':form,'demand':demand})
    else:
        messages.error(request,'Hearing in this matter is incomplete..!!')
    return redirect('runmastertemp',pk)

def view_additions(request,pk):#View edits order_additions for updating appeal results
    pi = Addition.objects.filter(order__proceeding=pk)
    return render(request,'app_appeal/view_additions.html',{'pi':pi,'pk':pk})    

@login_required
def appellate_order_details(request,pk,id):
    disp = tuple(Appellate_Order_Details.objects.filter(order__proceeding=pk).values_list('demand',flat=True))
    # print(disp)
    t_demand = Appellate_Order.objects.get(order__proceeding=pk).demand
    # print(t_demand)
    demand= check_total_additions(t_demand,*disp)
    # print(pk,demand)
    pi = Addition.objects.get(id=id)
    if request.method =='POST':
        form =Apellate_Order_Details_Form(request.POST)
        form1= Additions_Form_Edit(request.POST,instance=pi)
        if form.is_valid():
            try:
                instance= form.save(commit=False)
                instance.admitted_tax=instance.demand-instance.disputed_tax
                instance.created_by= User.objects.get(id=request.user.id)
                instance.order = Order.objects.get(proceeding=pk)
                instance.app_order = Appellate_Order.objects.get(order__proceeding=pk)
                instance.save()
                messages.success(request,'Data Save Successfully')
                return redirect('view_additions',pk)
            except:
                messages.error(request,'Something Went Wrong Pls Try Again')
    else:
        form = Apellate_Order_Details_Form()
        form1 = Additions_Form_Edit(instance=pi)
    return render(request,'app_appeal/appeal_order_detail.html',{'form':form,'form1':form1,'pk':pk,'demand':demand})

@login_required    
def payment(request,pk):
    add= tuple(Addition.objects.filter(order__proceeding=pk).values_list('disputed_additions',flat=True))
    adm= tuple(Addition.objects.filter(order__proceeding=pk).values_list('admitted_additions',flat=True))
    add = sum_addition(*add)    #sum disputed tax
    adm = sum_addition(*adm)    #sum admitted tax
    if request.method=='POST':
        form = Payment_Form(request.POST,request.FILES)
        if form.is_valid():
            try:
                instance=form.save(commit=False)
                instance.order= Order.objects.get(proceeding=pk)
                instance.created_by= User.objects.get(id=request.user.id)
                instance.save()
                messages.success(request,'Payment uploaded to database')
                return redirect('runmastertemp',pk)
            except:
                messages.error(request,'Something Went Wrong, Pls. Try Again')
    else:
        form = Payment_Form()
    return render(request,'app_appeal/payment.html',{'form':form,'add':add,'adm':adm})
        
def view_hearing_notice(request,pk):    
    notice = Hearing_Notice.objects.get(order__proceeding=pk)
    return render(request,'app_appeal/view_hearing_notice.html',{'notice':notice,'pk':pk})           

def view_hearing_data(request,pk):    
    notice = App_Appeal_Hearing.objects.filter(order__proceeding=pk)
    return render(request,'app_appeal/view_hearing_data.html',{'notice':notice,'pk':pk})           

def view_as_filed_appeal(request,pk):    
    notice = Appellate_Appeal_Final.objects.get(order__proceeding=pk)
    return render(request,'app_appeal/view_as_filed_appeal.html',{'notice':notice,'pk':pk})           

def view_appellate_order(request,pk):    
    notice = Appellate_Order.objects.get(order__proceeding=pk)
    return render(request,'app_appeal/view_appellate_order.html',{'notice':notice,'pk':pk})           

def view_appellate_order_details(request,pk):    
    notice = Appellate_Order_Details.objects.filter(order__proceeding=pk)
    return render(request,'app_appeal/view_appellate_order_details.html',{'notice':notice,'pk':pk})           


     

    

    
    
