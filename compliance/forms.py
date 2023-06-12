from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import RecentNews,TaxNews,UserQueryNew,TaxUserClass
from django.forms.widgets import NumberInput


class RecentNewsForm(forms.ModelForm):
    class Meta:
        model = RecentNews 
        fields = ("newsdate","newstext")
        widgets={
            'newsdate': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'newstext': forms.Textarea(attrs={'class':'form-control','rows':3,'cols':50})
        }

class TaxNewsForm(forms.ModelForm):
    class Meta:
        model = TaxNews 
        fields = ("act","newsdate","newstext")
        widgets={
            'act' :forms.Select(attrs={'class':'form-control'}),
            'newsdate': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'newstext': forms.Textarea(attrs={'class':'form-control','rows':3,'cols':50})
        }
class UserQueryForm(forms.ModelForm):
    class Meta:
        model=UserQueryNew
        exclude='status',
        fields = ('query_date','act','tax_cat','advisor','upload','query')
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'query_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'act':forms.Select(attrs={'class':'form-control'}),
            'tax_cat':forms.Select(attrs={'class':'form-control'}),
            'advisor':forms.Select(attrs={'class':'form-control'}),
            'query':forms.Textarea(attrs={'class':'form-control'}),
            'upload':forms.ClearableFileInput(attrs={'class':'control'})
         }

class UserQueryReplyForm(forms.ModelForm):
        def __init__(self, *args, **kwargs): 
            super(UserQueryReplyForm, self).__init__(*args, **kwargs)
            self.fields['user'].disabled = True                       
            self.fields['query'].disabled = True
            self.fields['query_date'].disabled = True            
            self.fields['unit'].disabled = True            
            self.fields['act'].disabled = True            
            
        class Meta:
            model=UserQueryNew            
            fields = ('user','query_date','unit','act','upload','query','query_reply')
            widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'query_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'act':forms.Select(attrs={'class':'form-control'}),
            'query':forms.Textarea(attrs={'class':'form-control'}),
            'upload':forms.ClearableFileInput(attrs={'class':'control'}),
            'query_reply': forms.Textarea(attrs={'class':'form-control'})
         }

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
      
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password1','password2')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
                                   
         }
class UserProfileForm(forms.ModelForm):
    class Meta:
        model= TaxUserClass
        fields=('designation','unit','department','band')        
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'designation':forms.Select(attrs={'class':'form-control'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'band':forms.Select(attrs={'class':'control'}),
        }
       

