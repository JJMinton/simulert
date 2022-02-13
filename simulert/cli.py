import click
import runpy
from pathlib import Path

from simulert import getAlerter
from simulert.handlers import Emailer, Slacker, Pushover

alerter = getAlerter()


@click.group()
# E-mail handler CLI options
@click.option("-e", "--email", help="attach email handler", is_flag=True)
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
# Slack handler CLI options
@click.option("-s", "--slack", help="attach slack handler", is_flag=True)
@click.option(
    "--slackToken", help="the token for the slack-bot used to send messages from.",
)
@click.option(
    "--slackUsername", help="the username of the slack user to send messages to.",
)
# Pushover handler CLI options
@click.option("-p", "--pushover", help="attach pushover handler", is_flag=True)
@click.option(
    "--pushoverToken", help="the token for the pushover integration used for sending messages.",
)
@click.option(
    "--pushoverUsername", help="the username of the pushover account used for sending messages.",
)
def cli(
    email,
    emailhost,
    emailport,
    emailauthentication,
    emailsender,
    emailrecipient,
    slack,
    slacktoken,
    slackusername,
    pushover,
    pushovertoken,
    pushoverusername,
):
    if not slack and not email and not pushover:
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
    if pushover:
        pushover_handler = Pushover(pushovertoken, pushoverusername)
        alerter.add_handler(pushover_handler)


@cli.command()
@click.option("-n", "--name", help="simulation name")
@click.argument("filename", required=True)
def run(name, filename):
    with alerter.simulation_alert(name):
        runpy.run_path(str(Path.cwd() / filename))
