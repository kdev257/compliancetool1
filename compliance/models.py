from django.db import models

# Create your models here.
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class RecentNews(models.Model):
    newsdate=models.DateField(default=date.today)
    newstext=models.CharField(max_length=100)

class State(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Unit(models.Model):
    unit_name=models.CharField(max_length=150)
    address=models.TextField(max_length=300)
    city = models.CharField(max_length=70)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    zipcode=models.IntegerField()
    def __str__(self):
        return f"{self.unit_name}"

class Act(models.Model):
    name = models.CharField(max_length=70)
    def __str__(self):
        return f"{self.name}"
    
class Advisor(models.Model):
    CAT_CHOICES=(
        ('1','Indirect Tax'),
        ('2','Direct Tax'),
        ('3','Custom'),
        ('4','Taxhead'),
    )
    advisor=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    tax_cat = models.CharField(choices=CAT_CHOICES,max_length=70,default='Indirect Tax' )
    def __str__(self):
        return f"{self.advisor}"
    
class TaxNews(models.Model):
    act = models.ForeignKey(Act,on_delete=models.CASCADE)
    newsdate= models.DateField(default=date.today)
    newstext=models.TextField(max_length=150)

class UserQueryNew(models.Model):
    CAT_CHOICES=(
        ('1','Indirect Tax'),
        ('2','Direct Tax'),
        ('3','Custom'),
    )    
    STATUS_CHOICES=(
        ('open','open'),
        ('replied','replied'),
        ('close','close'),
    )    
    user =models.ForeignKey(User,max_length=100,on_delete=models.CASCADE)    
    query_date=models.DateField(default=date.today) 
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)
    tax_cat=models.CharField(choices=CAT_CHOICES, max_length=70,default='Indirect Tax')
    act=models.ForeignKey(Act, on_delete=models.CASCADE,
    help_text='Pls Select the Act from drop down')
    advisor=models.ForeignKey(Advisor,on_delete=models.CASCADE)
    query = models.TextField(max_length=500,blank=False,default='Pls Explain the transaction in detail')
    upload = models.FileField(upload_to='media',max_length=254,default='no file')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='open')
    query_reply= models.TextField(max_length=500, blank=False,default='Reply Open')

    def __str__(self):
        return f"{self.user}"    

class TaxUserClass(models.Model):
    DESIGNATION_CHOICE=(
        ('Asst. Manager','Asst.Manager'),
        ('Manager','Manager'),
        ('Senior Manager','Senior Manager'),
        ('AGM','AGM'),
        ('GM','GM'),
        ('AVP','AVP'),
        ('VP','VP'),
        ('EVP','EVP'),
    )
    DEPARTMENT_CHOICE=(
        ('Finance','Finance'),
        ('Marketing','Marketing'),
        ('HR','HR'),
        ('Sales','Sales'),
        ('Export','Export'),
        ('External Affairs','External Affairs'),
        ('Legal','Legal'),
    )
    BAND_CHOICE=(
        ('1A','1A'),
        ('1A','1A'),
        ('2A','2A'),
        ('2B','2B'),
        ('3A','3A'),
        ('3B','3B'),
        ('4A','4A'),
        ('4B','4B'),
        ('5A','5A'),
        ('5B','5B'),
        ('5C','5C')
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    designation=models.CharField(choices=DESIGNATION_CHOICE, max_length=75,null=False,blank=False)
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    department=models.CharField(choices=DEPARTMENT_CHOICE,max_length=70)
    band = models.CharField(choices=BAND_CHOICE,max_length=10)
    

