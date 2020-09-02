
# Network Equipment Simulator (NESi)
### (former Softboxen)

[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/inexio/NESi/master/LICENSE.rst)
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/api_build?label=build)]()




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

## Features


[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_alcatel?label=alcatel_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_huawei?label=huawei_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_edgecore?label=edgecore_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_keymile?label=keymile_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_pbn?label=pbn_tests)]()
[![GitHub build](https://img.shields.io/github/workflow/status/inexio/NESi/test_zhone?label=zhone_tests)]()

### Supported Vendors
 - Alcatel  (nearly feature complete)
 - Huawei   (work in progress)
 - Edgecore (not implemented yet)
 - Keymile  (not implemented yet)
 - Pbn      (not implemented yet)
 - Zhone    (not implemented yet)

### Supported network components

- Subracks
- Cards
- Ports
- ONTs
- CPEs
- Vlans


## Download

The `NESi` package is distributed under terms and conditions of 2-clause BSD [license](https://github.com/inexio/NESi/blob/master/LICENSE.rst). 

Furthermore the previous `softboxen` project is freely available as a GitHub [repository](https://github.com/etingof/softboxen) or can be downloaded from [PyPI](https://pypi.org/project/softboxen).

## Installation

Either clone the repository with the following command:
```shell script
$ git clone git@github.com:inexio/NESi.git
```
After that, make sure you have installed the required python packages found in the requirements.txt. An easy way to do this is with the following command:
```shell script
$ pip install -r requirements.txt
```

## How to use NESi

The easiest way to play with the example CLI is to run two terminals on the NESi
repo - one that starts up the REST API server and populates the example model in
the underlying DB, and another that simulates the devices Command Line Interface and runs against the REST API server.

REST API terminal:

    $ ./bootup/restapi.sh --keep-running [--recreate-db]


CLI terminal:

First we collect the uuid´s of all boxes

    % ./bootup/box.sh --list-boxen

    Vendor Alcatel, model 7360, version FX-4, instance 1
    
Second we connect to one box with the specific uuid

    % ./bootup/box.sh --box-uuid <box-uuid> 

          _   _ ______  _____ _ 
         | \ | |  ____|/ ____(_)
         |  \| | |__  | (___  _ 
         | . ` |  __|  \___ \| |
         | |\  | |____ ____) | |
         |_| \_|______|_____/|_|
    
    
    Hint: login credentials: admin/secret
    
    login:admin
    Password:secret
    Last login on 01.03.2020

Interactive menus will guide you through the implemented commands.


### How to use debug mode

First we configure a debugger in our IDE. Therefore we add a Python Debug Server with pydevd_pycharm. 

    Host name   : localhost
    Port        : 3001

After that we first start our debuger and add the argument '--debug' in our CLI terminal:

    % ./bootup/box.sh --box-uuid <box-uuid> --debug

### How to start tests 

Tests can be started with the following command structure:

    % ./bootup/restapi.sh --test-alcatel-commands 

For other vendors replace 'alcatel' with your desired vendor, or use:

    % ./bootup/restapi.sh --help


 
### How to add new simulated CLI

For more information on this matter, please refer to the
[developer's documentation](https://github.com/inexio/NESi/blob/master/docs/source/development.rst).

-----

Copyright (c) 2020
 
Original Software Design by [Ilya Etingof](https://github.com/etingof).


Software adapted by [inexio](https://github.com/inexio).

- [Janis Groß](https://github.com/unkn0wn-user)

- [Philip Konrath](https://github.com/Connyko65)

- [Alexander Dincher](https://github.com/Dinker1996)

<br/>


All rights reserved.
