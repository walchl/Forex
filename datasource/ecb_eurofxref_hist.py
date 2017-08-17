import requests
from lxml import etree

from datasource.types import *

def Fetch_DailyPrices( CURRENCY, DAYS ):
    URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    XMLText = ''

    while True:
        try:
            XMLText = requests.get( URL, timeout=1.0 ).text
            break
        except:
            print( 'Retry:', URL )

    table = etree.fromstring( XMLText.encode('utf-8') )[2]

    # Init Return Values
    daily_prices = []

    for day in range(DAYS):
        # Get label
        label = table[day].get( 'time' )

        # Build price_dist
        price_dist = {}
        for child in table[day]:
            price_dist[ child.get('currency') ] = float( child.get('rate') )

        # Build price_list
        price_list = []
        for symbol in CURRENCY:
            price = 1.0 if symbol=='EUR' else price_dist[symbol]
            price_list.append( price )

        # Append label & price_list
        daily_prices.append( DailyPrices( label, price_list ) )
        print( '{} Fetched'.format(daily_prices[-1].label) )

    return daily_prices
