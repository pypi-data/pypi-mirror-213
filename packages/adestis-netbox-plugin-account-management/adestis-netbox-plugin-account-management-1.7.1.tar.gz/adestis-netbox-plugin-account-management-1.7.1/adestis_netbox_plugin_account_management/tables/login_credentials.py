import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_plugin_account_management.models import *


class LoginCredentialsTable(NetBoxTable):
    logon_name = tables.Column(
        linkify=True
    )

    contact = tables.Column(
        linkify=True
    )

    system = tables.Column(
        linkify=True
    )

    login_credentials_status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = LoginCredentials
        fields = ['pk', 'id', 'logon_name', 'contact', 'system', 'valid_from', 'valid_to',
                  'login_credentials_status', 'comments', 'actions', 'tags', 'created', 'last_updated']
        default_columns = ['logon_name', 'contact', 'system', 'valid_from', 'valid_to',
                           'login_credentials_status', 'tags']
