from netbox.api.viewsets import NetBoxModelViewSet

from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.models import *
from .serializers import *


class LoginCredentialsViewSet(NetBoxModelViewSet):
    queryset = LoginCredentials.objects.prefetch_related('tags', 'contact', 'system')
    serializer_class = LoginCredentialsSerializer
    filterset_class = LoginCredentialsFilterSet


class SystemListViewSet(NetBoxModelViewSet):
    queryset = System.objects.prefetch_related(
        'tags'
    )

    serializer_class = SystemSerializer
    filterset_class = SystemFilterSet
