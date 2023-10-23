from datetime import datetime, timedelta

# Date and Time - import these to easily create date parameters for different functions such as option aggregates, stock aggregates.
today = datetime.today().date()  # Current date
now = datetime.now()  # Current date and time
today_str = datetime.now().strftime('%Y-%m-%d')
today_str_yymmdd = datetime.now().strftime('%y%m%d')



headers_sec = {
    "Accept": "application/json",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
