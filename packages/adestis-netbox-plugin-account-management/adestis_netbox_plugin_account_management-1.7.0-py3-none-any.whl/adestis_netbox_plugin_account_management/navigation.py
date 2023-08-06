from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

system_buttons = [
    PluginMenuButton(
        link='plugins:adestis_netbox_plugin_account_management:system_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["adestis_netbox_plugin_account_management.system_add"],
    )
]

login_credentials_buttons = [
    PluginMenuButton(
        link='plugins:adestis_netbox_plugin_account_management:logincredentials_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["adestis_netbox_plugin_account_management.logincredentials_add"],
    )
]

menu_items = [
    PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:system_list',
        link_text='Systems',
        buttons=system_buttons,
        permissions=["adestis_netbox_plugin_account_management.system_list"],
    ),
    PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:logincredentials_list',
        link_text='Login Credentials',
        buttons=login_credentials_buttons,
        permissions=["adestis_netbox_plugin_account_management.logincredentials_list"],
    )
]
