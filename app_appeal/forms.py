from django import forms 
from idtlit.models import Order
from .models import *
class Update_Appeal_Action_Form(forms.ModelForm):
    class Meta:
        model = Addition
        fields = 'order','issue','total_additions','admitted_additions','disputed_additions','approval_reason','is_appealed','is_recommended'

        widgets={
            'order': forms.Select(attrs={'class':'form-control'}),            
            'issue':forms.Select(attrs={'class':'form-control'}),            
            'total_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'admitted_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'disputed_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'approval_reason': forms.TextInput(attrs={'class':'form-control'}),
            'is_appealed':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_recommended':forms.CheckboxInput(attrs={'class':'form-control'}),
                        
 }

class Approve_Appeal_Actions_Form(forms.ModelForm):
     class Meta:
        model = Addition
        fields = 'order','issue','total_additions','admitted_additions','disputed_additions','approval_reason','is_appealed','is_recommended','is_approved',

        widgets={
            'order': forms.Select(attrs={'class':'form-control'}),            
            'issue':forms.Select(attrs={'class':'form-control'}),            
            'total_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'admitted_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'disputed_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'is_appealed':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_recommended':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_approved':forms.CheckboxInput(attrs={'class':'form-control'}),
                        
        }


class Draft_Appeal_Form(forms.ModelForm):
    class Meta:
        model = Appellate_Appeal_Draft
        fields = 'comments','upload' 
        widgets={            
            'comments':forms.Textarea(attrs={'class':'form-control','rows':3,'columns':50}),
                        
        }

class As_Filed_Appeal_Form(forms.ModelForm):
    class Meta:
        model = Appellate_Appeal_Final
        fields ='file_date','comments','upload' 
        widgets={     
            'file_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),       
            'comments':forms.Textarea(attrs={'class':'form-control','rows':4,'columns':50}),
            'upload' : forms.ClearableFileInput(attrs={'class':'form-control'})
     }

class Hearing_Notice_Form(forms.ModelForm):
    class Meta:
        model = Hearing_Notice
        fields = 'notice_no','notice_date','hearing_date','upload'
        widgets={
            'notice_no': forms.TextInput(attrs={'class':'form-control'}),
            'notice_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'hearing_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'upload' : forms.ClearableFileInput(attrs={'class':'form-control'})
        }

class Appeal_Hearing_Form(forms.ModelForm):     
    class Meta:
        model = App_Appeal_Hearing
        fields = 'hearing_date','was_effective','hearing_gist','is_complete','next_date','upload'
        widgets={            
            'hearing_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'was_effective': forms.CheckboxInput(attrs={'class':'form-control'}),
            'hearing_gist': forms.Textarea(attrs={'class':'form-control','rows': 4,'column':50}),
            'is_complete':forms.CheckboxInput(attrs={'class':'form-control'}),
            'next_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'upload':forms.ClearableFileInput(attrs={'class':'form-control'})
     } 
    
class Appellate_Order_Form(forms.ModelForm):
    class Meta:
        model = Appellate_Order
        fields = 'order_no','order_date','order_gist','demand','outcome',   'next_appeal_by_date','upload'

        widgets={
            'order_no':forms.TextInput(attrs={'class':'form-control'}),            
            'order_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'order_gist': forms.Textarea(attrs={'class':'form-control','rows': 3,'column':50}),
            'was_effective': forms.CheckboxInput(attrs={'class':'form-control'}),
            'demand':forms.NumberInput(attrs={'class':'form-control'}),
            'outcome':forms.Select(attrs={'class':'form-control'}),
            'next_appeal_by_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'upload' : forms.ClearableFileInput(attrs={'class':'form-control'})
     } 

class Apellate_Order_Details_Form(forms.ModelForm):
    class Meta:
        model =Appellate_Order_Details
        fields = 'issue','demand','disputed_tax','is_disputed','reason','is_remanded',

        widgets={            
            'issue':forms.Select(attrs={'class':'form-control'}),
            'demand':forms.NumberInput(attrs={'class':'form-control'}),
            'disputed_tax':forms.NumberInput(attrs={'class':'form-control'}),
            'reason':forms.Textarea(attrs={'class':'form-control'}),
            'is_disputed':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_remanded':forms.CheckboxInput(attrs={'class':'form-control'}),
        }
class Apellate_Order_Edit_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):     
            super(Apellate_Order_Edit_Form, self).__init__(*args, **kwargs)
            self.fields['issue'].disabled = True                       
            self.fields['disputed_tax'].disabled = True
    class Meta:
        model =Appellate_Order_Details
        fields = 'issue','disputed_tax'

        widgets={            
            'issue':forms.Select(attrs={'class':'form-control'}),
            'disputed_tax':forms.NumberInput(attrs={'class':'form-control'}),
        }
            
class Payment_Form(forms.ModelForm):
    class Meta:
        model = Payment
        fields= 'payment_type','challan_no','challan_date','tax','interest','penalty','upload'
        widgets={
            'payment_type':forms.Select(attrs={'class':'form-control'}),
            'challan_no' : forms.TextInput(attrs={'class':'form-control'}),
            'challan_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'addition':forms.Select(attrs={'class':'form-control'}),
            'tax':forms.NumberInput(attrs={'class':'form-control'}),
            'interest':forms.NumberInput(attrs={'class':'form-control'}),
            'penalty':forms.NumberInput(attrs={'class':'form-control'}),
            'is_disputed':forms.CheckboxInput(attrs={'class':'form-control'}),
        }