from django.shortcuts import render,redirect
from django_q.tasks import async_task
from .forms import *
from . models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from compliancetool1.settings import EMAIL_HOST_USER
from django.conf import settings
from compliance.models import User,Advisor
from .functions import check_total_additions  
# from django.forms import modelformset_factory
# Create your views here.
def action(request,pk):
    path = request.path
    path = path.split('/')
    pk = int(path[3])
    pi = Initial_Notice.objects.get(proceeding=pk)
    notices = Initial_Notice.objects.filter(desired_date_of_reply__lt =timezone.now())            
    ap = Hearing.objects.filter(proceeding=pk).last()
    scn = ShowCauseNotice.objects.filter(proceeding=pk).last()
    try:
        order= Order.objects.get(proceeding=pk)
    except:
        Order.DoesNotExist
        order= None
    try:
        adv =Advisor.objects.filter(advisor=request.user.id).exists()
    except:
        pass
    try:
        th =Advisor.objects.filter(tax_cat='4',advisor=request.user.id).exists()        
    except:
        pass
    pad = ProposedAddition.objects.filter(proceeding=pk).order_by('id')    
    addition = Addition.objects.filter(order__proceeding=pk).order_by('issue')    
    return render(request,('idtlit/location_user_home.html'),{'pi':pi,'pk':pk,'ap':ap,'scn':scn,'order':order,'addition':addition,'pad':pad,'adv':adv,'th':th})

def view_proposed_additions(request,pk):
    path = request.path
    path = path.split('/')
    pk = int(path[3])
    pa = ProposedAddition.objects.filter(proceeding=pk)
    return render(request,'idtlit/view_proposed_additions.html',{'pa':pa,'pk':pk})

def appearance(request,pk):
    path = request.path
    path = path.split('/')
    pk = int(path[3])    
    pi = Initial_Notice.objects.get(proceeding=pk)
    if Hearing.objects.filter(proceeding=pk).last() is None:
        la= pi.date_of_appearance
    else:
        la = Hearing.objects.filter(proceeding=pk).last()
    if request.method =='POST':
        form= Hearing_Form(request.POST,request.FILES)
        if form.is_valid():                        
            hearing_date= form.cleaned_data['hearing_date']
            is_complete= form.cleaned_data['is_complete']
            was_effective = form.cleaned_data['was_effective']
            hearing_gist = form.cleaned_data['hearing_gist']
            next_date = form.cleaned_data['next_date']
            upload = form.cleaned_data['upload']
            try:
                hearing=Hearing(proceeding=Initial_Notice.objects.get(proceeding=pk),hearing_date =hearing_date,next_date=next_date,hearing_gist=hearing_gist,was_effective=was_effective,created_by=User.objects.get(id=request.user.id),is_complete=is_complete,upload=upload)
                hearing.save()
                messages.success(request,'Hearing updated successfully')               
                return redirect('action',pk)
            except:
                messages.error(request,'Something Went Wrong Pls Try Again')
    else:
        initial = {'hearing_date': la}         
        form= Hearing_Form(initial=initial)
    return render(request,('idtlit/appearance.html'),{'form':form,'la':la,'pi':pi,'pk':pk})

@login_required
def create_scn(request,pk):
    path = request.path
    path = path.split('/')
    pk = int(path[3])
    complete = Hearing.objects.filter(proceeding=pk).last()
    if complete.is_complete:             
        if request.method == 'POST':
            form = SCN_Form(request.POST,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.created_by= User.objects.get(id=request.user.id)
                instance.proceeding = Initial_Notice.objects.get(proceeding=pk)
                instance.save()
            return redirect('update_proposed_addition', pk=pk)
        else:            
            form=SCN_Form()            
        return render(request,'idtlit/create_scn.html',{'form':form})
    else:
        messages.error(request,'Hearing in this matter is not yet complete')
    return redirect('action',pk)

def update_proposed_additions(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    ta = ShowCauseNotice.objects.get(proceeding=pk)
    ta = ta.proposed_additions
    pad= tuple(ProposedAddition.objects.filter(proceeding=pk).values_list('proposed_addition',flat=True))    
    tp =check_total_additions(ta,*pad)    
    if request.method =='POST':                
        # proceeding = Initial_Notice.objects.get(proceeding=pk)        
        # created_by = User.objects.get(id=request.user.id)        
        form =Proposed_Additions_Form(request.POST)
        if form.is_valid():
            issue= form.cleaned_data['issue']
            proposed_addition=form.cleaned_data['proposed_addition']
            # try:
            addition = ProposedAddition(scn_ref=ShowCauseNotice.objects.filter(created_by=request.user.id).last(),proceeding=Initial_Notice.objects.get(proceeding=pk),issue=issue,proposed_addition=proposed_addition,created_by=User.objects.get(id=request.user.id))
            addition.save()            
            messages.success(request,'Proposed Addition Successfully save to data base..!!!')                        
            form= Proposed_Additions_Form()
            return redirect('update_proposed_addition',pk)
            # except:
                # messages.error(request,'Something went Wrong. Pls try again..!!')
    else:
        form = Proposed_Additions_Form
    return render(request,('idtlit/proposed_additions.html'),{'form':form,'ta':ta,'tp':tp})

def scn_reply_draft(request,pk):
       path=request.path
       path = path.split('/')
       pk = int(path[3])
       scn = ShowCauseNotice.objects.filter(proceeding=pk)
       if request.method =='POST':
           form = Reply_Scn_Draft_Form(request.POST,request.FILES)
           if form.is_valid():               
               comments = form.cleaned_data['comments']
               upload = form.cleaned_data['upload']
               proceeding=Initial_Notice.objects.get(proceeding=pk)
            #    created_by = request.user.id
               try:
                    reply = NoticeReplyDraft(proceeding=proceeding,comments=comments,upload=upload,created_by=User.objects.get(id=request.user.id),scn_ref=ShowCauseNotice.objects.filter(proceeding=pk).last())
                    reply.save()               
                    messages.success(request,'Draft reply Successfully uploaded')
                    return redirect('action',pk)
               except:
                     messages.error(request,'Something Went wrong. Pls try Again')
       else:
           form = Reply_Scn_Draft_Form()
       return render(request,'idtlit/reply_scn_draft.html',{'form':form,'scn':scn})

def scn_reply_final(request,pk):
       path=request.path
       path = path.split('/')
       pk = int(path[3])    
       scn = ShowCauseNotice.objects.filter(proceeding=pk).last()
       if request.method =='POST':
           form = Reply_Scn_Final_Form(request.POST,request.FILES)
           if form.is_valid():               
               reply_date= form.cleaned_data['reply_date']
               comment = form.cleaned_data['comment']
               upload = form.cleaned_data['upload']
               proceeding=Initial_Notice.objects.get(proceeding=pk)
            #    created_by = request.user.id
               try:
                    reply = NoticeReplyFinal(proceeding=proceeding,scn_ref=ShowCauseNotice.objects.filter(created_by=request.user.id).last(),reply_date=reply_date, comment=comment,upload=upload,created_by=User.objects.get(id=request.user.id))
                    reply.save()
                    messages.success(request,'Final reply Successfully uploaded')
                    return redirect('action', pk)
               except:
                     messages.error(request,'Something Went wrong. Pls try Again')
       else:
           initial = {'reply_date' :scn.reply_by_date}
           form = Reply_Scn_Final_Form(initial=initial)
       return render(request,'idtlit/reply_scn_final.html',{'form':form,'pk':pk,'scn':scn})

def order(request,pk):
       path=request.path
       path = path.split('/')
       pk = int(path[3])    
       if request.method =='POST':
           form = Order_Form(request.POST,request.FILES)
           if form.is_valid():               
               order_no = form.cleaned_data['order_no']
               order_date=form.cleaned_data['order_date']
               order_gist = form.cleaned_data['order_gist']
               total_demand=form.cleaned_data['total_demand']
               appeal_by_date=form.cleaned_data['appeal_by_date']
               uplaod = form.cleaned_data['upload']               
               try:
                order = Order(proceeding=Initial_Notice.objects.get(proceeding=pk),scn_ref=ShowCauseNotice.objects.filter(created_by=request.user.id).last(),order_no=order_no,order_date=order_date,order_gist=order_gist,total_demand=total_demand,appeal_by_date=appeal_by_date,upload=uplaod,created_by=User.objects.get(id=request.user.id))
                order.save()
                messages.success(request,'Order Successfully uploaded')
                return redirect('view_proposed_additions', pk)
               except:
                     messages.error(request,'Something Went wrong. Pls try Again')
       else:
           form = Order_Form()
       return render(request,'idtlit/order.html',{'form':form})
                
def additions(request,pk,id):
       path=request.path
       path = path.split('/')
       pk = int(path[3])
       order= Order.objects.get(proceeding=pk)
       ta = order.total_demand
       pa= ProposedAddition.objects.get(id=id)
       tpa = tuple( Addition.objects.filter(order__proceeding=pk).values_list('total_additions',flat=True))
       print(tpa)
       ba = check_total_additions(ta,*tpa)       
       if request.method== 'POST':           
           form = Additions_Form(request.POST)
           form1 = Proposed_Additions_Form_view(request.POST,instance=pa)
           if form.is_valid():
            #    try:
                instance=form.save(commit=False)
                instance.order = Order.objects.get(proceeding=pk)
                instance.created_by = User.objects.get(id=request.user.id)
                instance.save()
                messages.success(request,'Data Successfully uploaded to database')                
                return redirect('view_proposed_additions',pk)
            #    except:
                #    messages.error(request,'Something went wrong Pls. Try Again')
       
       else:
           form = Additions_Form()
           form1 = Proposed_Additions_Form_view(instance=pa)
       return render(request,'idtlit/addition.html',{'form':form,'form1':form1,'order':order,'pa':pa,'ta':ta,'ba':ba})

           
def location_user_home(request):
    return render(request,('idtlit/location_user_home.html'))

def create_notice(request):       
        created_by= request.user
        if request.method == 'POST':
            form = Initial_Notice_Form(request.POST,request.FILES)
            if form.is_valid():            
                proceeding_type=form.cleaned_data['proceeding_type']
                notice_no = form.cleaned_data['notice_no']
                notice_date =form.cleaned_data['notice_date']
                notice_type = form.cleaned_data['notice_type']
                unit= form.cleaned_data['unit']
                authority=form.cleaned_data['authority']
                year = form.cleaned_data['year']
                act = form.cleaned_data['act']
                description = form.cleaned_data['description']
                advisor = form.cleaned_data['advisor']
                production_of_books= form.cleaned_data['production_of_books']
                reply_sought = form.cleaned_data['reply_sought']
                desired_date_of_reply= form.cleaned_data['desired_date_of_reply']
                appearance_sought= form.cleaned_data['appearance_sought'] 
                date_of_appearance= form.cleaned_data['date_of_appearance']    
                upload = form.cleaned_data['upload']
                try:
                    notice =Initial_Notice(proceeding_type=proceeding_type,notice_no=notice_no,notice_date=notice_date,notice_type=notice_type,unit=unit,authority=authority,year=year, act=act,description=description,advisor=advisor, production_of_books=production_of_books,reply_sought=reply_sought,desired_date_of_reply=desired_date_of_reply,appearance_sought=appearance_sought,date_of_appearance=date_of_appearance,upload=upload,created_by=created_by)
                    notice.save()                
                    messages.success(request, 'Notice Created Successfully')                    
                    return redirect('view_notice_location_user')
                except: 
                    messages.error(request,'Something went wrong Please try again')
                return redirect('view_notice_location_user')
        else:            
            form=Initial_Notice_Form()
        return render(request,'idtlit/create_notice.html',{'form':form})

def show_notice_location(request):    
    notice_data = Initial_Notice.objects.filter(created_by=request.user)
    return render(request,('idtlit/notice_data.html'),{'notice_data':notice_data})

def show_notice_advisor(request):
    taxhead= Advisor.objects.get(tax_cat='4')
    try:    
        if taxhead.advisor.id==request.user.id:
            notice_data= Initial_Notice.objects.all()
        else:
            notice_data = Initial_Notice.objects.filter(advisor=request.user.id)
    except:
        pass        
    return render(request,('idtlit/notice_data_advisor.html'),{'notice_data':notice_data,})

def update_notice(request,pk):
    pi = Initial_Notice.objects.get(proceeding_id=pk)
    if request.method == 'POST':
        form = Initial_Notice_Form(request.POST,request.FILES,instance=pi)
        if form.is_valid():
            form.save()
    else:
        pi = Initial_Notice.objects.get(proceeding_id=pk)
        form =Initial_Notice_Form(instance=pi)
    return render(request,('idtlit/update_notice.html'),{'form':form})

def delete_notice(request,pk):
    if request.user.is_authenticated:
        pi = Initial_Notice.objects.get(proceeding_id=pk)
        pi.delete()
        return redirect('view_notice_location_user/')

def new_notice(request):
    return render(request,'idtlit/new_notice_form.html')

def view_notice(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    return render(request,'idtlit/view_notice.html',{'notice_data':notice_data,'pk':pk})


def view_hearing(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    adj_data = Hearing.objects.filter(proceeding=pk)
    return render(request,'idtlit/appearance_data.html',{'notice_data':notice_data,'pk':pk,'adj_data':adj_data})

def view_Scn(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    scn_data = ShowCauseNotice.objects.filter(proceeding=pk)
    return render(request,'idtlit/scn_data.html',{'notice_data':notice_data,'pk':pk,'scn_data':scn_data})

def view_Scn_Reply_draft(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    scn_data = NoticeReplyDraft.objects.filter(proceeding=pk)
    return render(request,'idtlit/scn_reply_draft.html',{'notice_data':notice_data,'pk':pk,'scn_data':scn_data})

def view_Scn_Reply_Final(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    scn_data = NoticeReplyFinal.objects.filter(proceeding=pk)        
    return render(request,'idtlit/scn_reply_final.html',{'notice_data':notice_data,'pk':pk,'scn_data':scn_data})

def view_assessment_order(request,pk):
    path=request.path
    path = path.split('/')
    pk = int(path[3])
    notice_data = Initial_Notice.objects.get(proceeding=pk)
    order = Order.objects.get(proceeding=pk)        
    return render(request,'idtlit/view_assessment_order.html',{'notice_data':notice_data,'pk':pk,'order':order})

def test_code(request):
    # hearings= Hearing.objects.all().distinct()
    d_hearing =tuple(Hearing.objects.values_list('proceeding').distinct().order_by('proceeding'))
    for d in d_hearing:
        complete= Hearing.objects.filter(proceeding=d).last()       
        if complete.is_complete:
            pass
        else:
           print(complete.proceeding_id,complete.next_date)
    return render(request,'idtlit/test.html')


      
    