from django import forms
from .models import Server, Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ServerForm(forms.Form):
    name = forms.CharField(max_length=200)
    ip_address = forms.GenericIPAddressField(protocol='IPv4')
    server_assignment = forms.CharField(max_length=200)

    name.widget.attrs.update({'class': 'form-control'})
    ip_address.widget.attrs.update({'class': 'form-control'})
    server_assignment.widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        new_name = self.cleaned_data['name'].lower()

        if new_name == 'server':
            raise ValidationError('Name may not be "server"')

        if Server.objects.filter(name__iexact=new_name).count():
            raise ValidationError('Name must be unique. We have "{}" name already'.format(new_name))

        return new_name

    def save(self):
        new_server = Server.objects.create(
            name=self.cleaned_data['name'],
            ip_address=self.cleaned_data['ip_address'],
            server_assignment=self.cleaned_data['server_assignment']
        )
        return new_server

    
#set forms for UserProfile (User,Profile)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('middle_name', 'login', 'job_title', 'department', 'company', 'personal_mobile_phone', 'phisical_delivery_office_name', )

# sent mail
class EmailUserForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
        