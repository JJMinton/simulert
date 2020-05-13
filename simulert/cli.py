import runpy
from pathlib import Path

import click

from simulert import getAlerter
from simulert.handlers import Emailer, Slacker

alerter = getAlerter()


@click.command()
@click.argument("filename", required=True)
@click.option("-n", "--name", help="simulation name")
@click.option("-e", "--email", help="attach email handler", is_flag=True)
@click.option("-s", "--slack", help="attach slack handler", is_flag=True)
@click.option(
    "--slackToken", help="the token for the slack-bot used to send messages from.",
)
@click.option(
    "--slackUsername", help="the username of the slack user to send messages to.",
)
@click.option("--emailHost", help="the host address of the email server to send from.")
@click.option(
    "--emailPort", help="the connection port of the email server to send from."
)
@click.option(
    "--emailAuthentication",
    help="comma-separated username and password to authenticate to the email server.",
)
@click.option("--emailSender", help="comma-separated sender name and email address")
@click.option(
    "--emailRecipient", help="comma-separated receiver name and email address"
)
def cli(
    filename,
    name,
    email,
    slack,
    slacktoken,
    slackusername,
    emailhost,
    emailport,
    emailauthentication,
    emailsender,
    emailrecipient,
):
    if not slack and not email:
        print(
            "Try 'simulert --help' for help.\n\nError: Please specify at least one handler."
        )
        exit(0)
    if slack:
        slacker = Slacker(slacktoken, slackusername)
        alerter.add_handler(slacker)
    if email:
        emailer = Emailer(
            emailhost, emailport, emailauthentication, emailsender, emailrecipient,
        )
        alerter.add_handler(emailer)

    with alerter.simulation_alert(name):
        runpy.run_path(Path.cwd() / filename)
