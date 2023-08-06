from django.db import models
from django.urls import reverse
from adestis_netbox_plugin_account_management.models import *

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *

__all__ = (
    'PersonStatusChoices',
    'Person',
)


class PersonStatusChoices(ChoiceSet):
    key = 'Person.status'

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_STAGED = 'staged'
    STATUS_FAILED = 'failed'
    STATUS_INVENTORY = 'inventory'
    STATUS_DECOMMISSIONING = 'decommissioning'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_OFFLINE, 'Offline', 'gray'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_STAGED, 'Staged', 'blue'),
        (STATUS_FAILED, 'Failed', 'red'),
        (STATUS_INVENTORY, 'Inventory', 'purple'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'yellow'),
    ]


class Person(NetBoxModel):
    
    first_name = models.CharField(
        max_length=130
    )
    last_name = models.CharField(
        max_length=130
    )

    mail_address = models.EmailField(
        max_length=254,
        verbose_name='E-Mail Address'
    )

    comments = models.TextField(
        blank=True
    )

    person_status = models.CharField(
        max_length=50,
        choices=PersonStatusChoices,
        verbose_name='Status'
    )
    
    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.SET_NULL,
        related_name='contact',
        blank=True,
        null=True
    )
    
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.SET_NULL,
        related_name='tenant',
        blank=True,
        null=True
    )
    
    group = models.ForeignKey(
        to='tenancy.TenantGroup',
        on_delete=models.SET_NULL,
        related_name='tenantgroup',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Persons"
        verbose_name = 'Person'
        ordering = ('last_name', 'first_name',)
        constraints = [
            models.UniqueConstraint(
                fields=['mail_address'],
                name='%(app_label)s_%(class)s_unique_mail_address'
            )
        ]

    def get_person_status_color(self):
        return PersonStatusChoices.colors.get(self.person_status)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return self.__str__ if self.first_name and self.last_name else None

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_plugin_account_management:person', args=[self.pk])
