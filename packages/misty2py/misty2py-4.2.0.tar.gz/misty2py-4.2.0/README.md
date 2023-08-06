# Misty2py

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/ChrisScarred/misty2py/blob/main/LICENSE)

Misty2py is a Python 3 package for Misty II development using [Misty's REST API](https://docs.mistyrobotics.com/misty-ii/rest-api/api-reference/ "Misty Robotics REST API").

## Installation

### Poetry

To install misty2py, run `pip install misty2py`.

### From source

- If this is your first time using `misty2py` from source, do following:

  - Get Poetry (`python -m pip install poetry`) if you do not have it yet.
  - Copy `.env.example` to `.env`.
  - Replace the placeholder values in the new `.env` file.
  - Run `poetry install` to obtain all dependencies.

- Run the desired script via `poetry run python -m [name]` where `[name]` is the placeholder for the module location (in Python notation).
- If the scripts run but your Misty does not seem to respond, you have most likely provided an incorrect IP address for `MISTY_IP_ADDRESS` in `.env`.
- Pytests can be run via `poetry run pytest .`.
- The coverage report can be obtained via `poetry run pytest --cov-report html --cov=misty2py tests` for HTML output or via `poetry run pytest --cov=misty2py tests` for terminal output.

## Features

Misty2py can be used to develop complex skills (behaviours) for the Misty II robot utilising:

- **actions** via sending a `POST` or `DELETE` requests to Misty's API;
- **informations** via sending a `GET` request to Misty's API;
- **continuous streams of data** via subscribing to event types on Misty's websockets.

Misty2py uses following concepts for easy of usage:

- **action keywords** - customisable python-styled keywords for endpoints of Misty's API that correspond to performing actions;
- **information keywords** - customisable python-styled keywords for endpoints of Misty's API that correspond to retrieving information;
- **data shortcuts** - customisable python-styled keywords for commonly used data that are supplied to Misty's API as the body of a `POST` request.

## Usage

### Getting started

- Start by making **a new instance** of `misty2py.robot`'s `Misty` by `misty_robot = Misty("ip_address_here")`
  - Substitute `ip_address_here` with the IP address of your Misty.
  - `misty2py.utils.env_loader` module contains `EnvLoader` class that can be used to load Misty's IP from the .env file in your project's home directory:
    - Create the `.env` file and write `MISTY_IP_ADDRESS="[ip_address_here]"` in it.
    - Initialise an `EnvLoader` object via `env_loader = EnvLoader()`; this loads the environment variables.
    - Use `env_loader.get_ip()` to obtain the IP address.
- Use the method `misty_robot.perform_action()` to tell Misty to **perform an action**.
- Use the method `misty_robot.get_info()` to tell Misty to **return information**.
- Use the method `misty_robot.event()` to initialise, obtain and stop **continuous streams of data** from Misty's event types.

### Obtaining information

Obtaining digital information is handled by `misty2py.robot::get_info` method.

`misty2py.robot::get_info` has following arguments:

- `info_name` - *required;* the string information keyword corresponding to an endpoint in Misty's API;
- `params` - *optional;* a dictionary of parameter name and parameter value pairs, defaults to `{}`.

### Performing actions

Performing physical and digital actions including removal of non-system files is handled by `misty2py.robot::perform_action()` method.

`misty2py.robot::perform_action()` has following arguments:

- `action_name` - *required;* the string action keyword corresponding to an endpoint in Misty's API;
- `data` - *optional;* the data to pass to the request as a dictionary or a data shortcut (string), defaults to `{}`.

### Event types

To obtain event data in Misty's framework, it is required to **subscribe** to an event type on Misty's websocket server. Misty's websocket server then streams data to the websocket client, in this implementation via a separate thread. To **access this data,** `misty2py.robot::event` method must be called with `"get_data"` parameter from the main thread. When data are no longer required to be streamed to the client, an event type can be **unsubscribed** to kill the event thread.

#### Subscription

Subscribe to an event via `misty2py.robot::event` with the parameter `"subscribe"` and following keyword arguments:

    - `type` - *required;* event type string as documented in [Event Types Docs](https://docs.mistyrobotics.com/misty-ii/robot/sensor-data/ "Misty Robotics Event Types").
    - `name` - *optional;* a custom event name string; must be unique.
    - `return_property` - *optional;* the property to return from Misty's websockets; all properties are returned if return_property is not supplied.
    - `debounce` - *optional;* the interval in ms at which new information is sent; defaults to 250.
    - `len_data_entries` - *optional;* the maximum number of data entries to keep (discards in fifo style); defaults to 10.
    - `event_emitter` - *optional;* an event emitter function which emits an event upon message recieval. Supplies the message content as an argument.

#### Accessing the data and the log

Access the data of an event or its log via `misty2py.robot::event` with the parameter `"get_data"` or `"get_log"` and a keyword argument `name` (the name of the event).

#### Unsubscribing

Unsubscribe from an event via `misty2py.robot::event` with the parameter `"unsubscribe"` and a keyword argument `name` (the name of the event).

#### Basic example

```python
import time

from misty2py.robot import Misty
from misty2py.utils.env_loader import EnvLoader

env_loader = EnvLoader

m = Misty(env_loader.get_ip())

d = m.event("subscribe", type = "BatteryCharge")
e_name = d.get("event_name")

time.sleep(1)

d = m.event("get_data", name = e_name)

d = m.event("unsubscribe", name = e_name)
```

#### Event emitter usage - example

```python
import time
from pymitter import EventEmitter

from misty2py.robot import Misty
from misty2py.utils.env_loader import EnvLoader

env_loader = EnvLoader

m = Misty(env_loader.get_ip())
ee = EventEmitter()
event_name = "myevent_001"

@ee.on(event_name)
def listener(data):
    print(data)

d = m.event("subscribe", type = "BatteryCharge", name = event_name, event_emitter = ee)

time.sleep(2)

d = m.event("unsubscribe", name = event_name)
```

### Adding custom keywords and shortcuts

Custom keywords and shortcuts can be passed to a Misty object while declaring a new instance by using the optional arguments:

- `custom_info` for custom information keywords (a dictionary with keys being the information keywords and values being the endpoints),
- `custom_actions` for custom action keywords (a dictionary with keys being the action keywords and values being a dictionary `{"endpoint" : "edpoint_value", "method" : "method_value"}` where `method_value` is either `post` or `delete`),
- `custom_data` for custom data shortcuts (a dictionary with keys being the data shortcuts and values being the dictionary of data values).

An example:

```python
custom_allowed_infos = {
    "hazards_settings": "api/hazards/settings"
}

custom_allowed_data = {
    "amazement": {
        "FileName": "s_Amazement.wav"
    },
    "red": {
        "red": "255",
        "green": "0",
        "blue": "0"
    }
}

custom_allowed_actions = {
    "audio_play" : {
        "endpoint" : "api/audio/play",
        "method" : "post"
    },
    "delete_audio" : {
        "endpoint" : "api/audio",
        "method" : "delete"
    }
}

misty_robot = Misty("0.0.0.0", 
    custom_info=custom_allowed_infos, 
    custom_actions=custom_allowed_actions, 
    custom_data=custom_allowed_data)
```
