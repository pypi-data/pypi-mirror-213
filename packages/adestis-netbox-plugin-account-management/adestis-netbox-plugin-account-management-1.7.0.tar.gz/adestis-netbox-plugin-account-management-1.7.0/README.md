# NetBox Account Management

A NetBox plugin for managing the ownership of accounts.
Netbox `v3.5-2.6.1` is required.

# PIP Package

[Click here](https://pypi.org/project/adestis-netbox-plugin-account-management/)

## Installation with Docker

The Plugin may be installed in a Netbox Docker deployment.
The package contains a Dockerfile for [Netbox-Community Docker](https://github.com/netbox-community/netbox-docker)
extension.

Download the Plugin and build from the source:

```
$ git clone https://github.com/adestis/netbox-account-management
$ cd adestis-netbox-plugin-account-management
$ docker build -f Dev-Dockerfile -t adestis-netbox-plugin-account-management-plugin .
```

Update a netbox image name in **docker-compose.yml** in a Netbox Community Docker project root:

```yaml
services:
  netbox: &netbox
    image: adestis-netbox-plugin-account-management-plugin:latest
```

Rebuild the running docker containers:

```
$ cd netbox-docker
$ docker-compose down
$ docker-compose up -d
```

Stop the application container. Then add PLUGINS parameter and PLUGINS_CONFIG parameter to **configuration.py**. It is
stored in netbox-docker/configuration/ by default:

```python
PLUGINS = ['adestis_netbox_plugin_account_management']
```

After that you can start the application again

## Screenshots

![](docs/systems.PNG)