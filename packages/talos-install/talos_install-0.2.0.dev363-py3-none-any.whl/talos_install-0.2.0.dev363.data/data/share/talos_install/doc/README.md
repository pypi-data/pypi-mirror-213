# All in One installation

## Deploy requirements

Currrent Talos-cli version is still not public, a dev_key is required for deployment.

Ask a `dev_key` and `dev_key.pub` to save in your `$HOME/.ssh` folder.

## OS requirements

- The supported OS is Rocky Linux 8. Other Rhel like distributions should works, but aren't tested yet.

- An **user with sudo permissions** is MANDATORY, don't use root directly.

### Packages

- python = 3.9
- pip = 3.9

```bash
sudo dnf install epel-release -y

# Install Python 3.9 requirements
sudo dnf install python39  python39-pip sshpass -y

# Update pip
pip3.9 install --upgrade pip

# Install package
pip install talos-install
```

### Installation

The talos_install package can be runned with these options:

- precheck: to prepare system with base requirements
- deploy: to install components
- build: to recreate docker images and pull on docker Hub (only for authorized developper)
- remove: to remove main settings and confurations.

> Note that remove doesn't remove installed packages (like docker)
and doesn't return to original settings (like selinux or firewalld).

#### inventory

File `<pip_environment>/share/talos_install/etc/inventory` is dinamically create at code level.
Changes to this file by user are tatally ignored during execution.

#### ansible.cfg

The default ansible configuration should not be changed.
By default the `display_ok_hosts` parameter is set to false.
If you need to display also the OK state please comment the row in
`<pip_environment>/share/talos_install/ansible/ansible.cfg`

#### talos.yaml

Change configuration of config file `<pip_environment>/share/talos_install/etc/talos.yaml`
to change users configuration.
Is not allow to add or delete master and guest configuration

#### global.yaml

Change configuration of config file `<pip_environment>/share/talos_install/etc/global.yaml`
to change customer configuration.

### Run Installation precheck

```bash
talos_install precheck
```

A list of change will be shown for user approval. Use `-y` to confirm automatically.

### Run Installation deploy

```bash
talos_install deploy
```

A list of change will be shown for user approval. Use `-y` to confirm automatically.

## Post installation

Then need to validate configuration.
First access as talos user:

```bash
sudo su - talos
```

By default setup is automatically done during deploy:

```bash
<pip_environment>/share/talos_cli/etc/talos.yaml

talos_conf: use_default: 'true'
```

If necessary run setup

```bash
 talos-config setup
```

Load initial configuration

```bash
talos-config reload
```

Check Key Pairs with Talos-cli (needed for update only)

```bash
talos-config git_keys
```

Check Overall status

```bash
talos-config check
```
