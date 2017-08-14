from datetime import datetime, timedelta
from forex_python.converter import CurrencyRates

from datasource.types import *

def Fetch_DailyPrices( CURRENCY, DAYS ):
    cr = CurrencyRates()
    PIVOT = CURRENCY[0]

    # Init Return Values
    daily_prices = []

    today = datetime.now()
    daysdelta = 0
    cr_pivot_last = []
    while len(daily_prices) < DAYS:
        datetime_current = today - timedelta(days=daysdelta)
        cr_pivot_current = cr.get_rates(PIVOT,datetime_current)
        daysdelta += 1

        # Skip Identical
        if len(daily_prices)>0 and cr_pivot_last==cr_pivot_current:
            daily_prices[-1].label = datetime_current.date()
            continue

        # Init Price List
        price_list = []
        for symbol in CURRENCY:
            if symbol == PIVOT:
                price_list.append( 1.0 )
            else:
                price_list.append( cr_pivot_current[symbol] )
        cr_pivot_last = cr_pivot_current

        # Append data & price_list
        daily_prices.append( DailyPrices(datetime_current.date(), price_list) )
        print( '{} Fetched'.format(daily_prices[-1].label) )

    return daily_prices
