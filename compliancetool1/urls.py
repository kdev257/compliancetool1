from django.contrib import admin
from django.urls import path,include
from compliance import views
# from dispmanage import views as dis
from taxbot import views as tax
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('idt/',include('idtlit.urls')),
    path('app/',include('app_appeal.urls')),
    path('cht/',include('chart.urls')),
    path('hcw/',include('hcwrit.urls')),    
    path('tri/',include('tribunal_appeal.urls')),
    path('',views.homepage, name ='home'),
    path('landingpage/',views.landingpage,name='landingpage'),
    path('userlogin/',views.userloginview,name='userlogin'),
    path('logout/',views.userlogout,name='logout'),
    path('userprofile/',views.userprofile, name='userprofile'),    
    path('createuser/',views.createuserview,name='createuser'),
    path('recentnew/',views.recentnews, name='recent'),
    path('taxnews/',views.taxnews, name='taxnews'),
    path('advisory/',views.advisory, name='advisory'),
    path('updatequery/<int:id>',views.updatequery,name='updatequery'),
    path('deletequery/<int:id>',views.deletequery,name='deletequery'),
    path('showquery/',views.showquerydata,name='showquerydata'),
    path('queryreply/<int:id>',views.queryreply, name='queryreply'),
    path('closequery/<int:id>',views.closequery,name='closequery'),    
    path('admin/', admin.site.urls),
    #dispmanageURLS
    # path('notice/',dis.noticedetails,name='notice'),
    # path('updatenotice/<int:id>',dis.noticeupdate,name='updatenotice'),
    # path('showdata/',dis.showdisputedata,name='showdata'),
    # path('noticereply/<int:id>',dis.noticereply,name='noticereply'),
    # path('openproceeding/',dis.showproceedingdata,name='openproceeding'),
    # path('upackrep/<int:id>',dis.uploadackreply,name='upackrep'),
    # path('hearingnotice/<int:id>',dis.asshearingnotice,name='hearingnotice'),
    # path('hearingdetails/<int:id>',dis.hearingdetailsview,name='hearingdetails'),
    # path('order/<int:id>',dis.AssessmentOrderview, name='order'),
    
    # path('showorder/',dis.showassessmentorder,name='showorder'),
    # path('sendappeal/<int:id>',dis.senddraftappeal, name='sendappeal'),
    # path('sendafappeal/<int:id>',dis.uploadasfiledappeal, name='sendafappeal'),
    # path('appealhearing/<int:id>',dis.apphearingnotice,name='appealhearing'),
    # path('fahearing/<int:id>',dis.fahearingdetailsview,name='fahearing'),
    # path('faorder/<int:id>',dis.faorderview,name='faorder'),
    # path('cifaorder/<int:id>',dis.faciorderview,name='cifaorder')
    #taxbot views
    path('pos/',tax.findpos,name='pos'),
    path('poss/',tax.findposs,name='poss'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
