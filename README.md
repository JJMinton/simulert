# Simulert
![Run Pytest and Lint](https://github.com/JJMinton/simulert/workflows/Run%20Pytest%20and%20Lint/badge.svg)

How often do your simulations fail moments after you close the terminal and head home
for the evening? Do you repeatedly check on your simulations to see how they're doing?
Have you ever left a long simulations for days longer than it needed?
This package is for configuring alerts for your simulations so you get told what's
happened, when it's happened and in the format that best suits you.

## Installation
An early release has been made available onn Pypi so install via pip:
`pip install simulert`. Or for the latest, clone this repository and adding it as a
development package with either `pip install -e /path/to/simulert` or
`conda develop /path/to/simulert`.

## Usage
This package is architected similarly to Python's built-in logging package.
An `Alerter` class is instantiated with `getAlerter()` and is triggered to send
alerts to all the handlers registered with it.

Current handlers include a logger (default), an emailer and a slack client.

The `Alerter` currently provides two ways to trigger alerts: most simply, calling the
`alert` method with a message; and possibly more conveniently, with the
`simulation_alert` context wrapping the simulation code.

## Environment variable configuration
The handlers will take default arguments from environment variables so that this package
can be configured globally for the fewest lines to alerts.

##### Email hander:
* `SIMULERT_EMAIL_HOST`: the host address of the email server to send from.
* `SIMULERT_EMAIL_PORT`: the connection port of the email server to send from.
* `SIMULERT_EMAIL_AUTHENTICATION`: comma-separated username and password to authenticate
    to the email server.
* `SIMULERT_EMAIL_SENDER`: comma-separated sender name and email address
* `SIMULERT_EMAIL_RECIPIENT`: comma-separated receiver name and email address


##### Slack handler:
* `SIMULERT_SLACK_TOKEN`: the token for the slack-bot used to send messages from.
* `SIMULERT_SLACK_USERNAME`: the username of the slack user to send messages to.


## Example
The verbose and transparent example:
```python
from simulert import getAlerter
from simulert.handlers import Emailer, Slacker

emailer = Emailer(
    "username",
    "password",
    ("Simulations", "noreply_simulations@company.com"),
    ("Data scientist", "scientist@company.com"),
    "smtp.mailserver.company.com",
)
slacker = Slacker("slack_app_token", "username")
alerter = getAlerter().add_handler(emailer).add_handler(slacker)
alerter.alert("Something special has happened in my code")
```
which will send "Something special has happened in my code" to the log files, to
`scientist@company.com` and to `@username` on slack.

The convenient example, with environment variables configured:
```python
from simulert import getAlerter
from simulert.handlers import Slacker
alerter = getAlerter("BigSims").add_handler(Slacker())
with alerter.simulation_alert("super dooper sim"):
    run_simulation()
```
which will send "BigSims: super dooper sim has completed without error." via slack once
`run_simulation()` has completed.

## CLI Usage
Simulert can also be used from the command line with the `simulert` command
that is automatically added on `pip install simulert`. To use, specify the
options followed by `run` and then the python file you would like to run.

For example, to run the simulation `hello_world.py` with a slack handler
using the set environment variables. 

    simulert -s run ~/hello_world.py --name my_simulation

See `simulert --help` for a comprehensive usage guide. 
      
## TODO
1. Test logs.py
1. Tidy up pyproject.toml to include only necessary files
1. Add a changelog
1. Add a logging handler as an event source.
