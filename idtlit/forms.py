from django import forms
from django.contrib import admin
# from django.forms import formse
from .models import *
from django.db.models import Q

class Initial_Notice_Form(forms.ModelForm):
    class Meta:
        model = Initial_Notice 
        fields = ('proceeding_type','notice_no','notice_date','notice_type','unit','authority','year','act','description','advisor','production_of_books','reply_sought','desired_date_of_reply','appearance_sought','date_of_appearance','upload')
        
        widgets={
            'proceeding_type': forms.Select(attrs={'class':'form-control'}),
            'notice_no' : forms.TextInput(attrs={'class':'form-control'}),
            'notice_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'notice_type':forms.Select(attrs={'class':'form-control'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'authority':forms.Select(attrs={'class':'form-control'}),
            'year:':forms.Select(attrs={'class':'form-control'}),
            'act':forms.Select(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':3,'columns':20}),
            'advisor': forms.Select(attrs={'class':'form-control'}),
            'production_of_books': forms.CheckboxInput(attrs={'class':'form-control'}),
            'reply_sought':forms.CheckboxInput(attrs={'class':'form-control'}),
            'desired_date_of_reply':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'appearance_sought':forms.CheckboxInput(attrs={'class':'form-control'}),  
            'date_of_appearance':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'updload':forms.ClearableFileInput(attrs={'class':'control'}),            
        }
class Hearing_Form(forms.ModelForm):
    class Meta:
        model = Hearing 
        fields = ('hearing_date','was_effective','hearing_gist','is_complete','next_date','upload')  

        widgets={
            'hearing_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'hearing_gist': forms.Textarea(attrs={'class':'form-control'}),
            'is_complete':forms.CheckboxInput(attrs={'class':'form-control'}),
            'was_effective':forms.CheckboxInput(attrs={'class':'form-control'}),
            'next_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'upload':forms.ClearableFileInput(attrs={'class':'control'})            
        }


class SCN_Form(forms.ModelForm): 
    class Meta:
        model = ShowCauseNotice 
        fields = ['scn_no','scn_date','scn_gist','reply_by_date','proposed_additions','upload']
        widgets={
            'scn_no' : forms.TextInput(attrs={'class':'form-control'}),
            'scn_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'scn_gist':forms.Textarea(attrs={'class':'form-control','rows':3,'columns':20}),
            'reply_by_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),           
            'proposed_additions':forms.NumberInput(attrs={'class':'form-control'}),
            'upload':forms.ClearableFileInput(attrs={'class':'control'}),            
        }
class Proposed_Additions_Form(forms.ModelForm):
    # def __init__(self, *args, **kwargs):     
    #         super(Proposed_Additions_Form, self).__init__(*args, **kwargs)
    #         self.fields['issue'].disabled = True                       
    #         self.fields['proposed_addition'].disabled = True    
    class Meta:
        model = ProposedAddition        
        fields = 'issue','proposed_addition'
        
        widgets={
            'issue':forms.Select(attrs={'class':'form-control'}),            
            'proposed_addition':forms.NumberInput(attrs={'class':'form-control'}),
      }
class Proposed_Additions_Form_view(forms.ModelForm):
    def __init__(self, *args, **kwargs):     
            super(Proposed_Additions_Form_view, self).__init__(*args, **kwargs)
            self.fields['issue'].disabled = True                       
            self.fields['proposed_addition'].disabled = True    
    class Meta:
        model = ProposedAddition        
        fields = 'issue','proposed_addition'
        
        widgets={
            'issue':forms.Select(attrs={'class':'form-control'}),            
            'proposed_addition':forms.NumberInput(attrs={'class':'form-control'}),
      }
class Additions_Form(forms.ModelForm):    
    class Meta:
        model = Addition        
        fields ='issue','total_additions','admitted_additions','approval_reason'

        widgets={    
        'issue':forms.Select(attrs={'class':'form-control'}),            
        'total_additions':forms.NumberInput(attrs={'class':'form-control'}),        
        'admitted_additions':forms.NumberInput(attrs={'class':'form-control'}),
        'approval_reason': forms.TextInput(attrs={'class':'form-control'})
          }
class Additions_Form_Edit(forms.ModelForm):
    def __init__(self, *args, **kwargs):     
            super(Additions_Form_Edit, self).__init__(*args, **kwargs)
            self.fields['issue'].disabled = True                       
            self.fields['disputed_additions'].disabled = True    
    
    class Meta:
        model = Addition        
        fields ='issue','disputed_additions'
        widgets={    
        'issue':forms.Select(attrs={'class':'form-control'}),            
        'disputed_additions':forms.NumberInput(attrs={'class':'form-control'}),        
        
          }

    
    
    # def __init__(self, pk, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     issue=self.fields['issue'].queryset = ProposedAddition.objects.filter(proceeding=pk).values_list()
    #     for issue in issue:
    #         print(issue)            

        
class Reply_Scn_Draft_Form(forms.ModelForm):    
    class Meta:
        model = NoticeReplyDraft       
        fields = 'comments','upload'
        
        widgets={
            'comments':forms.Textarea(attrs={'class':'form-control'}),           
            'upload':forms.ClearableFileInput(attrs={'class':'control'}),
      }
class Reply_Scn_Final_Form(forms.ModelForm):    
    class Meta:
        model = NoticeReplyFinal       
        fields = 'reply_date','comment','upload'
        
        widgets={            
            'reply_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'comment':forms.Textarea(attrs={'class':'form-control'}),           
            'upload':forms.ClearableFileInput(attrs={'class':'form-control'}),
      }
        
class Order_Form(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ('order_no','order_date','order_gist','total_demand',   
    'appeal_by_date','upload')  
        widgets={            
            'order_no' : forms.TextInput(attrs={'class':'form-control'}),
            'order_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'order_gist': forms.Textarea(attrs={'class':'form-control','rows':3,'columns':50}),
            'total_demand':forms.NumberInput(attrs={'class':'form-control'}),
            'appeal_by_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'upload':forms.ClearableFileInput(attrs={'class':'form-control'}),
                        
        }

