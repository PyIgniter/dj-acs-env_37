from django.db import models
from django.urls import reverse
import uuid #Required for unique User instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    """
    Model represent a Profile
    """
    middle_name = models.CharField(max_length=200, help_text="Додайте, по батькові")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    login = models.CharField(max_length=200, help_text="Додайте користувача, M.E.Doc")
    password = models.CharField(max_length=200, help_text="Додайте пароль, M.E.Doc")
    job_title = models.CharField(max_length=200, help_text="")
    department = models.CharField(max_length=200, help_text="")
    company = models.CharField(max_length=200, help_text="")
    personal_mobile_phone = models.CharField(max_length=200, help_text="")
    phisical_delivery_office_name = models.CharField(max_length=200, help_text="")
    external_user = models.BooleanField(default=False, help_text="Статус зовнішнього користувача")

    class Meta:
        ordering  = ['user__username']
            


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{}'.format(self.user)

    def get_absolute_url(self):
        """
        Returns the url to access a particular Profile instance.
        """
        return reverse('user-detail', args=[str(self.id)])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_full_name(self):
        return "{} {} {}".format(self.user.last_name, self.user.first_name, self.middle_name)



class UserInstanceAccess(models.Model):
    """
    Model represent a User Instance Access
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular User Instance")
    jira_ticket = models.CharField(max_length=150, help_text="")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    role = models.ManyToManyField('Role', help_text='Choices Role-(s)')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    access_date = models.DateField(null=True, blank=True)
    subject = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering  = ['access_date']
        permissions = (
            ("can_view_all_list", "Can view all list"),
            ("can_view_self_list", "Can view self list"),
            )
            

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{}'.format(self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a particular user instance.
        """
        return reverse('userinstanceaccess-detail', args=[str(self.id)])

    def display_role(self):
        """
        Creates a string for the access permit . This is required to display acccess in Admin.
        """
        return ', '.join( [role.name for role in self.role.all()[:3] ])
    display_role.short_description = 'Access permit'

        
class Role(models.Model):
    """
    Model represent a Role
    """
    name = models.CharField(max_length=100, help_text='Enter a Role name')
    description = models.CharField(max_length=200, help_text='Enter a Description')


    def __str__(self):
        """
        String for representing the Model object
        """
        return self.name

class Organization(models.Model):
    """
    Model represent a Organization
    """
    status = (
        ('a','Активна'),
        ('d','Не активна'),
        ('l', 'Ліквідується'),
        ('s', 'Продано'),
        )

    name = models.CharField(max_length=200, help_text='Назва організації')
    num_id = models.CharField(max_length=9, help_text='Код ЄДРПО')
    is_branch = models.IntegerField(help_text='Ознака філії', blank=True, default=0)
    group = models.ForeignKey('DirectionCompanyInstance', on_delete=models.SET_NULL, null=True)
    location_on_server = models.ForeignKey('Server', on_delete=models.SET_NULL, null=True)
    status_organization = models.CharField(max_length=100, choices=status, default='a', help_text='Статус організації')

    def __str__(self):
        """
        String for representing the Model object
        """
        return self.name
        
class DirectionCompanyInstance(models.Model):
    """
    Model represent a Direction Company Instance
    """
    name = models.CharField(max_length=200, help_text='Напрям')
    direction_company = models.CharField(max_length=200, help_text='З урахуванням структури')

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{}'.format(self.name)

class Server(models.Model):
    """
    Model represent a Server
    """
    name = models.CharField(max_length=200, help_text="Вказати ім'я сервера")
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    server_assignment = models.CharField(max_length=200, help_text='Призначння сервера')
    # win_version = models.CharField(max_length=200, help_text='Опереційна система')

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{}'.format(self.name)
        