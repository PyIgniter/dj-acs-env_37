from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, UserInstanceAccess, Role, Organization, Server, DirectionCompanyInstance, User

from import_export.admin import ImportExportModelAdmin

from import_export import widgets, resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

# Register your models here.


# Define the admin class
admin.site.unregister(User)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'get_password_medoc', 'email', 'first_name', 'get_middle_name', 'last_name', 'is_staff', 'is_active' )
    list_select_related = ('profile', )

    def get_middle_name(self, instance):
        return instance.profile.middle_name
    get_middle_name.short_description = 'Middle name'

    def get_password_medoc(self, instance):
        return instance.profile.password
    get_password_medoc.short_description = 'Password Medoc'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class UserAdmin(ImportExportModelAdmin):
    """docstring for UserAdmin"""
    pass
admin.site.register(User, CustomUserAdmin)



# import-export resource

class ProfileResource(resources.ModelResource):

    username = Field(
        attribute='user',
        column_name='username',
        widget=ForeignKeyWidget(User, 'username')
        )
    last_name = Field(
        attribute='user',
        column_name='last_name',
        widget=ForeignKeyWidget(User, 'last_name')
        )
    first_name = Field(
        attribute='user',
        column_name='first_name',
        widget=ForeignKeyWidget(User, 'first_name')
        )
    email = Field(
        attribute='user',
        column_name='email',
        widget=ForeignKeyWidget(User, 'email')
        )
    is_active = Field(
        attribute='user',
        column_name='is_active',
        widget=ForeignKeyWidget(User, 'is_active')
        )


    class Meta:
        model = Profile
        fields = (
            'id',
            'password',
            'job_title',
            'department',
            'middle_name',
            'company',
            'personal_mobile_phone',
            'phisical_delivery_office_name',
            'external_user',
            )

        export_order = (
            # 'id',
            'username',
            'last_name',
            'first_name',
            'middle_name',
            'email',
            'password',
            'is_active',
            'job_title',
            'department',
            'company',
            'personal_mobile_phone',
            'phisical_delivery_office_name',
            'external_user'
            )


class UserInstanceAccessInline(admin.TabularInline):
    model = UserInstanceAccess
    extra = 0

# Register the Admin classes for Profile using the decorator
@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):

    resource_class = ProfileResource

    search_fields = ('user__username',)
    list_display = ('user', 'get_full_name', 'login', 'password', 'department', 'company', 'external_user')
    fields = ['middle_name', ('user', 'external_user'), ('login', 'password'), ('job_title', 'department', 'company'),('personal_mobile_phone', 'phisical_delivery_office_name')]
    inlines = [UserInstanceAccessInline]

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full name'
    get_full_name.admin_order_field = 'get_full_name'


class UserInstanceAccessResource(resources.ModelResource):


    # user_status = Field()

    user = Field(
        column_name='Логін',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'user__username')
        )
    first_name = Field(
        column_name="Ім'я",
        attribute='subject',
        widget=ForeignKeyWidget(User, 'first_name')
        )
    last_name = Field(
        column_name='Прізвище',
        attribute='subject',
        widget=ForeignKeyWidget(User, 'last_name')
        )
    organization = Field(
        column_name='Організація',
        attribute='organization',
        widget=ForeignKeyWidget(Organization, 'name')
        )
    role = Field(
        column_name='Ролі',
        attribute='role',
        widget=ManyToManyWidget(Role, ',', 'name')
        )
    
    

    class Meta:
        model = UserInstanceAccess
        fields = ('access_date', 'jira_ticket','id',)
        export_order = (
        'id',
        'first_name',
        'last_name',
        'jira_ticket',
        'user',
        'organization',
        'role',
        'access_date'
        )
      

# Register the Admin classes for UserInstanceAccess using the decorator
@admin.register(UserInstanceAccess)
class UserInstanceAccessAdmin(ImportExportModelAdmin):

    resource_class = UserInstanceAccessResource
    search_fields = ('jira_ticket', 'subject__username',)
    list_display = ('jira_ticket', 'get_full_name', 'subject', 'display_role', 'organization', 'get_server',  'access_date')

    def get_full_name(self, obj):
        return obj.subject.get_full_name()
    get_full_name.short_description = 'Full name'
    get_full_name.admin_order_field = 'subject__get_full_name'

    def get_server(self, obj):
        return obj.organization.location_on_server
    get_server.short_description = 'Server'
    get_server.admin_order_field = 'organization__location_on_server'

    list_filter = ('access_date',)

    fieldsets = (
        (None, {
            'fields': ('jira_ticket', 'id')
        }),
        ('Access', {
            'fields': ('role', 'organization') # 'role', must be a list or tuple
        }),
        ('Availability', {
            'fields': ('profile', 'subject', 'access_date')
        }),
    )

class ServerInline(admin.TabularInline):
    model = Organization
    extra = 0
      
@admin.register(Server)
class ServerAdmin(ImportExportModelAdmin):


    list_display = ('name', 'ip_address', 'server_assignment')
    inlines = [ServerInline]


class DirectionCompanyInstanceInline(admin.TabularInline):
    model = Organization
    extra = 0
        
@admin.register(DirectionCompanyInstance)
class DirectionCompanyInstanceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'direction_company')
    inlines = [DirectionCompanyInstanceInline]


@admin.register(Role)
class RoleAdmin(ImportExportModelAdmin):
    pass

class OrganizationResource(resources.ModelResource):

    group = Field(
        column_name='group',
        attribute='group',
        widget=ForeignKeyWidget(DirectionCompanyInstance, 'name')
        )
    location_on_server = Field(
        column_name='location_on_server',
        attribute='location_on_server',
        widget=ForeignKeyWidget(Server, 'name')
        )



    class Meta:
        model = Organization
        fields = ('name', 'num_id','is_branch', 'status_organization',)
        export_order = (
        'name',
        'num_id',
        'is_branch',
        'group',
        'location_on_server',
        'status_organization'
        )
      


@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    """docstring for PersonAdmin"""
    resource_class = OrganizationResource
    list_display = ('name', 'num_id','is_branch', 'group', 'location_on_server', 'status_organization')
