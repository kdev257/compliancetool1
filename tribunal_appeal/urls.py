from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
# path('new_notice',views.new_notice,name='new_notice'),
path("<int:pk>",views.tribunal_home,name='tribunal_home'),
path('tri_appeal_action/<int:pk>',views.tri_appeal_action,name='tri_appeal_action'),
path('recommend_appeal_action/<int:pk>/<int:id>/',views.recommend_appeal_action,name='recommend_appeal_action'),
path('tri_view_appeal_action/<int:pk>/',views.view_appeal_action,name='tri_view_appeal_action'),
path('tri_approve_appeal_action/<int:pk>/<int:id>',views.approve_appeal_action,name='tri_approve_appeal_action'),
path('tribunal_draft_appeal/<int:pk>',views.tribunal_draft_appeal,name='tribunal_draft_appeal'),
path('as_filed_tribunal_appeal/<int:pk>',views.tribunal_as_filed_appeal,name='as_filed_tribunal_appeal'),
path('create_tribunal_hearing_notice/<int:pk>',views.create_hearing_notice,name='create_tribunal_hearing_notice'),
path('tribunal_appeal_hearing/<int:pk>',views.tribunal_appeal_hearing,name='tribunal_appeal_hearing'),
path('tribunal_order/<int:pk>',views.tribunal_order,name='tribunal_order'),
path('view_appellate_additions/<int:pk>',views.view_appellate_additions ,name='view_appellate_additions'),
path('tribunal_order_details/<int:pk>/<int:id>',views.tribunal_order_details,name='tribunal_order_details'),
path('tribunal_payment/<int:pk>',views.tribunal_payment,name='tribunal_payment'),
# # views
path('view_tribunal_hearing_notice/<int:pk>',views.view_tribunal_hearing_notice,name='view_tribunal_hearing_notice'),
path('view_tribunal_hearing_data/<int:pk>',views.view_tribunal_hearing_data ,name='view_tribunal_hearing_data'),
path('view_as_filed_tribunal_appeal/<int:pk>',views.view_tribunal_as_filed_appeal,name='view_as_filed_tribunal_appeal'),
path('view_tribunal_order/<int:pk>',views.view_tribunal_order ,name='view_tribunal_order'),
path('view_tribunal_order_details/<int:pk>',views.view_tribunal_order_details,name='view_tribunal_order_details'),

]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)