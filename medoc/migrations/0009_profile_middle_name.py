# Generated by Django 2.2.4 on 2019-10-25 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medoc', '0008_auto_20191025_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='middle_name',
            field=models.CharField(default='по батькові', help_text='Додайте, по батькові', max_length=200),
        ),
    ]