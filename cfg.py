from datetime import datetime, timedelta

# Date and Time - import these to easily create date parameters for different functions such as option aggregates, stock aggregates.
today = datetime.today().date()  # Current date
now = datetime.now()  # Current date and time
today_str = datetime.now().strftime('%Y-%m-%d')
today_str_yymmdd = datetime.now().strftime('%y%m%d')
five_days_ago_str = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

two_days_from_now_str = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
two_days_ago_str = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
five_days_from_now_str = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
thirty_days_ago_str = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
fifteen_days_ago_str = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
nine_days_ago_str = (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')
thirty_days_str = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
seven_days_from_now_str = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
eight_days_from_now_str = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
fifteen_days_from_now_str = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
two_years_ago_str = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
two_years_from_now_str = (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d')
thirty_days_from_now_str = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
fudstop='https://media.discordapp.net/attachments/938986871223091231/941121473450491934/FS_Logo_5.gif'
hex_colors = {
    'black': '000000',
    'white': 'FFFFFF',
    'red': 'FF0000',
    'green': '00FF00',
    'blue': '0000FF',
    'yellow': 'FFFF00',
    'cyan': '00FFFF',
    'magenta': 'FF00FF',
    'gray': '808080',
    'silver': 'C0C0C0',
    'maroon': '800000',
    'olive': '808000',
    'purple': '800080',
    'teal': '008080',
    'navy': '000080',
    'fuchsia': 'FF0080',
    'lime': '00FF80',
    'aqua': '00FFFF',
    'orange': 'FFA500',
    'pink': 'FFC0CB',
    'lavender': 'E6E6FA',
    'sky blue': '87CEEB',
    'forest green': '228B22',
    'dark slate gray': '2F4F4F',
    'chocolate': 'D2691E',
    'goldenrod': 'DAA520',
    'deep pink': 'FF1493',
    'tomato': 'FF6347',
    'dark orchid': '9932CC',
    'steel blue': '4682B4'
}
headers_sec = {
    "Accept": "application/json",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
