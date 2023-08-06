from extras.plugins import PluginConfig


class MachineTrackingConfig(PluginConfig):
    name = 'machine_tracking'
    verbose_name = 'Machine Tracking'
    description = 'Track and show machine lifecycle history'
    version = '0.1'
    base_url = 'machine-tracking'
    min_version = '3.4.0'

config = MachineTrackingConfig