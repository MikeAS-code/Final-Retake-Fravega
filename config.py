from dotenv import load_dotenv
import os
import re

load_dotenv('.env')

BASE_URL='https://www.fravega.com'

CRAWLER_NAME='fravega'

PAGE_PATTERN=re.compile('^https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$')

PRODUCT_PATTERN=re.compile('^https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$')

PROXY={
    'http':os.environ.get('PROXY'),
    'https':os.environ.get('PROXY')
}



MAX_RETRIES=3

TIMEOUT=30