# Machine failures tracking system

A Netbox plugin for keeping track of failures and other state changes for individual devices.


## Installation
Installation package to come.

Once installed, the plugin needs to be added to the configuration.py file.

```python
PLUGINS = ['machine_tracking']

```


## Usage

The plugin shows a log of all state changes under the 'Events' page and log of all replacements under 'Replacements'.

For each device, a panel has been added to show the number of failures in the past 60 days, average time between failures and a link to see all events (state changes) related to that device.