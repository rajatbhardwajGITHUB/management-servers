from django.urls import path
from .api_constants import TENANT_ENDPOINT, TENANT_DETAIL_ENDPOINT

# function based views are used
urlpatterns = [
    path(TENANT_ENDPOINT, tenant_list, name =  "tenant-list" ),
]
