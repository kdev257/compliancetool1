from django.contrib import admin
from .models import *
# from .forms import Additions_Form
# Register your models here.
admin.site.register(TaxJurisdiction),
admin.site.register(Initial_Notice),
# admin.site.register(Adjournment),
admin.site.register(Hearing),
admin.site.register(Issue),
admin.site.register(ProposedAddition),
admin.site.register(ShowCauseNotice),
admin.site.register(NoticeReplyDraft),
admin.site.register(NoticeReplyFinal),
admin.site.register(Order),
admin.site.register(Addition),

