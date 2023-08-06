from django import forms
from django.core.exceptions import ValidationError
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, CSVChoiceField, CSVModelChoiceField, TagFilterField
from utilities.forms.widgets import DatePicker
from adestis_netbox_plugin_account_management.models import *
from tenancy.models import *
from django.utils.translation import gettext as _

__all__ = (
    'LoginCredentialsForm',
    'LoginCredentialsFilterForm',
    'LoginCredentialsBulkEditForm',
    'LoginCredentialsCSVForm'
)


class LoginCredentialsForm(NetBoxModelForm):
    comments = CommentField()

    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=True,
    )

    system = DynamicModelChoiceField(
        queryset=System.objects.all(),
        required=True,
    )

    fieldsets = (
        (None, ('logon_name', 'contact', 'system', 'login_credentials_status', 'tags')),
        ('Validity', ('valid_from', 'valid_to')),
    )  

    class Meta:
        model = LoginCredentials
        fields = ['logon_name', 'contact', 'system', 'valid_from', 'valid_to',
                  'login_credentials_status', 'comments', 'tags']
        widgets = {
            'valid_from': DatePicker(),
            'valid_to': DatePicker()
        }
        help_texts = {
            'logon_name': "Logon name",
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from_data = cleaned_data.get("valid_from")
        valid_to_data = cleaned_data.get("valid_to")

        if valid_from_data and valid_to_data:
            # Only do something if both fields are valid so far.
            if valid_to_data < valid_from_data:
                raise ValidationError(
                    "Invalid date range! Field 'Valid to' must be older than field 'Valid from'"
                )


class LoginCredentialsBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=LoginCredentials.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    
    system = DynamicModelChoiceField(
        queryset=System.objects.all(),
        required=False
    )
    
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )
    
    logon_name = forms.CharField(
        max_length=254,
        required=False
    )
    
    valid_from = forms.DateField(
        required=False
    )

    valid_to = forms.DateField(
        required=False
    )
    
    login_credentials_status = forms.ChoiceField(
        required=False,
        choices=LoginCredentialsStatusChoices,
    )

    model = LoginCredentials
    
    fieldsets = (
        (None, ('logon_name', 'contact', 'system', 'login_credentials_status')),
        ('Validity', ('valid_from', 'valid_to')),
    )  
    
    nullable_fields = [
       'valid_from', 'valid_to', 'add_tags', 'remove_tags'
    ]

class LoginCredentialsFilterForm(NetBoxModelFilterSetForm):
    model = LoginCredentials
    
    fieldsets = (
        (None, ('q', 'index', 'tag', 'contact_id', 'system', 'login_credentials_status')),
    )  

    index = forms.IntegerField(
        required=False
    )

    contact_id = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        null_option='None',
        label=_('Contact')
    )

    system = forms.ModelMultipleChoiceField(
        queryset=System.objects.all(),
        required=False
    )

    login_credentials_status = forms.MultipleChoiceField(
        choices=LoginCredentialsStatusChoices,
        required=False
    )
    
    tag = TagFilterField(model)
    
    
class LoginCredentialsCSVForm(NetBoxModelImportForm):
    
    system = CSVModelChoiceField(
        queryset=System.objects.all(),
        required=True,
        to_field_name='system_url',
        help_text='System URL'
    )
    
    contact = CSVModelChoiceField(
        queryset=Contact.objects.all(),
        required=True,
        to_field_name='email',
        help_text='Email address of the contact'
    )
    
    login_credentials_status = CSVChoiceField(
        choices=LoginCredentialsStatusChoices,
        help_text=_('Status'),
        required=True,
    )
        
    class Meta:
        model = LoginCredentials
        fields = ['system', 'contact', 'login_credentials_status', 'logon_name']
        default_return_url = 'plugins:adestis_netbox_plugin_account_management:logincredentials_list'
