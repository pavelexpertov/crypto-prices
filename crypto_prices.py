from datetime import datetime
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


def get_daily_price_history(currency_code_from, currency_code_to, number_of_days=10):
    parameters = {'fsym': currency_code_from.upper(), 'tsym': currency_code_to.upper(), 'limit': number_of_days}
    headers = {'authorization': 'Apikey ' + API_KEY}
    response = requests.get(DATA_API_URL_TEMPLATE.format('histoday'), params=parameters, headers=headers)
    return response.json()


@click.group()
def cli():
    '''A simple module to get prices for currencies cryptocurrencis as well as their history'''
    pass


@click.command()
@click.argument('currency_from')
@click.argument('currency_to')
def today(currency_from, currency_to):
    '''Get today's price based on given currency codes.'''
    click.echo('Price: {0}'.format(get_todays_price(currency_from, currency_to)))

@click.command()
@click.argument('currency_from')
@click.argument('currency_to')
def history(currency_from, currency_to):
    '''Get ten day history worth data based on given currency codes.'''
    json_data = get_daily_price_history(currency_from, currency_to)
    max_padding = max([len(str(day['close'])) for day in json_data['Data']])
    template = "{0}: {1: " + str(max_padding) + ".2f}"
    click.echo('template: ' + template)
    date_format = '%d %b'
    output_list = [template.format(datetime.fromtimestamp(day['time']).strftime(date_format), day['close'])
                   for day in json_data['Data']]
    click.echo('\n'.join(output_list))



cli.add_command(today)
cli.add_command(history)

if __name__ == '__main__':
    cli()
