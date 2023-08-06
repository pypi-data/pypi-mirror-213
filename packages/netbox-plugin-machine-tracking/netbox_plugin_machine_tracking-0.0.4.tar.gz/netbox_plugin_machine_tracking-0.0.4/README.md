# Machine failures tracking system

A Netbox plugin for keeping track of failures and other state changes for individual devices.


## Installation
The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-plugin-machine-tracking
```

Once installed, the plugin needs to be added to the configuration.py file.

```python
PLUGINS = ['machine_tracking']

```


## Usage

The plugin shows a log of all state changes under the 'Events' page and log of all replacements under 'Replacements'.

For each device, a panel has been added to show the number of failures in the past 60 days, average time between failures and a link to see all events (state changes) related to that device.