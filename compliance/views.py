from django.shortcuts import render
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import RecentNewsForm,TaxNewsForm,UserQueryForm,UserQueryReplyForm,AuthenticationForm,CreateUserForm,UserProfileForm
from .models import Advisor, RecentNews,TaxNews,UserQueryNew,TaxUserClass,Act,Unit
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def userloginview(request):
    if request.method=='POST':
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['username']
            pw =fm.cleaned_data['password']
            user=authenticate(username=name,password=pw)
            if user is not None:
                login(request,user)
                messages.success(request,(f'Login Successful...Welcome {user}'))
                # if user.is_authenticated:
                #     return HttpResponseRedirect('home')
                user=User.objects.filter(username=user)
                for u in user:
                    user_id=u.id
                    # print(u.id)
                    if TaxUserClass.objects.filter(user_id=user_id).exists():
                        return HttpResponseRedirect('/home/')
                    else:
                        return HttpResponseRedirect('/userprofile/')
    else:
        fm=AuthenticationForm()
    return render(request,'compliance/userlogin.html',{'form':fm}) 

def userprofile(request):    
    if request.user.is_authenticated:
        if request.method =='POST':
            user = User.objects.get(username=request.user)
            id=user.id
            fm=UserProfileForm(request.POST)
            if fm.is_valid():
                designation=fm.cleaned_data['designation']
                department=fm.cleaned_data['department']
                band=fm.cleaned_data['band']
                unit=fm.cleaned_data['unit']
                profile=TaxUserClass(user_id=id,designation=designation,department=department,band=band,unit=unit)
                profile.save()
                return HttpResponseRedirect('/home/')
        else:        
            fm = UserProfileForm()
        return render(request,'compliance/userprofile.html',{'form':fm})
    else:
        return HttpResponseRedirect('/')

def homepage(request):    
    if request.user.is_authenticated:
        news= RecentNews.objects.all()
        tnews=TaxNews.objects.all()
        return render(request,'compliance/base.html',{'news':news,'tnews':tnews})
    else:
        return HttpResponseRedirect('/')

def recentnews(request):
    if request.method=='POST':
        fm = RecentNewsForm(request.POST)
        if fm.is_valid():
            fm.save() 
            fm=RecentNewsForm()          
    else:
        user =Advisor.objects.filter(advisor=request.user).exists()        
        if user == True:
            fm=RecentNewsForm()
        else:
            message='<h3>Ooooo..Sooorry..You are not authorized to perform this action</h3>'
            return HttpResponse(message)
    return render(request,'compliance/recentnews.html',{'form':fm})
        
def taxnews(request):
    if request.method=='POST':
        fm= TaxNewsForm(request.POST)
        if fm.is_valid():
            res=fm.save()
    else:
        fm=TaxNewsForm()
    return render(request,'compliance/taxnews.html',{'form':fm})

def advisory(request):
    if request.method=="POST":
        user=User.objects.get(username=request.user)
        print(user.email)
        unit=TaxUserClass.objects.get(user_id=user.id)          
        fm=UserQueryForm(request.POST,request.FILES)
        if fm.is_valid():
            querydate=fm.cleaned_data['query_date']
            act=fm.cleaned_data['act']
            taxcat=fm.cleaned_data['tax_cat']
            query1=fm.cleaned_data['query']
            upload=fm.cleaned_data['upload']
            advisor=fm.cleaned_data['advisor']
            query=UserQueryNew(user_id=user.id,unit_id=unit.unit_id,query_date=querydate,act=act,tax_cat=taxcat,query=query1,upload=upload,advisor=advisor,status='Open')
            query.save()
            print(query)            
            send_mail(subject=f'Intimation for New Query in litigation tool by {user.username}',message=query1,from_email=user.email,recipient_list=("shrma.kdev257@gmail.com",),fail_silently=False)                
            messages.success(request,'Query Submitted Successfully')
    else:
        fm=UserQueryForm()
    queries= UserQueryNew.objects.filter(user=request.user).exclude(status='closed')
    return render(request,'compliance/advisory.html',{'form':fm,'queries':queries})

def updatequery(request,id):
    if request.method == 'POST':
        pi = UserQueryNew.objects.get(pk=id)
        fm = UserQueryForm(request.POST, instance=pi) 
        if fm.is_valid():
            pi.status='Open'
            fm.save()        
    else:
        pi= UserQueryNew.objects.get(pk=id)
        if pi.status=='Open' or pi.status=='Replied':
            fm= UserQueryForm(instance=pi)
        else:
            message ='You Cannot update a Closed Query'
            return HttpResponse(message)
    return render(request,'compliance/updatequery.html',{'form':fm})

def closequery(request,id):
    pi = UserQueryNew.objects.get(pk=id)
    pi.status='Closed'
    pi.save()
    return HttpResponseRedirect('/advisory/')
    
def deletequery(request,id):
    pi = UserQueryNew.objects.get(pk=id)
    if pi.status=='Open':
        pi.delete()
        return render(request,'compliance/delete.html')
    else:
        massage= '<h3>Oooo..Sorry..You can not delete a replied query</h3>'
        return HttpResponse(massage)

def showquerydata(request):
    user= request.user
    advisor =User.objects.filter(username=user)
    for a in advisor:
        id=a.id
        data = UserQueryNew.objects.filter(advisor_id=id).exclude(status='Closed')
        return render(request,'compliance/showquery.html',{'data':data})
    
def queryreply(request,id):
    if request.method == 'POST':
        pi = UserQueryNew.objects.get(pk=id)
        fm=UserQueryReplyForm(request.POST, instance=pi)
        if fm.is_valid():
            pi.status ='Replied'
            fm.save()            
    else:        
        pi = UserQueryNew.objects.get(pk=id)
        fm = UserQueryReplyForm(instance=pi)
    return render(request,'compliance/replyquery.html',{'form':fm})

def createuserview(request):
    if request.method=='POST':
        fm= CreateUserForm(request.POST)
        if fm.is_valid():
            fm.save()
        return HttpResponseRedirect('/')    
    else:
        fm = CreateUserForm()
    return render(request,'compliance/usercreation.html',{'form':fm})

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')        
