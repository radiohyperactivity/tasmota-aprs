# Control Tasmota Power Switch via APRS

A proof of concept script that will connect to a KISS TNC (such as a LoRa APRS iGate, Direwolf or any other KISS compatible TNC). It will listen for messages sent to it's callsign, from the administrators callsign. If such a message contains the words "POWER ON", "POWER OFF" or "POWER CYCLE" (case insensitive) it will execute the respective command on the configured Tasmota device.

Tested with the Sonoff Basic unit only!

## Security warning

APRS does not offer any protection against spoofing. This means anyone can technically send messages from any callsign, including the one you have set as an administrator!

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

The callsign the script will accept messages for. Can be a proper callsign or up to 6 alphanumeric characters.

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

The callsign allowed to execute commands. Can be any 6 alphanumeric characters but will probably be a proper callsign including SSID.

#### Example

##### PowerShell

```shell
$env:ADMIN="LB5JJ-4"
```

##### BASH

```shell
export ADMIN="LB5JJ-4"
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
$env:TNC_PORT="8001"
```

##### BASH

```shell
export TNC_HOST="192.168.10.246"
export TNC_PORT="8001"
```

### `SYSLOG_HOST`

The IP of a syslog server for logging

##### PowerShell

```shell
$env:SYSLOG_HOST="127.0.0.1"
```

##### BASH

```shell
export SYSLOG_HOST="127.0.0.1"
```

## Running

Once the requirements have been installed and the environment variables set, start the server by running the server script.

```shell
python main.py
```

## Usage

When everything is configured correctly and up and running, you should be able to send APRS messages from the configured ADMIN callsign to the configured CALL callsign. To switch the power on, the message needs to contain (case insensitive):

```
POWER ON
```

To turn the power off, send (again, case insensitive):

```
POWER OFF
```

And lastly, to power cycle (power off, wait 5 seconds, power on), send (still case insensitive):

```
POWER CYCLE
```

## Known bugs and shortcomings

- Will not understand messages relayed via APRS-IS
