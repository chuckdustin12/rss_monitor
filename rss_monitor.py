import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import feedparser
from discord_webhook import DiscordEmbed, AsyncDiscordWebhook
from cfg import headers_sec, two_days_ago_str, fudstop, today_str
from sec_embed import send_sec_embed,sec_filing_titles
from helpers import get_cik_by_ticker

real_subs=["BVN", "BHC", 'I:SPX', 'I:VIX', 'I:NDX', "AMC", "BYND", "SNAP", "TAL", "AGNC", "NIO", "AAOI", "RIOT", "TEVA", "ETRN", "ZIM", "NOVA", "HOOD", "VTRS", "LYFT", "KEY", "ENVX", "WBD", "GPS", "WW", "DB", "STNE", "RUN", "VKTX", "HTZ", "NYCB", "UPWK", "SOXS", "M", "LMND", "PARA", "AROC", "F", "GT", "SPXU", "AAL", "VALE", "CCL", "BILI", "ET", "ABR", "PAAS", "PBR", "FYBR", "BITO", "GRPN", "GOLD", "T", "JWN", "IONQ", "NVCR", "GME", "OSTK", "PCG", "CLF", "BEKE", "PLTR", "PTGX", "KMI", "SPXS", "TSLL", "NCLH", "AEO", "SAVE", "VFC", "TDS", "PATH", "JETS", "CPNG", "MP", "LTHM", "TOST", "NLY", "AFRM", "XPEV", "IEP", "FSLY", "CHWY", "TDOC", "FL", "SOXL", "STLA", "CVE", "NOV", "SLV", "MANU", "KVUE", "SQQQ", "KSS", "PENN", "BYLD", "MXL", "WBA", "DOCN", "LNC", "PPC", "RIVN", "BTU", "AR", "BBIO", "AI", "MRO", "QQMG", "ALLY", "ONON", "ASHR", "FXI", "EWG", "YINN", "GDX", "BAC", "HPQ", "TNA", "TRUP", "PINS", "KWEB", "UPST", "EPD", "SDOW", "AA", "TFC", "LUV", "JD", "CRTO", "DKNG", "EWZ", "U", "RBLX", "UUP", "BTI", "GDXJ", "CSX", "EWU", "COHR", "GM", "SPIB", "UCO", "USB", "VZ", "SU", "OPCH", "FNGS", "X", "XLF", "WMB", "B", "KHC", "PFE", "ZION", "MOS", "TZA", "MGM", "SLG", "LI", "NEM", "FLR", "FCX", "INTC", "TQQQ", "DAL", "CCJ", "BP", "EEM", "APLS", "CVNA", "MTCH", "APA", "VRT", "HAL", "ARKK", "WFC", "TECK", "CMA", "EQT", "C", "CPB", "UPRO", "KRE", "TBT", "UAL", "DOCU", "MO", "SE", "SQ", "YELP", "EBAY", "WAL", "DVN", "AEM", "CMCSA", "Z", "LVS", "CZR", "UBER", "WDC", "SMG", "TSN", "DPST", "IAC", "STNG", "XME", "NEE", "DOW", "SCHW", "BSX", "MNST", "AAP", "SHOP", "SIMO", "BUD", "MRVL", "CSCO", "FIS", "FUTU", "CARR", "KO", "FAS", "SLB", "TWLO", "BOIL", "BMY", "XLU", "EWY", "EWJ", "W", "KOLD", "FTNT", "PYPL", "EDU", "NET", "XRT", "MET", "OXY", "RIO", "CAMT", "SHEL", "ETSY", "ZM", "AZN", "EFA", "MU", "KMX", "XLP", "CVS", "XBI", "RTX", "ROKU", "HYG", "COIN", "DD", "GDDY", "XPO", "GILD", "XHB", "USO", "IYR", "MDT", "SPB", "SPXL", "MCHP", "DASH", "OKTA", "MS", "DIS", "TTD", "EMB", "BABA", "CROX", "XLE", "TLT", "TSM", "FND", "MMM", "WYNN", "DDOG", "RCL", "ON", "IEF", "SBUX", "ATVI", "ABT", "NKE", "NVS", "PDD", "XLI", "EXPE", "LQD", "GNRC", "MRK", "TIP", "AMD", "BX", "MRNA", "TGT", "ORCL", "GE", "QCOM", "XOM", "IEI", "COP", "HZNP", "ENPH", "DLR", "EOG", "SEDG", "AMZN", "ABNB", "BIDU", "XLV", "VLO", "GOOGL", "GOOG", "XOP", "TMUS", "RSP", "AMAT", "TTWO", "IBM", "MPC", "JPM", "SMH", "FANG", "PG", "AXP", "ABBV", "HLT", "FSLR", "SNOW", "UPS", "ZS", "JNJ", "TXN", "ALB", "SPOT", "XLY", "WMT", "CVX", "CRWD", "XLK", "VMW", "PEP", "GLD", "IWM", "AAPL", "ADI", "ANET", "BA", "TEAM", "LOW", "CRM", "UNP", "SGEN", "V", "PANW", "MCD", "FDX", "TSLA", "CAT", "AMGN", "SMCI", "HD", "META", "GS", "MSFT", "MSTR", "DIA", "MDB", "QQQ", "LULU", "NFLX", "DE", "MA", "ULTA", "URI", "SPY", "NVDA", "HUM", "UNH", "ADBE", "LLY", "NOW", "COST", "LRCX", "AVGO", "CMG", "BKNG"]

prospectus_hook="https://discord.com/api/webhooks/1153827363222716536/Z2E911yplYRaql_KA1dKjJcppBiVbT-ieTOWLBFgDlB8z04qm-rewVLq_OEkGO0ToRpC"
QUARTERLY_REPORT="https://discord.com/api/webhooks/1153827571423776778/swa4jAn5Fd8tvlRp2s9EgxA_GQ54wFRr6amw6s58jJcUBBVUlOnu0BNWZgXhfM9VKMmW"
withdrawal_hook="https://discord.com/api/webhooks/1153827771693408266/srGGy-JtJFzWn4GavS71wUHbFLj1QVW-psDJ05vjFJScL_JVyN0wKrFkDX_NBKn-hu24"
amended_hook="https://discord.com/api/webhooks/1153827966523023480/4zW4KW4FFSTRuLaLZuISoAuNrw4LfNHIxYhueT-2m3eK03RuC90nQBe2dHqqSb1vyt0D"
sec_sale_hook="https://discord.com/api/webhooks/1153828117564112937/zd7cI36tYCCHSxF-Hx_4xk3AjREMUkx2dMQdFc2u0EfYkfoFvc6xtSMUlbPxerLgYvWQ"
annual_hook="https://discord.com/api/webhooks/1153828326922784870/HvkXGZFfDoOPP7m7bm84j4BHVwdzo26DmuhLOB0hoK4x4GW0XgyiF2Pwd-jwhJvtqKAL"
shelf_hook="https://discord.com/api/webhooks/1153828471387209788/BalAp7H6XemmHW_DTFTLmZWaSQa6oivt2m2sfpiP57TkLsAyhBoiEE9Pa9ZHRoa37a04"
correspondence_hook="https://discord.com/api/webhooks/1153828592388669450/GrMQgY3eLm2dQcXR7QUVGP470EGxMm6Pw0Itta5jiRI7XVOZUWSKFlWMPPZ4BlXUmS8U"
current_report_hook="https://discord.com/api/webhooks/1153828786937278485/zXg4WkZoSTGYfRBIjWrx6cMHzTUY-SMXtvZXIDssW6lzB5DOvfSwj6cakr7uzYfR8gBp"
notice_effectiveness_hook="https://discord.com/api/webhooks/1153828874220740729/O2IQqJM8LBrHickyIcsmXnUj_T3SgEQxYSK1BuOHDb9B0Ddd-lgv3ou826RLiS8zVdij"
securities_sale_hook="https://discord.com/api/webhooks/1153829124264177766/9ZUhRzrGgcKo0FMMWtNnX67iFnXwS9nzJc47WpAYXde2yUj5bciW2m5cAfx-BCN5sraY"
beneficial_change_hook="https://discord.com/api/webhooks/1153829306531860490/BE1l1jCqU_oA-c4fc_H1W47vGD6yF98XR9YuUtKAgmHw9Ef94WYPJYZ0HAWUiT3NeQDM"
sec_generated_letter_hook="https://discord.com/api/webhooks/1153829474039775342/R7-7Q3YNaiq6eZTV5WRdgB4wSu8QS7SZbdmh88RL4U16hgRsHjw0wASy7isBUpB7QFk1"
employee_offering_hook="https://discord.com/api/webhooks/1153829643976179712/labk1s6wqU0LaHIFjq8aeI8f7GBZFA1EjE3Ngx3lh8ihXeImdKjDEW1MK9fnGOsQ1pOT"
foreign_issuer_hook="https://discord.com/api/webhooks/1153833647913312286/CSYl_fd0Y3MEdQ95AqxIZMAx9ltJMr7lgacQenYpN4sx3W1LkgBUNsl-V1G5JWB8Nj5y"
NPORT="https://discord.com/api/webhooks/1156987205756129372/kwL6PSGHTaLViM___R1GzQACagRsND5VgNRJ1HGUJ5lZlBw7-T5nVQBiNS41ehRqFwTi"
REGISTRATION_OF_SECURITIES="https://discord.com/api/webhooks/1156992969325420606/Kj2sOa5IZB9Bhr2bYk9AvpNQyyfmaArD1KmA0XHsITum680LYVHawBDc-zsf-OaW-A0A"
UNDERTAKING="https://discord.com/api/webhooks/1157037541099315250/0kfXtN4_LaKNKv5aCsg50xUOlR2DKh3IGwFAx2ePzi5PF7Qrz_74Q7cS5vA64O2ZzeJA"
CERTIFIED_SHAREHOLDER="https://discord.com/api/webhooks/1157031228214616084/rfk51ToXW0Hy7nWhwK59qQhsZeli6w70wZFe_2pQmeZtU_1maptAaUN3hpficE_dWe7J"
SEC_STAFF="https://discord.com/api/webhooks/1157031998502752418/qamL1Dut43Wl5o1I6TYtzbPpr0xvQ6qv6Z5hDAxAUDF91CvRSW0V30r4Lco2QpRDfw7l"
SECURITIES_REGISTRATION="https://discord.com/api/webhooks/1157034123077107732/6TtVk3KsiDSniy75ag8imnnPLaargFYbF6ssmDwnDgvI_BzFZwzxwXEifrXLK63M_9YI"
thirteenF_amended="https://discord.com/api/webhooks/1157038087168336043/ACurXojshWty8DKo7LQrFyK65A-fvVRO39yGd7QCcN4R4SfmQJ9fOV-QcEw-encMYy_e"
TEN_K="https://discord.com/api/webhooks/1157037834578964660/PHO5oS6wG-404zcr-UK6fGb7-CAUH3Y4mAZROI9096n5VZJjxxBQE9FD2J4S-Gd52uPO"
thirteenf="https://discord.com/api/webhooks/1157038898069917876/BlQO1LdxFpTgcWc-zYi4BBoxdzHuuYNOu0ZCmZiWESlunnBXugOVFhIpZLChM6BMj5ZZ"
LATE_FILING="https://discord.com/api/webhooks/1157107631257829416/ESJSENWD79FJqjt5DtpNLd88f9cpeTW6mtxvaOmE1wL-3SR4OTtXkW-ZzlJMuxLG9YGw"
DEFINITIVE_MATERIALS="https://discord.com/api/webhooks/1157107879803883571/ShxdJwFNeczRnL-98RqWG5rVSL3wPAUfBbuud8umOHlVaD6mDba2zxKTLgPhNCM3hCKl"


class RSSMonitor:
    def __init__(self):
        self.latest_entry_id = None

    async def fetch_rss(self, rss_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(rss_url, headers=headers_sec) as resp:
                if resp.status != 200:
                    print(f"Failed to get data: {resp.status}")
                    return None
                return await resp.text()

    async def check_for_new_articles(self):
        rss_data = await self.fetch_rss()
        if not rss_data:
            return
        feed = feedparser.parse(rss_data)

        new_entry_id = feed.entries[0].id if feed.entries else None

        if new_entry_id != self.latest_entry_id:
            print("New article found!")
            # Perform actions for new article (e.g., posting it)
            self.latest_entry_id = new_entry_id


import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin
async def fetch_rss_feed_async(url, ticker):
    async with aiohttp.ClientSession(headers=headers_sec) as session:
        async with session.get(url) as response:
            text = await response.text()
            try:
                root = ET.fromstring(text.encode("ISO-8859-1"))


                # Define the namespace
                namespaces = {'atom': 'http://www.w3.org/2005/Atom'}

                # Loop through each entry in the feed
                for entry in root.findall('atom:entry', namespaces=namespaces):

                    # Find and print out each element you're interested in
                    title = entry.find('atom:content-type/atom:form-name', namespaces=namespaces)
                    link = entry.find('atom:link', namespaces=namespaces)
                    published = entry.find('atom:content-type/atom:filing-date', namespaces=namespaces)
                    updated = entry.find('atom:content-type/atom:updated', namespaces=namespaces)
                    size = entry.find('atom:content-type/atom:size', namespaces=namespaces)
                    filing_href = entry.find('atom:content-type/atom:filing-href', namespaces=namespaces)
                    # Extract and print individual elements
                    # Initialize an empty dictionary to hold the extracted values
                    data_dict = {}

                    # Loop through each element in the XML fragment
                    for elem in root.findall('.//', namespaces=namespaces):
                        tag = elem.tag.split('}')[-1]  # Remove the namespace part
                        text = elem.text  # Get the text content
                        data_dict[tag] = text  # Add to dictionary
                        data_dict['ticker'] = ticker

                    filtered_data_dict = {k: v for k, v in data_dict.items() if v is not None and v.strip()}
                    # Using pop()
                    filtered_data_dict.pop('id', None)
                    filtered_data_dict.pop('summary', None)
                    df = pd.DataFrame(filtered_data_dict, index=[ticker])
                    return df
            except ET.ParseError:
                print(f"Error: Not well formed for {ticker}")

async def extract_links_from_filing(url):
    async with aiohttp.ClientSession(headers=headers_sec) as session:
        if url is not None:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                xml_and_pdf_links = []
                
                for link in soup.find_all('a'):
                    link_url = urljoin(url, link.get('href'))
                    if link_url.endswith('.xml'):
                        xml_and_pdf_links.append(link_url)
                
                return xml_and_pdf_links
# Example usage

import pandas as pd
async def main():
    
    df = pd.read_csv('ciks.csv')
    for i in real_subs:

        cik = get_cik_by_ticker(df, i)
        monitor = RSSMonitor()
        data_dict = await fetch_rss_feed_async(f'https://data.sec.gov/rss?cik={cik}&count=1', i)
        if data_dict is not None:
            try:
                for i,row in data_dict.iterrows():
                    ticker = row['ticker']
                    title = row['title']
                    subtitle = row['subtitle']
                    email = row['email']
                    name = row['name']
                    updated = row['updated']
                    street1 = row['street1']
                    city = row['city']
                    stateOrCountry = row['stateOrCountry']
                    zipCode = row['zipCode']
                    stateOrCountryDescription = row['stateOrCountryDescription']
  

                    assigned_sic_href = row['assigned-sic-href'] if 'assigned-sic-href' in row else None
                    confirmed_name = row['confirmed-name']
                    employer_identification_number = row['employer-identification-number'] if 'employer-identification-number' in row else None
                    fiscal_year_end = row['fiscal-year-end'] if 'fiscal-year-end' in row else None
                    office = row['office'] if 'office' in row else None
                    state_location = row['state-location']
                    state_location_href = row['state-location-href']
                    state_of_incorporation = row['state-of-incorporation'] if 'state-of-incorporation' in row else None
                    acceptance_date_time = row['acceptance-date-time']
                    accession_number = row['accession-number']


                    filing_date = row['filing-date']
                    if filing_date == today_str:
                        filing_href = row['filing-href']

                        form_name = row['form-name']
                        size = row['size']

                        print(title)

                        if title == 'Securities to be offered to employees in employee benefit plans':
                            await send_sec_embed(employee_offering_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                            print(filing_href)

                            links = await extract_links_from_filing(filing_href)
                            print(links)
                        elif 'Quarterly Report' in title:
                            await send_sec_embed(QUARTERLY_REPORT, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif 'changes in beneficial ownership' in title: #
                            await send_sec_embed(beneficial_change_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'Annual Report to Security Holders':#
                            await send_sec_embed(annual_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'Current report':
                            print(filing_href)
                            await send_sec_embed(current_report_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href) #


                        elif title == 'Current report - amended':
                            await send_sec_embed(current_report_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href) #
                        elif title == 'Prospectus [Rule 424(b)(2)]':#
                            await send_sec_embed(prospectus_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'Prospectus [Rule 424(b)(3)]':#
                            await send_sec_embed(prospectus_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == 'Quarterly report [Sections 13 or 15(d)]':
                            await send_sec_embed(QUARTERLY_REPORT, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)#

                        elif title == 'Report of proposed sale of securities':
                            await send_sec_embed(sec_sale_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif 'Registration of securities [Section 12(b)]' in title:
                            await send_sec_embed(REGISTRATION_OF_SECURITIES, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == 'Notice of Effectiveness':
                            await send_sec_embed(notice_effectiveness_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href )

                        elif title == 'Certified Shareholder Report':
                            await send_sec_embed(CERTIFIED_SHAREHOLDER, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'SEC Staff Letter':
                            await send_sec_embed(SEC_STAFF, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == 'Post-effective amendment [Rule 485(a)]': #
                            await send_sec_embed(amended_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'Report of foreign issuer [Rules 13a-16 and 15d-16]':
                            await send_sec_embed(foreign_issuer_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)#


                        elif title == 'Appointment of Agent for Service of Process and Undertaking':
                            await send_sec_embed(UNDERTAKING, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == '10-K':
                            await send_sec_embed(TEN_K, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        elif title == 'General statement of acquisition of beneficial ownership - amended':#
                            await send_sec_embed(thirteenF_amended, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)



                        elif title == 'General statement of acquisition of beneficial ownership':#
                            await send_sec_embed(thirteenF_amended, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)



                        elif title == 'Quarterly report filed by institutional managers, Holdings - amended':
                            await send_sec_embed(thirteenF_amended, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == 'Quarterly report filed by institutional managers, Holdings':
                            await send_sec_embed(thirteenf, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title == 'Notification of inability to timely file Form 10-K 405, 10-K, 10-KSB 405, 10-KSB, 10-KT, or 10-KT405':
                            await send_sec_embed(LATE_FILING, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)

                        
                        elif title == 'Definitive materials':
                            await send_sec_embed(DEFINITIVE_MATERIALS, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)


                        elif title =='Automatic shelf registration statement of securities of well-known seasoned issuers':
                            await send_sec_embed(shelf_hook, title,ticker,subtitle,name,updated,filing_date,acceptance_date_time,filing_href,form_name,size,confirmed_name,employer_identification_number,fiscal_year_end,office,state_of_incorporation,state_location,state_location_href,email,street1,city,stateOrCountry,stateOrCountryDescription,zipCode,assigned_sic_href)                

            except Exception as e:
                print(f"Error: {e}")









if __name__ == "__main__":
    asyncio.run(main())


