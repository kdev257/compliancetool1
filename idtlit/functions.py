from .models import Initial_Notice, Hearing
import sqlite3
def check_total_additions(total,*args):
    for args in args:
        total = total-args
    return total         

def sum_addition(*args):
    sum = 0
    for args in args:
        sum += args
    return sum

