from lxml import etree

from datasource.types import *

def Fetch_DailyPrices( CURRENCY ):
    URL = 'http://rates.fxcm.com/RatesXML3'
    table = etree.parse( URL ).getroot()

    # Fetch All Prices
    price = {}
    for ele in table:
        price[ele.find('Symbol').text] = (
            (float(ele.find('Bid').text) + float(ele.find('Ask').text)) /2,
            ele.find('Last').text, ele.find('Date').text )

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
            pivot_price = price[PIVOT+symbol][0]
        elif symbol+PIVOT in price:
            pivot_price = 1.0/price[symbol+PIVOT][0]

        price_list.append( pivot_price )

    eur = price['EURUSD']
    print( 'FXCM RatesXML at ({},{}) Fetched'.format( eur[1], eur[2] ) )
    return [ DailyPrices( eur[1], price_list ) ]
