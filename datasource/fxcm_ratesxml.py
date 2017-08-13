from lxml import etree

from datasource.types import *

def Fetch_DailyPrices( CURRENCY ):
    URL = 'http://rates.fxcm.com/RatesXML'
    table = etree.parse( URL ).getroot()

    # Fetch All Prices
    price = {}
    for ele in table:
        price[ele.get('Symbol')] = (float(ele.find('Bid').text) +
                                    float(ele.find('Ask').text)) /2

    # Build price_list[]
    price_list = []
    PIVOT = CURRENCY[0]

    for symbol in CURRENCY:
        if symbol == 'CNY':
            symbol = 'CNH'

        pivot_price = 0.0
        if symbol == PIVOT:
            pivot_price = 1.0
        elif PIVOT+symbol in price:
            pivot_price = price[PIVOT+symbol]
        elif symbol+PIVOT in price:
            pivot_price = 1.0/price[symbol+PIVOT]

        price_list.append( pivot_price )

    timestamp = table[0].find('Last').text
    print( 'FXCM RatesXML at {} Fetched'.format(timestamp) )
    return [ DailyPrices( timestamp, price_list ) ]
