# Generated by Django 3.1.6 on 2021-05-02 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created'], 'verbose_name_plural': 'Categories'},
        ),
    ]
