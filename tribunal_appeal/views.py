from django.shortcuts import render,redirect
from django.contrib import messages
from compliance.models import Advisor
from django.contrib.auth.decorators import login_required
from idtlit.models import Order,Issue,User,Initial_Notice,ProposedAddition,Addition
from app_appeal.models import Appellate_Order,Appellate_Order_Details
from idtlit.functions import check_total_additions,sum_addition
from .forms import *
from app_appeal.forms import Apellate_Order_Details_Form,Apellate_Order_Edit_Form
from idtlit.forms import Additions_Form_Edit
from django.db.models import Sum
from .models import *
# Create your views here.
@login_required
def tribunal_home(request,pk): #This View triggers master template for appeal proceedings    
    try:
        adv =Advisor.objects.filter(advisor=request.user.id).exists()
    except:
        pass
    try:
        th =Advisor.objects.filter(tax_cat='4',advisor=request.user.id).exists()        
    except:
        pass
    try:
        pi = Appellate_Order.objects.get(order=pk)
    except:
        Appellate_Order.DoesNotExist
        pi=None
    try:
        notice = Tribunal_Hearing_Notice.objects.get(order=pk)
    except:
        Tribunal_Hearing_Notice.DoesNotExist
        notice = None    
    try:
        hearing = Tribunal_Appeal_Hearing.objects.filter(order=pk).last().hearing_date
    except:
        Tribunal_Appeal_Hearing.DoesNotExist
        hearing= None
    try:
        order= Tribunal_Order.objects.get(order=pk)
    except:
        Tribunal_Order.DoesNotExist
        order=None
    cash = Tribunal_Payment.objects.filter(order=pk) 
    pad = ProposedAddition.objects.filter(proceeding=pk).order_by('id')   
    addition = Addition.objects.filter(order__proceeding=pk).order_by('issue')
    aa = Appellate_Order_Details.objects.filter(order=pk).order_by('issue')
    ta = Tribunal_Order_Details.objects.filter(order=pk)    
    return render(request,('tribunal_appeal/tribunal_master_template.html'),{'pi':pi,'pk':pk,'adv':adv,'th':th,'notice':notice,'hearing':hearing,'order':order,'cash':cash,'pad':pad,'addition':addition,'aa':aa,'ta':ta})

@login_required
def tri_appeal_action(request,pk): 
    ''' This View show list of issue in order as uploaded by location to funtional head. The function mananger decided whether appeal is to be filed and recommend the action to tax head'''
    add = Appellate_Order_Details.objects.filter(order=pk)
    order = Appellate_Order.objects.get(order=pk).order 
    app_order = Appellate_Order.objects.get(order=pk).order_no         
    return render(request,"tribunal_appeal/tri_appeal_actions.html",{'add':add,'pk':pk,'order':order,'app_order':app_order})

@login_required
def view_appeal_action(request,pk): 
    ''' This View is similar to above but it is meant for tax head to approve the recommendation given by functional manager show list of issue in order as uploaded by location to funtional head duly recommended by for approval to tax head.'''
    add = Appellate_Order_Details.objects.filter(order=pk)     
    return render(request,"tribunal_appeal/view_appeal_action.html",{'add':add,'pk':pk,'add':add})

@login_required
def recommend_appeal_action(request,pk,id):
    '''Indirect Tax head recommend the action againt the order'''
    path=request.path
    path = path.split('/')
    # pk = int(path[3])      
    add = Appellate_Order_Details.objects.get(id=id)
    if Advisor.objects.filter(advisor=request.user.id).exists():
        if request.method =='POST':
            form = Recommend_Appeal_Action_Form(request.POST,instance=add)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.disputed_tax=instance.demand-instance.admitted_tax
                instance.recommended_by= User.objects.get(id=request.user.id)
                instance.save()
                return redirect('tri_appeal_action',pk)
        else:        
            form=Recommend_Appeal_Action_Form(instance=add)
        return render(request,'tribunal_appeal/recommend_appeal_actions.html',{'form':form,'pk':pk,'add':add})
    else:
        messages.error(request,'You are not authorized to perform this action')
    return redirect('tri_appeal_action',pk)

@login_required
def approve_appeal_action(request,pk,id):
    '''Tax head approve the action as recommended by functional head'''    
    path=request.path
    path = path.split('/')
    pk = int(path[3])    
    add = Appellate_Order_Details.objects.get(id=id)
    if add.is_recommended:
        if request.method =='POST':
            form = Approve_Appeal_Actions_Form(request.POST,instance=add)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.approved_by= User.objects.get(id=request.user.id)
                instance.save()
                return redirect('tri_view_appeal_action',pk)
        else:
            form=Approve_Appeal_Actions_Form(instance=add)
        return render(request,'tribunal_appeal/approve_appeal_action.html',{'form':form,'pk':pk,'add':add})
    else:
         messages.error(request,'This issue yet to be recommeded for action by Functional Head')
    return redirect('tri_view_appeal_action',pk)

@login_required       
def tribunal_draft_appeal(request,pk):
        approved =list(Appellate_Order_Details.objects.filter(order=pk).values_list('is_approved',flat=True))
        if not False in approved: 
            if request.method=='POST':
                form = Draft_Tribunal_Appeal_Form(request.POST,request.FILES)
                if form.is_valid():
                    try:
                        instance=form.save(commit=False)
                        instance.created_by=User.objects.get(id=request.user.id)
                        instance.order = Order.objects.get(id=pk)
                        instance.app_order= Appellate_Order.objects.get(order=pk)
                        instance.save()
                        messages.success(request,'Draft Appeal Successfully Saved to database')
                        return redirect('tribunal_home',pk)
                    except:
                        messages.error(request,'Something Went Wrong, Pls Try Again')
            else:
                form = Draft_Tribunal_Appeal_Form()
            return render(request,'tribunal_appeal/tribunal_appeal_draft.html',{'form':form})
        else:
            messages.warning(request,'One or all issue are awaiting approval from Tax Head')
        return redirect('tribunal_home',pk)

@login_required
def tribunal_as_filed_appeal(request,pk):
    try:
        if Tribunal_Appeal_Draft.objects.get(order=pk) is not None:       
            if request.method=='POST':
                form = As_Filed_Tribunal_Appeal_Form(request.POST,request.FILES)
                if form.is_valid():
                    try:
                        instance=form.save(commit=False)
                        instance.created_by=User.objects.get(id=request.user.id)
                        instance.order = Order.objects.get(proceeding=pk)
                        instance.app_order = Appellate_Order.objects.get(order=pk)
                        instance.save()
                        messages.success(request,'As Filed Appeal Successfully Saved to database')
                        return redirect('tribunal_payment',pk)
                    except:
                        messages.error(request,'Something Went Wrong, Pls Try Again')
            else:
                form = As_Filed_Tribunal_Appeal_Form()
            return render(request,'app_appeal/as_filed_appeal.html',{'form':form})
        else:
            messages.warning(request,'Draft Appeal for this order has not been sent')
        return redirect('tribunal_home',pk)
    except:
        messages.warning(request,'There is no Draft Appeal against this order')
    return redirect('tribunal_home',pk)
        
def create_hearing_notice(request,pk):
    try:
        if Tribunal_Appeal_Final.objects.get(order=pk):
            if request.method=='POST':
                form = Hearing_Notice_Form(request.POST,request.FILES)
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.order = Order.objects.get(id=pk)
                    instance.app_order = Appellate_Order.objects.get(order=pk)
                    instance.created_by= User.objects.get(id=request.user.id)
                    instance.save()
                    messages.success(request,'Hearing Notice Successfully Added to Database')
                    return redirect('tribunal_home',pk)
            else:
                form = Hearing_Notice_Form()
            return render(request,'app_appeal/create_hearing_notice.html',{'form':form})
        else:
            pass            
    except:
        messages.error(request,'As filed Appeal against this Hearing notice not uploaded')
    return redirect('tribunal_home',pk)

@login_required
def tribunal_appeal_hearing(request,pk):
    # hearing_date= Tribunal_Hearing_Notice.objects.get(order=pk).hearing_date
    # la= hearing_date.strftime('%d-%m-%Y')
    complete = Tribunal_Appeal_Hearing.objects.filter(order=pk).values_list('is_complete',flat=True).last()
    if not complete:        
        if Tribunal_Appeal_Hearing.objects.last() is None:
            la= Tribunal_Hearing_Notice.objects.get(order=pk).hearing_date
        else:
            la = Tribunal_Appeal_Hearing.objects.filter(order=pk).last().next_date            
        try:        
            if request.method =='POST':
                form = Tribunal_Appeal_Hearing_Form(request.POST,request.FILES)
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.created_by=User.objects.get(id=request.user.id)
                    instance.app_order = Appellate_Order.objects.get(order=pk)
                    instance.order = Order.objects.get(proceeding=pk)
                    try:
                        instance.save()
                        messages.success(request,'Hearing Successfully updated..!!')
                        return redirect('tribunal_home',pk)
                    except:
                        messages.error(request,'Something Went Wrong, Pls Try Again')
            else:
                form = Tribunal_Appeal_Hearing_Form()
            return render(request,'app_appeal/appeal_hearing.html',{'form':form,'la':la})
        except:
            messages.error(request,'There in no Hearing Scheduled for this Appeal')
        return redirect('tribunal_home',pk)
    else:
        messages.warning(request,'Hearing in this matter is already complete')
    return redirect('tribunal_home',pk)
    
@login_required
def tribunal_order(request,pk):
    demand = Appellate_Order.objects.get(order=pk).demand
    if Tribunal_Appeal_Hearing.objects.filter(order=pk).last().is_complete:
        if request.method =='POST':
            form = Trinunal_Order_Form(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.created_by=User.objects.get(id=request.user.id)
                instance.app_order = Appellate_Order.objects.get(order=pk)
                instance.order = Order.objects.get(id=pk)
                try:
                    instance.save()
                    messages.success(request,'Tribunal Order Successfully Saved to  database')
                    return redirect('view_appellate_additions',pk)
                except:
                    messages.error(request,'Something Went Wrong, Pls Try Again')
        else:
            form = Trinunal_Order_Form()
        return render(request,'app_appeal/appellate_order.html',{'form':form,'demand':demand})
    else:
        messages.error(request,'Hearing in this matter is incomplete..!!')
    return redirect('tribunal_home',pk)

def view_appellate_additions(request,pk):#View edits order_additions for updating appeal results
    pi = Appellate_Order_Details.objects.filter(order=pk)
    return render(request,'tribunal_appeal/view_appellate_additions.html',{'pi':pi,'pk':pk})    

@login_required
def tribunal_order_details(request,pk,id):
    disp = tuple(Tribunal_Order_Details.objects.filter(order=pk).values_list('demand',flat=True))       
    admitted_tax=Tribunal_Order_Details.objects.aggregate(Sum('admitted_tax')) 
    t_demand = Tribunal_Order.objects.get(order=pk).demand
    admitted_tax=admitted_tax['admitted_tax__sum']
    demand = t_demand-admitted_tax    
    demand= check_total_additions(demand,*disp)    
    pi = Appellate_Order_Details.objects.get(id=id)
    if request.method =='POST':
        form =Tribunal_Order_Details_Form(request.POST)
        form1= Apellate_Order_Edit_Form(request.POST,instance=pi)
        if form.is_valid():
            try:
                instance= form.save(commit=False)
                instance.disputed_tax=instance.demand-instance.admitted_tax
                instance.created_by= User.objects.get(id=request.user.id)
                instance.order = Order.objects.get(proceeding=pk)
                instance.app_order = Appellate_Order.objects.get(order=pk)
                instance.save()
                messages.success(request,'Data Save Successfully')
                return redirect('view_appellate_additions',pk)
            except:
                messages.error(request,'Something Went Wrong Pls Try Again')
    else:
        form = Tribunal_Order_Details_Form()
        form1 = Apellate_Order_Edit_Form(instance=pi)
    return render(request,'tribunal_appeal/tribunal_appeal_order_detail.html',{'form':form,'form1':form1,'pk':pk,'demand':demand})

@login_required    
def tribunal_payment(request,pk):
    add= tuple(Appellate_Order_Details.objects.filter(order=pk).values_list('demand',flat=True))
    adm= tuple(Appellate_Order_Details.objects.filter(order=pk).values_list('admitted_tax',flat=True))
    add = sum_addition(*add)    #sum disputed tax
    adm = sum_addition(*adm)    #sum admitted tax
    if request.method=='POST':
        form = Payment_Form(request.POST,request.FILES)
        if form.is_valid():
            try:
                instance=form.save(commit=False)
                instance.order= Order.objects.get(proceeding=pk)
                instance.app_order = Appellate_Order.objects.get(order=pk)
                instance.created_by= User.objects.get(id=request.user.id)
                instance.save()
                messages.success(request,'Payment uploaded to database')
                return redirect('tribunal_home',pk)
            except:
                messages.error(request,'Something Went Wrong, Pls. Try Again')
    else:
        form = Payment_Form()
    return render(request,'app_appeal/payment.html',{'form':form,'add':add,'adm':adm})
        
def view_tribunal_hearing_notice(request,pk):    
    notice = Tribunal_Hearing_Notice.objects.get(order=pk)
    return render(request,'tribunal_appeal/view_tribunal_hearing_notice.html',{'notice':notice,'pk':pk})           

def view_tribunal_hearing_data(request,pk):    
    notice = Tribunal_Appeal_Hearing.objects.filter(order=pk)
    return render(request,'tribunal_appeal/view_tribunal_hearing_data.html',{'notice':notice,'pk':pk})           

def view_tribunal_as_filed_appeal(request,pk):    
    notice = Tribunal_Appeal_Final.objects.get(order=pk)
    return render(request,'tribunal_appeal/view_as_filed_tribunal_appeal.html',{'notice':notice,'pk':pk})           

def view_tribunal_order(request,pk):    
    notice = Tribunal_Order.objects.get(order=pk)
    return render(request,'tribunal_appeal/view_tribunal_order.html',{'notice':notice,'pk':pk})           

def view_tribunal_order_details(request,pk):    
    notice = Tribunal_Order_Details.objects.filter(order=pk)
    return render(request,'tribunal_appeal/view_tribunal_order_details.html',{'notice':notice,'pk':pk})           


     

    

    
    
