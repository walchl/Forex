import math

# Currency Symbols
#CURRENCY = ['USD', 'EUR', 'GBP', 'CHF', 'JPY',
#            'AUD', 'NZD', 'CAD', 'SEK', 'CNY',
#            'HKD', 'SGD', 'RUB', 'ZAR', 'HUF']
CURRENCY = ['USD', 'EUR', 'GBP', 'CHF', 'JPY',
            'AUD', 'NZD', 'CAD', 'SEK', 'CNY',
            'HKD', 'ZAR']

# Parse argvs
def parse_argv( argv ):
    # Parameters
    FORWARD = 2
    RECORDS = 7

    if len(argv) > 1:
        FORWARD = int(argv[1])
    if len(argv) > 2:
        RECORDS = int(argv[2])

    return FORWARD, RECORDS

# Build forex_ln_diff, the Finite Difference
def build_forex_ln_diff( daily_prices, FORWARD, RECORDS ):
    # Allocate list of dict: forex_ln_diff
    forex_ln_diff = []
    for day in range(RECORDS):
        forex_ln_diff.append( {} )

    # Calculate ln_diff for each symbol
    for symbol_i in range(len(CURRENCY)):
        # Calculate ln for each day
        forex_ln = []
        for day in range(RECORDS+FORWARD):
            forex_ln.append( math.log( daily_prices[day].prices[symbol_i] ) )

        # Calculate diff between [day] and [day+FORWARD]
        for day in range(RECORDS):
            forex_ln_diff[day][CURRENCY[symbol_i]] = (
                forex_ln[day] - forex_ln[day+FORWARD])

    return forex_ln_diff

# Init rank_sum & rank_diff_min
def init_rank_info():
    # Init rank_sum
    rank_sum = {}
    for symbol in CURRENCY:
        rank_sum[symbol] = 0

    # Init rank_diff_min
    rank_diff_min = {}
    for i in CURRENCY:
        for j in CURRENCY:
            rank_diff_min[i+j] = float('inf')

    return rank_sum, rank_diff_min

# Update rank_sum & rank_diff_min by sorted_symbol
def update_rank_info(rank_sum, rank_diff_min, sorted_symbol):
    # Calculate rank_sum
    rank = {}
    rank_symbol = 0
    for symbol in sorted_symbol:
        rank[symbol] = rank_symbol
        rank_sum[symbol] += rank_symbol
        rank_symbol += 1

    # Update rank_diff_min
    for i in CURRENCY:
        for j in CURRENCY:
            if i != j:
                rank_diff_min[i+j] = min( rank_diff_min[i+j], rank[j]-rank[i] )
