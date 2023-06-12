from django import forms
from django.forms import widgets
from django.forms.widgets import CheckboxInput, TextInput

class PosForm(forms.Form):
    REG_CHOICE=(
    ('Yes','Yes'),
    ('No','No'),)   
    Add_Choice=(
    ('Yes','Yes'),
    ('No','No'),)
        
    supplier_name=forms.CharField(max_length=100,required=True,label="Enter Supplier Name",widget=TextInput(attrs={'class':'form-control'}))    
    registered = forms.ChoiceField(choices=REG_CHOICE,widget=forms.Select)
    add_on_record=forms.ChoiceField(choices=Add_Choice,widget=forms.Select)
    rec_location=forms.CharField(max_length=70)
    supp_location=forms.CharField(max_length=70)

class PosformSS(forms.Form):
    service_name=(
        ('1','immovable property'),
        ('2','personal services'),
        ('3','training & Perfomance appraisal'),
        ('4','admission to events'),
        ('5','events & anciliary'),
        ('6','transportation & courier'),
        ('7','passenger transport'),
        ('8','onboard Services'),
        ('9','telecommunication'),
        ('10','banking Services'),
        ('11','insurance Services'),
        ('12','advertisement to Govt')
    )
    REG_CHOICE=(
                ('Yes','Yes'),
                ('No','No'),
            )   
    Add_Choice=(
            ('Yes','Yes'),
            ('No','No'),
    )
    Event_location=(
        ('1','India'),
        ('2','Outside India ')
    )
    supplier_name=forms.CharField(max_length=100,required=True,label="Enter Supplier Name",widget=TextInput(attrs={'class':'form-control'})) 
    service_name=forms.ChoiceField(choices=service_name,help_text='Pls Select Name of Service from the List',widget=forms.Select(attrs={'class':'form-control'}))
    registered = forms.ChoiceField(choices=REG_CHOICE,widget=forms.Select(attrs={'class':'form-control'}),help_text='Pls. Enter regisration status of recipient of Service')
    add_on_record=forms.ChoiceField(choices=Add_Choice,widget=forms.Select(attrs={'class':'form-control'}),help_text='Pls. Select Yes if Service Provider has address of Recipient in his records')
    rec_location=forms.CharField(max_length=70,help_text='Pls Enter name of State where recipient is based',widget=forms.TextInput(attrs={'class':'form-control'}))
    supp_location=forms.CharField(max_length=70,help_text='Pls Enter name of State where Service Provided is based',widget=forms.TextInput(attrs={'class':'form-control'}))
    state=forms.CharField(max_length=70,help_text='Pls enter the name of state where property is located or where service are actually performed ',widget=forms.TextInput(attrs={'class':'form-control'}))
    event_loc=forms.BooleanField(widget=CheckboxInput(attrs={'class':'onoffswitch','id': 'myonoffswitch'}),help_text='Only required in case of Organising of events check if recipient is unregistered and event is held ourside india',required=False)
