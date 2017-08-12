import sys

import datasource.forex_python as src_forex
import datasource.fxcm_ratesxml as src_fxcm
import analysis_ranking_defs as defs

# Parameters
FORWARD, RECORDS = defs.parse_argv( sys.argv )

# Fetch Latest Price by fxcm_rates
# Fetch CurrencyRates by python_forex
daily_prices = (
            src_fxcm.Fetch_DailyPrices( defs.CURRENCY ) +
            src_forex.Fetch_DailyPrices( defs.CURRENCY, RECORDS+FORWARD-1 ) )

# Allocate list of dict: forex_ln_diff
forex_ln_diff = defs.build_forex_ln_diff( daily_prices, FORWARD, RECORDS )

# Init rank_sum & rank_diff_min
rank_sum, rank_diff_min = defs.init_rank_info()

# Output Daily Records
print( '\n*** {} Day(s) Forwarding, {} Record(s) ***'
        .format(FORWARD, RECORDS) )

for day in range(RECORDS):
    sorted_symbol = sorted( forex_ln_diff[day], key=forex_ln_diff[day].get )
    if day == 0:
        print( '{:^10}'.format(daily_prices[day].timestamp), sorted_symbol )
    else:
        print( daily_prices[day].timestamp, sorted_symbol )

    # update rank_sum & rank_diff_min
    defs.update_rank_info( rank_sum, rank_diff_min, sorted_symbol )

# Output Rank Scoring
print( '\n*** Ranking ***\n', sorted(rank_sum, key=rank_sum.get) )

# Output The Most Stable Pairs
print( '\n*** Stable Pairs ***' )
last_diff = float('inf')
printed_pairs = 0
while printed_pairs < 5:
    max_diff = float('-inf')

    for key, diff in rank_diff_min.items():
        # Skip large diff
        if last_diff <= diff:
            continue
        # Update max
        max_diff = max( max_diff, diff )

    last_diff = max_diff

    for key, diff in rank_diff_min.items():
        if max_diff == diff:
            print( key, max_diff )
            printed_pairs += 1
