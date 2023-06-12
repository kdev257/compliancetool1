from django.db import models
from idtlit.models import Order,User,Issue,Addition
# Create your models here.

class Appellate_Appeal_Draft(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comments = models.TextField(max_length=300,verbose_name='Pls write Message to location user',blank=True)
    upload = models.FileField()
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order}/{self.order__order_date}'

class Appellate_Appeal_Final(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file_date= models.DateField(verbose_name='Appeal File Date')
    comments = models.TextField(max_length=300,verbose_name='Write a message to Advisor',blank=True)        
    upload = models.FileField()
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order}/{self.order__order_date}'

class Payment(models.Model):
    PAYMENT_CHOICES=(
        ('Pre-Deposit','Pre-Deposit'),
        ('Admitted_Tax','Admitted_Tax'),
        ('DRC-03','DRC-03'),
        ('Interest','Interest'),
        ('Penalty','Penalty'),
    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_type= models.CharField(max_length=50,choices=PAYMENT_CHOICES)
    challan_no  = models.CharField(max_length=50)
    challan_date= models.DateField()
    tax = models.PositiveIntegerField(default=0)
    interest=models.PositiveIntegerField(default=0)
    penalty = models.PositiveIntegerField(default=0)
    upload = models.FileField()
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.challan_no}/{self.challan_date}"

class Hearing_Notice(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    notice_no = models.CharField(max_length=50)
    notice_date = models.DateField()
    hearing_date = models.DateField()
    upload = models.FileField()
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

class App_Appeal_Hearing(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    hearing_date = models.DateField()
    was_effective= models.BooleanField(default=False,help_text='Pls upload copy of adjounment letter if not effective')
    hearing_gist = models.TextField(max_length=200,blank=True,help_text='Pls Enter Brief of hearing')
    is_complete= models.BooleanField(default=False)
    next_date = models.DateField(help_text='Pls. enter next date if hearing in not complete', blank=True,null=True)
    upload = models.FileField(help_text='Pls upload as filed written submission,if filed',blank=True,null=True)
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order}/{self.hearing_date}'

class Appellate_Order(models.Model):
    OUTCOME_CHOICE=(
        ('Allowed','Allowed'),
        ('Rejected','Rejected'),
        ('Partly_Allowed','Partly Allowed'),
        ('Remand Back','Remand Back')
    )
    order= models.ForeignKey(Order,on_delete=models.CASCADE)
    order_no = models.CharField(max_length=50,help_text='Pls Enter Order No')
    order_date = models.DateField()
    order_gist = models.TextField(max_length=300,help_text='Pls enter summary of order')
    demand = models.PositiveIntegerField('Impugned balance demand')
    outcome = models.CharField(max_length=50,choices=OUTCOME_CHOICE)
    next_appeal_by_date= models.DateField(verbose_name='2nd appeal limitation Date')
    upload = models.FileField(help_text='Pls upload Copy of Order')
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order_no}/{self.order_date}'
    
# class Appellate_Order_Details(models.Model):
#     order = models.ForeignKey(Appellate_Order,on_delete=models.CASCADE)
#     issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
#     demand = models.PositiveIntegerField(default=0)
#     disputed_tax = models.PositiveIntegerField(default=0,verbose_name='Balance Disputed Tax')
#     admitted_tax = models.PositiveIntegerField(default=0,verbose_name='Balance Disputed Tax')
#     is_disputed= models.BooleanField(default=False)
#     is_remanded = models.BooleanField(default=False)
#     created = models.DateTimeField('Created On',auto_now=True)    
#     updated = models.DateTimeField('Update On',auto_now_add=True)
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.order}/{self.order__order_date}'
    
class Appellate_Order_Details(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    app_order= models.ForeignKey(Appellate_Order,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
    demand = models.PositiveIntegerField(default=0)
    disputed_tax = models.PositiveIntegerField(default=0,verbose_name='Balance Disputed Tax')
    admitted_tax = models.PositiveIntegerField(default=0,verbose_name='Admitted Tax')
    is_disputed= models.BooleanField(default=False)
    is_remanded = models.BooleanField(default=False)
    reason = models.TextField(max_length=200,verbose_name='Reason for Demand',default='Pls give reason of demand')
    is_recommended= models.BooleanField(default=False)
    reco_reason = models.CharField(max_length=100,default='Write recommendation reason here')
    is_approved = models.BooleanField(default=False)
    approval_reason = models.CharField(max_length=100,default='Pls. write approval reason here ')
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering= ['issue']

    


    def __str__(self):
        return f'{self.order}/{self.order.order_date}'

# class Appellate_Order_Details_new(models.Model):
#     order = models.ForeignKey(Order,on_delete=models.CASCADE)
#     app_order= models.ForeignKey(Appellate_Order,on_delete=models.CASCADE)
#     issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
#     demand = models.PositiveIntegerField(default=0)
#     disputed_tax = models.PositiveIntegerField(default=0,verbose_name='Balance Disputed Tax')
#     admitted_tax = models.PositiveIntegerField(default=0,verbose_name='Balance Disputed Tax')
#     is_disputed= models.BooleanField(default=False)
#     is_remanded = models.BooleanField(default=False)
#     reason = models.TextField(max_length=200,verbose_name='Reason for Demand',default='Pls give reason of demand')
#     created = models.DateTimeField('Created On',auto_now=True)    
#     updated = models.DateTimeField('Update On',auto_now_add=True)
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE)

# #     def __str__(self):
# #         return f'{self.order}/{self.order__order_date}'
