from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RecentNews,TaxNews,UserQueryNew,State,Act,TaxUserClass,Unit,Advisor

# Register your models here.
@admin.register(RecentNews)
class RecentNewsAdmin(admin.ModelAdmin):
    list_display=('newsdate','newstext')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display='name',
    
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=('unit_name','address','city','state','zipcode')
    
@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    list_display= ('name',)
    
@admin.register(TaxNews)
class TaxNewsAdmin(admin.ModelAdmin):
    list_display=('act','newsdate','newstext')

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display=('tax_cat','advisor')

@admin.register(UserQueryNew)
class UserQueryNewAdmin(admin.ModelAdmin):
    list_display= ('user','query_date','unit','act','query','upload','status')

@admin.register(TaxUserClass)
class TaxUserClassAdmin(admin.ModelAdmin):
    list_display= ('user','designation','unit','department','band')
    



