# Generated by Django 2.2.4 on 2019-10-25 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0007_auto_20191025_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fullname',
        ),
        migrations.DeleteModel(
            name='FullName',
        ),
    ]
