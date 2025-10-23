# Control Tasmota Power Switch via APRS

A proof of consept script that will connect to a KISS TNC (such as a LoRa APRS iGate, Direwolf or any other KISS compatible TNC). It will listen for messages sent to it's call sign, from the administrators call sign. If such a message contains the words "POWER ON" or "POWER OFF" (case insensitive) it will execute the respective command on the configured Tasmota device.

Tested with the Sonoff Basic unit only!

## Security warning

APRS does not offer any protection against spoofing. This means anyone can technically send messages from any call sign, including the one you have set as an administrator!

## Installation

Download the zip-file and unzip or check out with git. Open a shell or command prompt and change directory to the downloaded project folder:

```shell
cd path/to/project
```

### Initialise a virtual environment:

```shell
python -m venv .venv
```

### Activate the virtual environment:

#### PowerShell

```shell
.venv/Scripts/Activate.ps1
```

#### BASH

```shell
source .venv/Scripts/activate
```

### Install requirement in the virtual environment

```shell
pip install -r requirements.txt
```

## Configuration

The script gets its configuration from the following 5 environment variables

### `CALL`

The call sign the script will accept messages for. Can be a proper call sign or up to 7 alphanumeric characters.

#### Example

##### PowerShell

```shell
$env:CALL="LAMP"
```

##### BASH

```shell
export CALL="LAMP"
```

### `ADMIN`

The call sign allowed to execute commands. Can be any 7 alphanumeric characters but will probably be a proper call sign including SSID.

#### Example

##### PowerShell

```shell
$env:ADMIN="LB5JJ-2"
```

##### BASH

```shell
export ADMIN="LB5JJ-2"
```

### `TASMOTA`

The base URL of the Tasmota unit to control.

##### PowerShell

```shell
$env:TASMOTA="http://192.168.10.213/cm?"
```

##### BASH

```shell
export TASMOTA="http://192.168.10.213/cm?"
```


### `TNC_HOST` and `TNC_PORT`

The hostname/IP and port of the TNC used to received messages and send acknowledgements.

```shell
$env:TNC_HOST="192.168.10.246"
$env:TNC_PORT="8001?"
```

##### BASH

```shell
export TNC_HOST="192.168.10.246"
export TNC_PORT="8001?"
```

## Running

Once the requirements have been installed and the environment variables set, start the server by running the server script.

```shell
python main.py
```

