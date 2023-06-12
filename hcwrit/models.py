from django.db import models
from compliance.models import Advisor,User
from idtlit.models import Order
# Create your models here.
class Recommend_Writ(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE)
    reason = models.TextField(max_length=500,verbose_name='Writ Justification',help_text='Pls explain the reasons for filing writ in 500 words max')
    is_recommended = models.BooleanField(default=False)
    recommended_by= models.ForeignKey(Advisor,on_delete=models.CASCADE,related_name='recommender')
    is_approved =  models.BooleanField(default=False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE)
    approver_comment= models.TextField(max_length=300,blank=True,null=True)
    created = models.DateTimeField('Created On',auto_now=True)    
    updated = models.DateTimeField('Update On',auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='intiator')

    def __str__(self):
        return f'{self.order} {self.order.order_date}'
