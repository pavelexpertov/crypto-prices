import os
import configparser

import click
import requests

config_file_parser = configparser.ConfigParser()
expanded_path = os.path.expanduser('~/.config/crypto-prices/config.ini')
config_file_parser.read(expanded_path)
API_KEY = config_file_parser['api']['key']
DATA_API_URL_TEMPLATE = 'https://min-api.cryptocompare.com/data/{0}'

def get_todays_price(currency_code_from, currency_code_to):
    '''Return today's price based on a given currency code'''
    parameters = {'fsym': currency_code_from.upper(), 'tsyms': currency_code_to.upper()}
    headers = {'authorization': 'Apikey ' + API_KEY}
    response = requests.get(DATA_API_URL_TEMPLATE.format('price'), params=parameters, headers=headers)
    return response.json()[currency_code_to.upper()]


@click.group()
def cli():
    '''A simple module to get prices for currencies cryptocurrencis as well as their history'''
    pass


@click.command()
@click.argument('currency_from')
@click.argument('currency_to')
def today(currency_from, currency_to):
    click.echo('Price: {0}'.format(get_todays_price(currency_from, currency_to)))


cli.add_command(today)

if __name__ == '__main__':
    cli()
