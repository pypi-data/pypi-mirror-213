from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *


class LoginCredentialsType(NetBoxObjectType):
    class Meta:
        model = LoginCredentials
        fields = '__all__'
        filterset_class = LoginCredentialsFilterSet


class SystemType(NetBoxObjectType):
    class Meta:
        model = System
        fields = '__all__'
        filterset_class = SystemFilterSet


class Query(ObjectType):
    login_credentials = ObjectField(LoginCredentialsType)
    login_credentials_list = ObjectListField(LoginCredentialsType)

    system = ObjectField(SystemType)
    system_list = ObjectListField(SystemType)


schema = Query
