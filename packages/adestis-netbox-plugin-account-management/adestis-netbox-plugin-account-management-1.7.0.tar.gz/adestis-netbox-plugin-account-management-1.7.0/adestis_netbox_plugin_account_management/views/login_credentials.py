from netbox.views import generic
from adestis_netbox_plugin_account_management.forms import *
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.tables import *
from tenancy.models import Contact

from netbox.views import generic
from utilities.views import ViewTab, register_model_view

__all__ = (
    'LoginCredentialsView',
    'LoginCredentialsListView',
    'LoginCredentialsEditView',
    'LoginCredentialsDeleteView',
    'DeviceLoginCredentials',
    'LoginCredentialsBulkDeleteView',
    'LoginCredentialsBulkEditView',
    'LoginCredentialsBulkImportView'
)


class LoginCredentialsView(generic.ObjectView):
    queryset = LoginCredentials.objects.all()


class LoginCredentialsListView(generic.ObjectListView):
    queryset = LoginCredentials.objects.all()
    table = LoginCredentialsTable
    filterset = LoginCredentialsFilterSet
    filterset_form = LoginCredentialsFilterForm


class LoginCredentialsEditView(generic.ObjectEditView):
    queryset = LoginCredentials.objects.all()
    form = LoginCredentialsForm


class LoginCredentialsDeleteView(generic.ObjectDeleteView):
    queryset = LoginCredentials.objects.all()


@register_model_view(Contact, name='devicelogincredentials', path='login-credentials')
class DeviceLoginCredentials(generic.ObjectView):
    ...
    queryset = Contact.objects.all()
    template_name = "adestis_netbox_plugin_account_management/device_login_credentials_table.html"
    
    tab = ViewTab(
        label='Login Credentials',
        badge=None,
        hide_if_empty=False
    )

    def get_extra_context(self, request, instance):
        assets = LoginCredentials.objects.filter(contact=instance)
        table = LoginCredentialsTable(assets)
        data = {
            "table": table,
        }
        return data


class LoginCredentialsBulkDeleteView(generic.BulkDeleteView):
    queryset = LoginCredentials.objects.all()
    table = LoginCredentialsTable
    
    
class LoginCredentialsBulkEditView(generic.BulkEditView):
    queryset = LoginCredentials.objects.all()
    filterset = LoginCredentialsFilterSet
    table = LoginCredentialsTable
    form =  LoginCredentialsBulkEditForm
    

class LoginCredentialsBulkImportView(generic.BulkImportView):
    queryset = LoginCredentials.objects.all()
    model_form = LoginCredentialsCSVForm
    table = LoginCredentialsTable
    