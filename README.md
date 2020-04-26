# simulert
A package for generating alerts about simulations.

## Installation
This project has not made it to Pypi so installation will require cloning the repository
and adding it as a development package with either `pip install -e /path/to/simulert` or
`conda develop /path/to/simulert`.

## Usage
This package is architected similarly to Python's built-in logging package.
An `Alerter` class is instantiated with `getAlerter` and this class is triggered to send
alerts which are distributed to all the handlers registered with that class.

Current handlers include a logger (default), an emailer and a slack client.

The `Alerter` currently provides two ways to trigger alerts: most simply,calling the
`alert` method with a message; and possibly more conveniently, with the
`simulation_alert` context wrapping the simulation code.

## Example
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
with alerter.simulation_alert("super dooper sim"):
    run_simulation()
```

##TODO
1. Complete docstrings
1. Test email.py, logs.py and slack.py
1. Add default environment args to emailer
1. Write a better README.md
1. Tidy up pyproject.toml to include only necessary files
1. Setup Github
    1. Automated testing
    1. Branch protection
1. Deploy to Pypi via github with version management
1. Add a changelog
1. Add a logging handler as an event source.