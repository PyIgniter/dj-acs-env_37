# Generated by Django 2.2.4 on 2019-11-08 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0010_auto_20191104_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='login',
            field=models.CharField(help_text='Додайте користувача, M.E.Doc', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='middle_name',
            field=models.CharField(help_text='Додайте, по батькові', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(help_text='Додайте пароль, M.E.Doc', max_length=200),
        ),
    ]