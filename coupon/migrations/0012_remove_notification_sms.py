# Generated by Django 3.1.6 on 2021-06-03 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0011_notification_sms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='sms',
        ),
    ]
