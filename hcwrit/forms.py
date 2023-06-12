from django import forms
from .models import *

class Recommend_Writ_Form(forms.ModelForm):
     class Meta:
        model = Recommend_Writ
        fields = 'reason','is_recommended'

        widgets={
            'reason': forms.Textarea(attrs={'class':'form-control'}),
            'is_recommended':forms.CheckboxInput(attrs={'class':'form-control'}),          
                        
        }

class Approved_Writ_Form(forms.ModelForm):
     class Meta:
        model = Recommend_Writ
        fields = 'approver_comment','is_approved'

        widgets={
            'approver_comment': forms.Textarea(attrs={'class':'form-control'}),            
            'is_approved':forms.CheckboxInput(attrs={'class':'form-control'}),
            
                        
         }
