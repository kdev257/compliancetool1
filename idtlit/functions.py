from django.contrib.sessions.models import Session

def check_total_additions(total,*args):
    for args in args:
        total = total-args
    return total         

def sum_addition(*args):
    sum = 0
    for args in args:
        sum += args
    return sum

def clear_session_history(session_key):
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    # Clear the session data
    session_data.clear()
    session.save()