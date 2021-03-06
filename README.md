
# Network Equipment Simulator (NESi)
### (former Softboxen)

[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/inexio/NESi/master/LICENSE.rst)
[![GitHub build](https://img.shields.io/github/v/tag/inexio/NESi?label=Release)](https://github.com/inexio/NESi)



The `NESi` project which originated from [`softboxen`](https://github.com/etingof/softboxen), a project originally created by our 
co-developer [Ilya Etingof](https://github.com/etingof), aims to support different 
network devices of various vendors like Alcatel or Huawei.

The goal of the project is to simulate the presence of a large number
of network devices (such as switches, routers, modems etc) on the network.
These simulated devices expose their management interfaces and support
command-line dialogues in a reasonably convincing way. The main use-case
for the software is to create a testing environment for network management
and automation.

For more information on `softboxen` or `NESi` please refer to our local [documentation](https://github.com/inexio/NESi/tree/master/docs/source).

## NESi at FOSDEM 2021 - Request for Papers
The NESi team will organize a devroom for Network monitoring, discovery and inventory.
Click [here](https://thola.io/posts/thola-fosdem/) for more information

## Features


[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_alcatel/master?label=alcatel_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_huawei/master?label=huawei_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_edgecore/master?label=edgecore_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_keymile/master?label=keymile_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_pbn/master?label=pbn_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_zhone/master?label=zhone_tests)]()

### Supported Vendors
 - Alcatel
 - Huawei
 - Edgecore
 - Keymile
 - Zhone
 
### Upcoming Vendors
 - Pbn
 - Juniper
 - Cisco

### Supported network components

- Subracks
- Cards
- Ports
- ONTs
- CPEs
- Vlans
- Interfaces


## Download

The `NESi` package is distributed under terms and conditions of 2-clause BSD [license](https://github.com/inexio/NESi/blob/master/LICENSE). 

Furthermore the previous `softboxen` project is freely available as a GitHub [repository](https://github.com/etingof/softboxen) or can be downloaded from [PyPI](https://pypi.org/project/softboxen).

## Installation

### Basic Setup

Either clone the repository with the following command:
```shell script
$ git clone git@github.com:inexio/NESi.git
```
After that, make sure you have installed the required python packages found in the requirements.txt. An easy way to do this is with the following command:
```shell script
$ pip install -r requirements.txt
```

### pip Setup

If you want to install our project as binaries into a venv using pip you can follow theses steps:

```
python3 -m venv venv
cd venv
source bin/activate
pip install https://github.com/inexio/NESi/archive/master.zip
```

After finishing the installation you can use these commands:

```
nesi-api --recreate-db --load-model <vendor>
nesi-cli --box-uuid <uuid>
nesi-cli --standalone <vendor> --box-uuid <uuid>
```

### Debian-package Setup

If you want to install our project using debian-package you can follow theses steps:

```
pip install -r requirements.txt
apt-get update
apt install NESi/deb_dist/$(ls "NESi/deb_dist" | grep ".deb$")
```

After finishing the installation you can use these commands:

```
nesi-api --recreate-db --load-model <vendor>
nesi-cli --box-uuid <uuid>
nesi-cli --standalone <vendor> --box-uuid <uuid>
```

### Systemd Setup

Add a nesi user to your system

```shell script
$ sudo adduser nesi
```

Add a folder for nesi to /opt

```shell script
$ cd /opt
$ mkdir nesi
```

Add a 'var' and 'etc' folder

```shell script
$ cd nesi/
$ mkdir var/ etc/
```

Add a new venv via python

```shell script
$ python3 -m venv venv
```

Clone NESi into the venv and install requirements

```shell script
$ cd venv
$ git clone https://github.com/inexio/NESi.git
$ source bin/activate
$ python3 -m pip install -r NESi/requirements.txt
$ deactivate
```

Change access rights

```shell script
$ chown nesi:nesi -R /opt/nesi/
```

Copy the service template to /etc/systemd/system

```shell script
$ cp NESi/bootup/conf/systemd/nesi-gunicorn.service /etc/systemd/system
```

Copy nesi.conf to /opt/nesi/etc and make according changes

```shell script
$ cp NESi/bootup/conf/nesi.conf /opt/nesi/etc/
```

Start systemd process
```shell script
$ systemctl daemon-reload
$ systemctl start nesi-gunicorn.service
```

## How to use NESi

The easiest way to play with the example CLI is to run two terminals on the NESi
repo - one that starts up the REST API server and populates the example model in
the underlying DB, and another that simulates the devices Command Line Interface and runs against the REST API server.

REST API terminal:

    $ python3 api.py [--recreate-db] [--load-model <VENDOR>]


CLI terminal:

First we collect the uuid´s of all boxes

    % python3 cli.py --list-boxen

    Vendor Alcatel, model 7360, version FX-4, uuid d8da2c00-ed28-11ea-9cc7-8c8590d3240c
    
Second we connect to one box with the specific uuid

    % python3 cli.py --box-uuid d8da2c00-ed28-11ea-9cc7-8c8590d3240c

          _   _ ______  _____ _ 
         | \ | |  ____|/ ____(_)
         |  \| | |__  | (___  _ 
         | . ` |  __|  \___ \| |
         | |\  | |____ ____) | |
         |_| \_|______|_____/|_|
    
    
    Hint: login credentials: admin/secret (Huawei: root/secret)
    
    login:admin
    Password:secret
    Last login on 01.03.2020

Interactive menus will guide you through the implemented commands.

### SSH and Telnet Daemon

NESi comes with SSH and Telnet socket Daemons built into the boxes itself. 

To use either telnet or ssh you have to specify one of them in the setup-script of a box or set it via the rest-api.

```shell script
req='{
  ...
  "network_protocol": "ssh",
  "network_address": "127.0.0.1",
  ...
}'
```

After setting the network_protocol of a device you can launch the 'box.sh' script with the --daemon flag to start the device in either telnet or ssh socket mode.

```shell script
$ ./bootup/box.sh --box-uuid <devices uuid> --daemon
```

The network_adress field is used as the host adress for the socket, so set this option accordingly.

After the socket has started you can connect to your device with the chosen protocol.

### How to use debug mode

First we configure a debugger in our IDE. Therefore we add a Python Debug Server with pydevd_pycharm. 

    Host name   : localhost
    Port        : 3001

After that we first start our debuger and add the argument '--debug' in our CLI terminal:

    % python3 cli.py --box-uuid <box-uuid> --debug

### How to start tests 

Tests can be started with the following command structure:

    python3 cli.py --test Alcatel 

For other vendors replace 'Alcatel' with your desired vendor.


For more information see [test_structure.rst](https://github.com/inexio/NESi/blob/master/docs/source/test_structure.rst)

### Available Flags

#### api.py

`--recreate-db`

Recreate the underlying SQLite Database (Important for first run)

`--debug`

Launches the API in debug mode

`--load-model <vendor>`

load the data of vendor <vendor> into the underlying Database

`--help`

Displays help for available flags


#### cli.py

`--list_boxen`

Lists all available devices that were created in the database

`--box-uuid <uuid>`

Launches the device with the given uuid

`--daemon`

Launches the device in daemon mode

`--standalone <vendor>`

Launches the device without having to launch the API in a seperate window first

`--debug`

Launches the device in debug mode

`--help`

Displays help for available flags

### Docker

For people using Docker we included a dockerfile. 

You can build nesi using docker with the command
    
    % docker build . -t nesi

After building you can start the container via

    % docker run -(d)it nesi

### How to add new simulated CLI

For more information on this matter, please refer to the
[developer's documentation](https://github.com/inexio/NESi/blob/master/docs/source/development.rst).



### Issues

If you find any bug or a feature you think should be implemented, you can open up an [issue](https://github.com/inexio/NESi/issues/new).
We will take care of the problem as fast as we can!


### Contributing

Contributions to the project are welcome.

We are looking forward to your [pull requests](https://github.com/inexio/NESi/pulls), suggestions and fixes.

Happy Coding!

-----
Copyright (c) 2020
 
Original Software Design by [Ilya Etingof](https://github.com/etingof).


Software adapted by [inexio](https://github.com/inexio).

- [Janis Groß](https://github.com/unkn0wn-user)

- [Philip Konrath](https://github.com/Connyko65)

- [Alexander Dincher](https://github.com/Dinker1996)

<br/>


All rights reserved.
