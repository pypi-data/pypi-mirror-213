from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:machine_tracking:event_list',
        link_text='Events',
    ),
    PluginMenuItem(
        link='plugins:machine_tracking:replacement_list',
        link_text='Replacements',
    ),
)