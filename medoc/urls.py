from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.ProfileListView.as_view(), name='users'),
    url(r'^user/(?P<pk>\d+)$', views.ProfileDetailView.as_view(), name='user-detail'),
    url(r'^userinstanceaccesses/$', views.UserInstanceAccessListView.as_view(), name='userinstanceaccesses'),
    url(r'^userinstanceaccess/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.UserInstanceAccessDetailView.as_view(), name='userinstanceaccess-detail'),
    url(r'^directories/$', views.DirectoriesListView.as_view(), name='directories'),
]

urlpatterns += [   
    url(r'^myaccesses/$', views.AvalibleAccessesByUserListView.as_view(), name='my-accesses'),
]

urlpatterns += [  
    url(r'^user/create/$', views.ProfileCreate.as_view(), name='profile_create'),
    url(r'^user/(?P<pk>\d+)/update/$', views.edit_user, name='profile_update'),
    # url(r'^user/(?P<pk>\d+)/update/$', views.ProfileUpdate.as_view(), name='profile_update'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.ProfileDelete.as_view(), name='profile_delete'),
]

urlpatterns += [  
    url(r'^role/create/$', views.RoleCreate.as_view(), name='role_create'),
    url(r'^role/(?P<pk>\d+)/update/$', views.RoleUpdate.as_view(), name='role_update'),
    url(r'^role/(?P<pk>\d+)/delete/$', views.RoleDelete.as_view(), name='role_delete'),
]

urlpatterns += [  
    url(r'^direction-company/create/$', views.DirectionCompanyCreate.as_view(), name='direction-company_create'),
    url(r'^direction-company/(?P<pk>\d+)/update/$', views.DirectionCompanyUpdate.as_view(), name='direction-company_update'),
    url(r'^direction-company/(?P<pk>\d+)/delete/$', views.DirectionCompanyDelete.as_view(), name='direction-company_delete'),
]

urlpatterns += [  
    url(r'^organization/create/$', views.OrganizationCreate.as_view(), name='organization_create'),
    url(r'^organization/(?P<pk>\d+)/update/$', views.OrganizationUpdate.as_view(), name='organization_update'),
    url(r'^organization/(?P<pk>\d+)/delete/$', views.OrganizationDelete.as_view(), name='organization_delete'),
]

urlpatterns += [  
    url(r'^server/create/$', views.ServerCreate.as_view(), name='server_create'),
    # url(r'^organization/(?P<pk>\d+)/update/$', views.OrganizationUpdate.as_view(), name='organization_update'),
    # url(r'^organization/(?P<pk>\d+)/delete/$', views.OrganizationDelete.as_view(), name='organization_delete'),
]

# urlpatterns += [  
#     url(r'^user/(?P<pk>\d+)/share$', views.user_share, name='user_share'),
# ]