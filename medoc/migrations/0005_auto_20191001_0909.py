# Generated by Django 2.2.4 on 2019-10-01 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0004_profile_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinstanceaccess',
            options={'permissions': (('can_view_all_list', 'Can view all list'), ('can_view_self_list', 'Can view self list'))},
        ),
    ]