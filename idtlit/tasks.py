from django_q.tasks import async_task,schedule
from django_q.models import Schedule
from django.core.mail import EmailMessage
from compliancetool1.settings import EMAIL_HOST_USER
from .models import Initial_Notice,Hearing
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from idtlit.templates.idtlit import *
import arrow
from django.utils import timezone
from django.db.models import Q


def send_notice_mail():
    date_range = timezone.now()-timezone.timedelta(days=2)
    notice_data = Initial_Notice.objects.filter(created__gte=date_range)
    for notice in notice_data:
        subject = f'Alert for creation of new notice bearing No.{notice.notice_no} dated {notice.notice_date}'
        html_message = render_to_string('idtlit/mail_template.html', {'notice_no':notice.notice_no,'notice_date':notice.notice_date,'unit':notice.unit,'authority':notice.authority,'year':notice.year,  'desired_date_of_reply':notice.desired_date_of_reply,'date_of_appearance':notice.date_of_appearance,'created_by':notice.created_by,'advisor':notice.advisor,'description':notice.description})
        plain_message = strip_tags(html_message)
        from_email = EMAIL_HOST_USER
        to = notice.advisor.advisor.email
        async_task(mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message))

def send_hearing_alert():
    date_range1 = timezone.now()
    date_range2 = timezone.now() + timezone.timedelta(days=4)
    notice_data = Initial_Notice.objects.filter(desired_date_of_reply__range=(date_range1,date_range2))
    for notice in notice_data:
        subject = f'Alert for new hearing in notice bearing No.{notice.notice_no} dated {notice.notice_date} scheduled for {notice.desired_date_of_reply}'
        html_message = render_to_string('idtlit/hearing_alert.html', {'notice_no':notice.notice_no,'notice_date':notice.notice_date,'unit':notice.unit,'authority':notice.authority,'year':notice.year,  'desired_date_of_reply':notice.desired_date_of_reply,'date_of_appearance':notice.date_of_appearance,'created_by':notice.created_by,'advisor':notice.advisor,'description':notice.description})
        plain_message = strip_tags(html_message)
        from_email = EMAIL_HOST_USER
        to = [notice.advisor.advisor.email,notice.created_by.email]
        async_task(mail.send_mail(subject, plain_message, from_email, to, html_message=html_message))

def upload_hearing_details():
    d_hearing =tuple(Hearing.objects.values_list('proceeding').distinct().order_by('proceeding'))
    for d in d_hearing:
        proceeding = Hearing.objects.filter(proceeding=d).last()
        if proceeding.is_complete:
            pass
        else:                
            subject = f'Alert for uploading hearing details in notice bearing No.{proceeding.proceeding.notice_no} dated {proceeding.proceeding.notice_date} scheduled for hearing on {proceeding.next_date}' 
            html_message = render_to_string('idtlit/upload_hearing_details.html', {'notice_no':proceeding.proceeding.notice_no,'notice_date':proceeding.proceeding.notice_date,'unit':proceeding.proceeding.unit,'authority':proceeding.proceeding.authority,'year':proceeding.proceeding.year,  'desired_date_of_reply':proceeding.proceeding.desired_date_of_reply,'date_of_appearance':proceeding.proceeding.date_of_appearance,'created_by':proceeding.proceeding.created_by,'advisor':proceeding.proceeding.advisor,'description':proceeding.proceeding.description})
            plain_message = strip_tags(html_message)
            from_email = EMAIL_HOST_USER
            to = [proceeding.proceeding.advisor.advisor.email,proceeding.proceeding.created_by.email]
            async_task(mail.send_mail(subject, plain_message, from_email, to, html_message=html_message))
        # else:            
        #     subject = f'Alert for uploading hearing details in notice bearing No.{notice.notice_no} dated {notice.notice_date} scheduled for hearing on {notice.desired_date_of_reply}'
        #     html_message = render_to_string('idtlit/upload_hearing_details.html', {'notice_no':notice.notice_no,'notice_date':notice.notice_date,'unit':notice.unit,'authority':notice.authority,'year':notice.year,  'desired_date_of_reply':notice.desired_date_of_reply,'date_of_appearance':notice.date_of_appearance,'created_by':notice.created_by,'advisor':notice.advisor,'description':notice.description})
        #     plain_message = strip_tags(html_message)
        #     from_email = EMAIL_HOST_USER
        #     to = [notice.advisor.advisor.email,notice.created_by.email]
        #     async_task(mail.send_mail(subject, plain_message, from_email, to, html_message=html_message))


    