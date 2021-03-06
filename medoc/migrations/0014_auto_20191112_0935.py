# Generated by Django 2.2.4 on 2019-11-12 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0013_auto_20191109_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='status_organization',
            field=models.CharField(choices=[('a', 'Активна'), ('ar', 'Архівна'), ('s', 'Продано')], default='a', help_text='Статус організації', max_length=100),
        ),
        migrations.AlterField(
            model_name='directioncompanyinstance',
            name='direction_company',
            field=models.CharField(help_text='З урахуванням структури', max_length=200),
        ),
        migrations.AlterField(
            model_name='directioncompanyinstance',
            name='name',
            field=models.CharField(help_text='Напрям', max_length=200),
        ),
        migrations.AlterField(
            model_name='server',
            name='name',
            field=models.CharField(help_text="Вказати ім'я сервера", max_length=200),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_assignment',
            field=models.CharField(help_text='Призначння сервера', max_length=200),
        ),
    ]
