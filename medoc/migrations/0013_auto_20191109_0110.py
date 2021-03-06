# Generated by Django 2.2.4 on 2019-11-08 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0012_profile_external_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_branch',
            field=models.IntegerField(blank=True, default=0, help_text='Ознака філії'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(help_text='Назва організації', max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='num_id',
            field=models.IntegerField(help_text='Код ЄДРПО'),
        ),
    ]
