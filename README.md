# simulert
A package for generating alerts about simulations.

## Installation
This project has not made it to Pypi so installation will require cloning the repository and adding it as a development package with either
`pip install -e /path/to/simulert` or `conda develop /path/to/simulert`.

## Usage
This package is architected similarly to Python's built-in logging package.
An `Alerter` class is instantiated with `getAlerter` and this class is triggered to send alerts which are distributed to all the handlers registered with that class.

Current handlers include a logger (default) and an emailer.

The `Alerter` currently provides two ways to trigger alerts: most simply,calling the `alert` method with a message; and possibly more conveniently,
with the `simulation_alert` context wrapping the simulation code.

## Example
```python
from simulert.alerter import getAlerter
from simulert.handlers.emailer import Emailer

emailer = Emailer(
    username,
    password,
    ("Simulations", "noreply_simulations@company.com"),
    ("Data scientist", "scientist@company.com"),
    "smtp.mailserver.company.com",
)
alerter = getAlerter().add_handler(emailer)
with alerter.simulation_alert("super dooper sim"):
    run_simulation()
```

##TODO
1. Complete docstrings
1. Expose imports via __init__.py
1. Test emailer and logger
1. Add default environment args to emailer
1. Write a better README.md
1. Tidy up pyproject.toml to include only necessary files
1. Setup Github
    1. Automated testing
    1. Branch protection
1. Deploy to Pypi via github with version management
1. Add a changelog
1. Add a Slack handler
1. Add a logging handler as an event source.