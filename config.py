from dotenv import load_dotenv
import os
import re

load_dotenv('.env')


PROXY={
    'http':os.environ.get('PROXY'),
    'https:':os.environ.get('PROXY')
}

BASE_URL='https://www.fravega.com'

CRAWLER_NAME='fravega'

MAX_RETRIES=3


PAGES_PATTERN=re.compile("^https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$")

PRODUCT_PATTERN=re.compile("^https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$")


HEADERS_PDP = {
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.fravega.com',
    'priority': 'u=1, i',
    'referer': 'https://www.fravega.com/p/perfume-rasasi-ibreez-para-hombre-eau-de-parfum-100-ml-23063759/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',    
}




