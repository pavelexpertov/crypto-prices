import click
import requests


@click.group()
def cli():
    '''A simple module to get prices for currencies cryptocurrencis as well as their history'''
    pass


@click.command()
@click.argument('currency_from')
@click.argument('currency_to')
def today(currency_from, currency_to):
    click.echo('currency ' + currency_from)
    click.echo('currency to ' + currency_to)


cli.add_command(today)

if __name__ == '__main__':
    cli()
