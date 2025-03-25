from django.urls import path
from .api_constants import TENANT_ENDPOINT, TENANT_DETAIL_ENDPOINT
from .views.UsermanagementViews import TenantCreateView 

# function based views are used


urlpatterns = [
    #path(TENANT_ENDPOINT, tenant_list, name =  "tenant-list" ),
    path('', TenantCreateView.as_view(), name='tenant-create'),
    path('ten/<int:id>', TenantCreateView.as_view(),name="tenant-detail")
]