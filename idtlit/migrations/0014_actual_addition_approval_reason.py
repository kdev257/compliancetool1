# Generated by Django 4.1.7 on 2023-04-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idtlit', '0013_actual_addition_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='actual_addition',
            name='approval_reason',
            field=models.CharField(default='Pls give reason for appeal/admiting the tax', help_text='Pls give reason for appeal/admiting the tax', max_length=200, verbose_name='Reason'),
        ),
    ]
