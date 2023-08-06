from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.views import *

urlpatterns = (

    # System lists
    path('systems/', SystemListView.as_view(), name='system_list'),
    path('systems/add/', SystemEditView.as_view(), name='system_add'),
    path('systems/delete/', SystemBulkDeleteView.as_view(), name='system_bulk_delete'),
    path('systems/edit/', SystemBulkEditView.as_view(), name='system_bulk_edit'),
    path('systems/import/', SystemBulkImportView.as_view(), name='system_import'),
    path('systems/<int:pk>/', SystemView.as_view(), name='system'),
    path('systems/<int:pk>/edit/', SystemEditView.as_view(), name='system_edit'),
    path('systems/<int:pk>/delete/', SystemDeleteView.as_view(), name='system_delete'),
    path('systems/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='system_changelog', kwargs={
        'model': System
    }),

    # Login Credentials
    path('login-credentials/', LoginCredentialsListView.as_view(), name='logincredentials_list'),
    path('login-credentials/add/', LoginCredentialsEditView.as_view(), name='logincredentials_add'),
    path('login-credentials/delete/', LoginCredentialsBulkDeleteView.as_view(), name='logincredentials_bulk_delete'),
    path('login-credentials/edit/', LoginCredentialsBulkEditView.as_view(), name='logincredentials_bulk_edit'),
    path('login-credentials/import/', LoginCredentialsBulkImportView.as_view(), name='logincredentials_import'),
    path('login-credentials/<int:pk>/', LoginCredentialsView.as_view(), name='logincredentials'),
    path('login-credentials/<int:pk>/edit/', LoginCredentialsEditView.as_view(), name='logincredentials_edit'),
    path('login-credentials/<int:pk>/delete/', LoginCredentialsDeleteView.as_view(), name='logincredentials_delete'),
    path('login-credentials/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='logincredentials_changelog', kwargs={
        'model': LoginCredentials
    }),

)
