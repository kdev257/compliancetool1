from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('new_notice',views.new_notice,name='new_notice'),
    path("",views.location_user_home,name='users_home'),
    path("action/<int:pk>",views.action,name='action'),
    # path("adjourment/<int:pk>",views.adjournment,name='adjourment'),
    path("appearance/<int:pk>",views.appearance,name='appearance'),
    path("create_scn/<int:pk>",views.create_scn ,name='create_scn'),
    path('update_proposed_addition/<int:pk>',views.update_proposed_additions,name='update_proposed_addition'),
    path('draft_scn_reply/<int:pk>',views.scn_reply_draft,name='draft_scn_reply'),
    path('final_scn_reply/<int:pk>',views.scn_reply_final,name='final_scn_reply'),
    path('assement_order/<int:pk>',views.order,name='assessment_order'),
    path('addition/<int:pk>/<int:id>',views.additions,name ='addition'),
    path('createnotice/',views.create_notice,name='create_notice'),
    path('updatenotice/<int:pk>',views.update_notice,name='update_notice'),
    path('delete_notice/<int:pk>',views.delete_notice,name='delete_notice'),
    path('view_notice_location_user/',views.show_notice_location,name='view_notice_location_user'),
    path('view_notice_advisor/',views.show_notice_advisor,name='view_notice_advisor'),
    path('view_notice/<int:pk>',views.view_notice,name='view_notice'),    
    path('view_hearing/<int:pk>',views.view_hearing,name='view_hearing'),
    path('view_scn/<int:pk>',views.view_Scn,name='view_scn'),
    path('view_proposed_additions/<int:pk>',views.view_proposed_additions,name='view_proposed_additions'),
    path('view_scn_reply_draft/<int:pk>',views.view_Scn_Reply_draft,name='view_scn_reply_draft'),
    path('view_scn_reply_final/<int:pk>',views.view_Scn_Reply_Final,name='view_scn_reply_final'),
    path('view_order/<int:pk>',views.view_assessment_order,name='view_order'),
    path('test_code/',views.test_code,name='test_code'),
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)