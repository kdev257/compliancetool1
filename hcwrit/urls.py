from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("<int:pk>",views.hcwrit_home,name='hcwrit_home'),
    path("view_order_for_writ/<int:pk>/",views.view_order_for_writ ,name='view_order_for_writ'),
    path("view_order_for_writ_approval/<int:pk>/",views.view_order_for_writ_approval ,name='view_order_for_writ_approval'),
    path("recommend_writ/<int:pk>/",views.recommend_writ ,name='recommend_writ'),
    path("approve_writ/<int:pk>/",views.approve_writ ,name='approve_writ'),
    # path("action/<int:pk>",views.action,name='action'),
    # path("adjourment/<int:pk>",views.adjournment,name='adjourment'),
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)