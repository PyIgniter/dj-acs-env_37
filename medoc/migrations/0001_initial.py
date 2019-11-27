# Generated by Django 2.2.4 on 2019-09-10 08:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DirectionCompanyInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('direction_company', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FullName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Enter a User first name', max_length=200)),
                ('middle_name', models.CharField(help_text='Enter a User middle name', max_length=200)),
                ('last_name', models.CharField(help_text='Enter a User last name', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('num_id', models.IntegerField(help_text='Введіть ЄДРПО')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medoc.DirectionCompanyInstance')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a Role name', max_length=100)),
                ('description', models.CharField(help_text='Enter a Description', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('server_assignment', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('mail', models.EmailField(max_length=200)),
                ('job_title', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('personal_mobile_phone', models.CharField(max_length=200)),
                ('phisical_delivery_office_name', models.CharField(max_length=200)),
                ('fullname', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='medoc.FullName')),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_enabled', models.CharField(blank=True, choices=[('e', 'Enable'), ('d', 'Disable')], default='e', max_length=1)),
                ('account_expires', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['account_expires'],
            },
        ),
        migrations.CreateModel(
            name='UserInstanceAccess',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular User Instance', primary_key=True, serialize=False)),
                ('jira_ticket', models.CharField(max_length=150)),
                ('access_date', models.DateField(blank=True, null=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medoc.Organization')),
                ('role', models.ManyToManyField(help_text='Choices Role-(s)', to='medoc.Role')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medoc.User')),
                ('user_status', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='medoc.UserStatus')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='location_on_server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medoc.Server'),
        ),
    ]