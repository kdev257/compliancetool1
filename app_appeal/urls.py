from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
path('runmastertemp/<int:pk>',views.action,name='runmastertemp'), #This file runs master template for apppeal action
path('appeal_action/<int:pk>',views.appeal_action,name='appeal_action'),
path('update_appeal_action/<int:pk>/<int:id>/',views.update_appeal_action,name='update_appeal_action'),
path('view_appeal_action/<int:pk>/',views.view_appeal_action,name='view_appeal_action'),
path('approve_appeal_action/<int:pk>/<int:id>',views.approve_appeal_action,name='approve_appeal_action'),
path('draft_appeal/<int:pk>',views.draft_appeal,name='draft_appeal'),
path('as_filed_appeal/<int:pk>',views.as_filed_appeal,name='as_filed_appeal'),
path('create_hearing_notice/<int:pk>',views.create_hearing_notice,name='create_hearing_notice'),
path('appeal_hearing/<int:pk>',views.appeal_hearing,name='appeal_hearing'),
path('appellate_order/<int:pk>',views.appeal_order,name='appellate_order'),
path('view_additions/<int:pk>',views.view_additions ,name='view_additions'),
path('appellate_order_details/<int:pk>/<int:id>',views.appellate_order_details,name='appellate_order_details'),
path('payment/<int:pk>',views.payment,name='payment'),
# views
path('view_hearing_notice/<int:pk>',views.view_hearing_notice,name='view_hearing_notice'),
path('view_hearing_data/<int:pk>',views.view_hearing_data ,name='view_hearing_data'),
path('view_as_filed_appeal/<int:pk>',views.view_as_filed_appeal ,name='view_as_filed_appeal'),
path('view_appellate_order/<int:pk>',views.view_appellate_order ,name='view_appellate_order'),
path('view_appellate_order_details/<int:pk>',views.view_appellate_order_details ,name='view_appellate_order_details'),

 ]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
