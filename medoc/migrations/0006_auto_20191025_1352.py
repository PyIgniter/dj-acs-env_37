# Generated by Django 2.2.4 on 2019-10-25 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0005_auto_20191001_0909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userinstanceaccess',
            old_name='user',
            new_name='profile',
        ),
    ]
