# Generated by Django 4.1.7 on 2023-04-15 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('idtlit', '0003_alter_hearing_next_date'),
        ('app_appeal', '0004_delete_appellate_order_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appellate_Order_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disputed_tax', models.PositiveIntegerField(default=0, verbose_name='Balance Disputed Tax')),
                ('is_disputed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Created On')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Update On')),
                ('addition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='idtlit.addition')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_appeal.appellate_order')),
            ],
        ),
    ]
