from django.db import models
from django.db.models import Q
from datetime import date
from datetime import datetime,timezone,timedelta
from compliance.models import Unit,Act,User,Advisor
from django.utils import timezone
import os
# from django.urls import reverse
# Create your models here.

def user_directory_path(instance,filename):
    # ext = filename.split('.')[-1]
    filename= '{}'.format(filename,)
    return os.path.join (str(instance.proceeding),filename)
class TaxJurisdiction(models.Model):
    name = models.CharField(max_length=50)
    adress1 = models.CharField(max_length=50)
    adress2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode= models.CharField(max_length=10)
    phone_number= models.CharField(max_length=10,blank=True,null=True)    
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # Other fields
    def __str__(self):
        return f'{self.name}|{self.unit}'
    
class Issue(models.Model):
    description = models.CharField(max_length=50,blank=True,unique=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.description}'
    
    

class Initial_Notice(models.Model):
    PROCEEDING_TYPE_CHOICES=(
        ('Assessment','Assessment'),
        ('Re-Assessment','Re-Assessment'),
        ('Investigation','Investigation'),
        ('search Seizure','Search Seizure'),
        ('Survey','Survey'),
        ('Pre-Show_Cause_Notice','Pre-Show_Cause_Notice'),
        ('Other','Other')
    )
    YEAR_CHOICES = (
        ('2005-06','2005-06'),
        ('2006-07','2006-07'),
        ('2007-08','2007-08'),
        ('2008-09','2008-09'),
        ('2009-10','2009-10'),
        ('2010-11','2010-11'),
        ('2011-12','2011-12'),
        ('2012-13','2012-13'),
        ('2013-14','2013-14'),
        ('2014-15','2014-15'),
        ('2015-16','2015-16'),
        ('2016-17','2016-17'),
        ('2017-18','2018-19'),
        ('2019-20','2019-20'),
        ('2020-21','2020-21'),
        ('2021-22','2021-22'),
        ('2022-23','2022-23'),
        ('2023-24','2023-24'),
        ('2024-25','2024-25'),
        
    )
    NOTICE_CHOICES=(
        ('Initiation Notice','Initiation Notice'),        
        ('Scrutiny Notice','Scrutiny Notice'),
        ('Notice Seeking Information','Notice Seeking Information'),        
        ('Other Notice','Other Notice'),
    )
    proceeding = models.AutoField(primary_key=True)
    proceeding_type = models.CharField(max_length=50,choices=PROCEEDING_TYPE_CHOICES)
    notice_no = models.CharField(max_length=50)
    notice_date = models.DateField()    
    notice_type = models.CharField(choices=NOTICE_CHOICES,max_length=100)
    unit= models.ForeignKey(Unit,on_delete=models.CASCADE,blank=True,null=True)
    authority=models.ForeignKey(TaxJurisdiction,on_delete=models.CASCADE)
    year = models.CharField(max_length=20,choices=YEAR_CHOICES,verbose_name='Financial Year',help_text='Pls Enter the Financial Year')
    act = models.ForeignKey(Act,on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Notice Gist', max_length=500,help_text='Pls Enter Gist of Notice')
    advisor = models.ForeignKey(Advisor,on_delete=models.CASCADE,default=1,blank=True,null=True)
    production_of_books= models.BooleanField(default=True,help_text='Pls click if proudction of books and evidence is sought in the notice')
    reply_sought = models.BooleanField(default=True,help_text='Pls click if reply is sought in the notice')
    desired_date_of_reply= models.DateField(blank=True,null=True,help_text='Pls leave blank if reply is not sought')
    appearance_sought= models.BooleanField(default=True,help_text='Pls Click if Authority has sought your appeanrance in the matter')
    date_of_appearance= models.DateField(blank=True,null=True,help_text='Pls Enter date of appearance as sought in the Notice')    
    upload = models.FileField(help_text='Pls upload copy of Notice here',max_length=100)
    status = models.CharField(max_length=20,default='Open')
    created = models.DateTimeField('Created On',auto_now_add=True)    
    updated = models.DateTimeField('Update On',auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


    def __str__(self):
        return f"{self.unit}/{self.notice_no}"     
      

class ShowCauseNotice(models.Model):
    proceeding= models.ForeignKey(Initial_Notice,on_delete=models.CASCADE)
    scn_no = models.CharField(max_length=50)
    scn_date = models.DateField()
    scn_gist=models.TextField(max_length=200)    
    reply_by_date = models.DateField()    
    proposed_additions=models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)    
    upload= models.FileField(verbose_name='Upload Documents',blank=True,null=True,help_text='Pls upload SCN')
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default=5)
    
    def __str__(self):
        return f'{self.scn_no}/{self.scn_date}'

class Hearing(models.Model):
    proceeding= models.ForeignKey(Initial_Notice,on_delete=models.CASCADE)
    hearing_date = models.DateField()
    was_effective= models.BooleanField(default=False,help_text='Pls upload copy of adjounment letter if not effective')
    hearing_gist = models.TextField(max_length=200,blank=True,help_text='Pls Enter Brief of hearing')
    is_complete= models.BooleanField(default=False)
    next_date = models.DateField(help_text='Pls. enter next date if hearing in not complete', blank=True,null=True)
    upload = models.FileField(help_text='Pls upload as filed written submission,if filed',blank=True)
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hearing_date}'


class ProposedAddition(models.Model):
    proceeding= models.ForeignKey(Initial_Notice,on_delete=models.CASCADE)
    scn_ref = models.ForeignKey(ShowCauseNotice,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE,blank=True,null=True)    
    proposed_addition = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Updated On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default=5)
    def __str__(self):
        return f"{self.issue}|{self.proposed_addition}"
    

class NoticeReplyDraft(models.Model):    
    proceeding= models.ForeignKey(Initial_Notice, on_delete=models.CASCADE)
    scn_ref = models.ForeignKey(ShowCauseNotice,on_delete=models.CASCADE,related_name='draftreply')
    comments=models.TextField(max_length=200,help_text='Pls enter comments if any',blank=True,null=True)   
    upload = models.FileField(verbose_name='Upload Draft Reply') 
    created = models.DateTimeField('Created On',auto_now_add=True)    
    updated = models.DateTimeField('Update On',auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default=5)

    def __str__(self):
        return f'{self.scn_ref}'
    

class NoticeReplyFinal(models.Model):    
    proceeding = models.ForeignKey(Initial_Notice, on_delete=models.CASCADE)
    scn_ref = models.ForeignKey(ShowCauseNotice,on_delete=models.CASCADE,related_name='noticereply')
    reply_date= models.DateField(verbose_name='Pls Enter date of Filing reply' )
    comment=models.TextField(max_length=100,help_text='Pls enter anything relevant')   
    upload = models.FileField(verbose_name='Upload Acknowledged Reply' ) 
    created = models.DateTimeField('Created On',auto_now_add=True)    
    updated = models.DateTimeField('Update On',auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default=5)

    def __str__(self):
        return f"{self.scn_ref}"

class Order(models.Model):
    proceeding = models.OneToOneField(Initial_Notice, on_delete=models.CASCADE,default=None)
    scn_ref = models.ForeignKey(ShowCauseNotice,on_delete=models.CASCADE,related_name='Order')    
    order_no= models.CharField(max_length=100)
    order_date=models.DateField(default=datetime.today)
    order_gist= models.TextField(max_length=500)    
    total_demand = models.DecimalField(verbose_name='Impugned Demand',max_digits=20,decimal_places=2,default=0)    
    appeal_by_date=models.DateField(verbose_name='Last date of filing appeal',blank=True)    
    upload = models.FileField(verbose_name='Upload Order')    
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order_no}"
   
    # Other fields

class Addition(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)    
    total_additions = models.PositiveIntegerField(default=0)
    admitted_additions=models.PositiveIntegerField(default=0)
    disputed_additions=models.PositiveIntegerField(default=0)
    is_appealed = models.BooleanField(verbose_name='Whether Appealed',default=False)
    is_recommended= models.BooleanField(verbose_name='Recommend',default=False,help_text='Pls chech the box to recommend the actions')
    is_approved = models.BooleanField(verbose_name='Approve',default=False,help_text='By checking the appove option you are consenting filing of appeal/payment of admitted tax')
    approval_reason = models.CharField(max_length=200,verbose_name='Reason',default='Pls give reason for appeal/admiting the tax')
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creatror')
    recommended_by =models.ForeignKey(User,on_delete=models.CASCADE,related_name='Recommender',blank=True,null=True)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Approver',blank=True,null=True)
 

    def __str__(self):
        return f"{self.issue}|{self.disputed_additions}"



    


     