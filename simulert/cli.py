import click
import os
import runpy

from simulert import getAlerter
from simulert.handlers import Emailer, Slacker

alerter = getAlerter()

@click.group()
@click.option('-e', '--email', help='attach email handler', is_flag=True)
@click.option('-s', '--slack', help='attach slack handler', is_flag=True)
@click.option('--simulertSlackToken', help='the token for the slack-bot used to send messages from.')
@click.option('--simulertSlackUsername', help='the username of the slack user to send messages to.')
@click.option('--simulertEmailHost', help='the host address of the email server to send from.')
@click.option('--simulertEmailPort', help='the connection port of the email server to send from.')
@click.option('--simulertEmailAuthentication', help='comma-separated username and password to authenticate to the email server.')
@click.option('--simulertEmailSender', help='comma-separated sender name and email address')
@click.option('--simulertEmailRecipient', help='comma-separated receiver name and email address')
def cli(email, slack, simulertslacktoken=None, simulertslackusername=None, simulertemailhost=None, simulertemailport=None, simulertemailauthentication=None, simulertemailsender=None, simulertemailrecipient=None):
    if not slack and not email:
        print("Try 'simulert --help' for help.\n\nError: Please specify at least one handler.")
        exit(0)
    if slack:
        slacker = Slacker(simulertslacktoken, simulertslackusername)
        alerter.add_handler(slacker)
    if email:
        emailer = Emailer(
            simulertemailhost,
            simulertemailport,
            simulertemailauthentication,
            simulertemailsender,
            simulertemailrecipient,
        )
        alerter.add_handler(emailer)


@cli.command()
@click.option('-n', '--name', help='simulation name')
@click.argument('method', required=True)
def run(name, method):
    with alerter.simulation_alert(name):
        runpy.run_path(os.path.join(os.getcwd(), method))
