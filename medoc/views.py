from django.shortcuts import render, redirect
from .models import Profile, UserInstanceAccess, Role, Organization, Server, DirectionCompanyInstance
from datetime import datetime, timedelta
from django.views import generic
from django.contrib.auth.models import User


# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Server form create
from django.views.generic import View
from .forms import ServerForm, UserForm

from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from django.core.mail import send_mail


def index(request):
    """
    Medoc homepage site
    """
   
    # Generete "counts" some main object.
    num_request = UserInstanceAccess.objects.all().count()
    num_users = Profile.objects.all().count()
    num_organizations = Organization.objects.count()
    # Request last month 
    last_month = datetime.today() - timedelta(days=30)
    num_request_by_month = UserInstanceAccess.objects.filter(access_date__gte=last_month).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Rendering HTML-template index.html with the data inside
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_request':num_request,'num_users':num_users,'num_organizations':num_organizations,'num_request_by_month':num_request_by_month,'num_visits':num_visits}, # num_visits appended
    )



class ProfileListView(LoginRequiredMixin,generic.ListView):
    model = User
    context_object_name = 'user_list' 
    template_name ='medoc/profile_list.html'
    paginate_by = 35
    permission_required = 'medoc.can_view_all_list'

class ProfileDetailView(generic.DetailView):
    # model = Profile
    # update 
    context_object_name = 'profile_detail'    
    template_name = 'medoc/profile_detail.html'
    queryset = User.objects.all()
    
class UserInstanceAccessListView(generic.ListView):
    model = UserInstanceAccess
    paginate_by = 30

class UserInstanceAccessDetailView(generic.DetailView):
    model = UserInstanceAccess

class DirectoriesListView(generic.ListView):
    context_object_name = 'direction_list'    
    template_name = 'medoc/directories_list.html'
    queryset = DirectionCompanyInstance.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DirectoriesListView, self).get_context_data(**kwargs)
        context['role_list'] = Role.objects.all()
        context['organization_list'] = Organization.objects.all()
        context['server_list'] = Server.objects.all()
        # And so on for more models
        return context

class AvalibleAccessesByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing available access to current user. 
    """
    model = UserInstanceAccess
    template_name ='medoc/useraccesses_list_avalible_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return UserInstanceAccess.objects.filter(subject=self.request.user).order_by('access_date')

# Forms for Profile
class ProfileCreate(CreateView):
    model = Profile
    fields = [
    'user',
    'login',
    'password',
    'job_title',
    'department',
    'company',
    'personal_mobile_phone',
    'phisical_delivery_office_name',
    ]
    # initial={'date_of_death':'12/10/2016',}

# class ProfileUpdate(UpdateView):
#     model = Profile
#     # fields = ['first_name','last_name','date_of_birth','date_of_death']
#     fields = '__all__'

class ProfileDelete(DeleteView):
    model = Profile
    success_url = reverse_lazy('users')

# Directories page
#Forms for Role
class RoleCreate(CreateView):
    model = Role
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}
    success_url = reverse_lazy('directories')

class RoleUpdate(UpdateView):
    model = Role
    fields = '__all__'
    success_url = reverse_lazy('directories')

class RoleDelete(DeleteView):
    model = Role
    success_url = reverse_lazy('directories')

#Forms for Role
class DirectionCompanyCreate(CreateView):
    model = DirectionCompanyInstance
    template_name = 'medoc/direction_company_form.html'
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}
    success_url = reverse_lazy('directories')

class DirectionCompanyUpdate(UpdateView):
    model = DirectionCompanyInstance
    template_name = 'medoc/direction_company_form.html'
    fields = '__all__'
    success_url = reverse_lazy('directories')

class DirectionCompanyDelete(DeleteView):
    model = DirectionCompanyInstance
    template_name = 'medoc/direction_company_confirm_form.html'
    success_url = reverse_lazy('directories')

#Forms for Organization
class OrganizationCreate(CreateView):
    model = Organization
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}
    success_url = reverse_lazy('directories')

class OrganizationUpdate(UpdateView):
    model = Organization
    fields = '__all__'
    success_url = reverse_lazy('directories')

class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('directories')

class ServerCreate(View):
    def get(self, request):
        form = ServerForm()
        return render(request, 'medoc/server_create.html', context={'form': form})

    def post(self, request):
        bound_form = ServerForm(request.POST)

        if bound_form.is_valid():
            new_server = bound_form.save()
            return redirect('directories')
        return render(request, 'medoc/server_create.html', context={'form': bound_form})

class ProfileUserDetailView(generic.DetailView):
    context_object_name = 'profile_detail'    
    template_name = 'medoc/profile_detail_1.html'
    queryset = User.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileUserDetailView, self).get_context_data(**kwargs)
    #     # context['user_detail'] = User.objects.all()

        # And so on for more models
        # return context

@login_required() # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('middle_name', 'password', 'job_title', 'department', 'company', 'personal_mobile_phone', 'phisical_delivery_office_name' ))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_active:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/medoc/users/')

        return render(request, "medoc/profile.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


def user_accesses_share(request, pk):
    # Retrieve user by id
    # sent after approved 
    # user = get_object_or_404(User, id=pk, status='approved')
    user = get_object_or_404(User, id=pk)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailUserForm(request.POST)
        # see the code below to use template as body
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import get_template
        from django.template import Context

        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            plaintext = get_template('email.txt')
            htmly = get_template('email.html')

            d = Context({ 'username': username })

            subject = 'hello'
            from_email, to = 'from@example.com', 'to@example.com'
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # user_url = request.build_absolute_uri(user.get_absolute_url())
            # subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], user.username)
            # message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, user_url, cd['name'], cd['comments'])
            # send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})