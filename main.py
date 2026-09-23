import pandas as pd
from curl_cffi import requests
from lxml import html, etree
import json

import config
from log import Log


class Discovery:

    def __init__(self):
        self.logger=Log().get_logger(f'{config.CRAWLER_NAME}-discovery.log')
        self._records=set()

    def make_requests(self, url, headers={}, params={}, proxies={}, impersonate='chrome', verify=False, timeout=30):

        attempt=0

        while attempt< config.MAX_RETRIES:

            try:

                response=requests.get(url=url, headers=headers,params=params,proxies=proxies, impersonate=impersonate, verify=verify, timeout=timeout)
                if response and response.status_code==200:
                    return response
            except Exception as e:
                self.logger.error(f'error en make_requests {e}')
                attempt+=1
        
        

    def get_products_url(self, page):
        try:
            response=requests.get(page, impersonate='chrome', verify=False,timeout=config.TIMEOUT,proxies=config.PROXY)

            if response:

                tree=etree.fromstring(response.content)

                urls=tree.xpath('//sm:loc/text()', namespaces={'sm','http://www.sitemaps.org/schemas/sitemap/0.9'})

                for url in urls:
                    if config.PRODUCT_PATTERN.fullmatch(url):
                        self._records(url)


        except Exception as e:
            self.logger.error('error en get_products_url {e}')

    def get_pages(self):

        try:
            response=requests.get(f'{config.BASE_URL}/sitemap/index.xml', impersonate='chrome', verify=False,timeout=config.TIMEOUT,proxies=config.PROXY)
            print('Esto es response',response.text)

            if response and response.status_code==200:
                
                tree=etree.fromstring(response.content) 

                urls=tree.xpath('//sm:loc/text()', namespaces={'sm','http://www.sitemaps.org/schemas/sitemap/0.9'})

                pages=[]

                for url in urls:
                    if config.PAGE_PATTERN.fullmatch(url):
                        print(url)
                        pages.append(url)
                print('Esto es pages',pages)
                return pages

        except Exception as e:
            self.logger.error(f'error en get_pages {e}')
            return []


    def run(self):

        try:
            self.logger.info('Start Discovery')

            pages=self.get_pages()

            print(pages)

            total=len(pages)

            for idx, page in enumerate(pages, start=1):
                self.logger.info('Page {idx}/{total}')
                self.get_products_url(page)

            self.logger.info('End Discovery')

        except Exception as e:
            self.logger.error(f'error en Discovery run {e}')

class PDP:
    def __init__(self):
        self.logger=Log().get_logger(f'{config.CRAWLER_NAME}-PDP.log')

    def procesed_data(self, data):
        try:
            file_path= 'output/data.jsonl'

            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(json.dumps(data) + '\n')

        except Exception as e:
            self.logger.error(f'error en procesed_data {e}')

    def parser_data(self,data, product):

        try:

            url=(product,'')

            code=data.get('code','')

            id=data.get('id','')

            title=data.get('title','')

            slug=''

            description=''

            brand=''

            image_main=''

            images=[]

            price=''

            sale_price=''

            discount_price=''

            discount_percentage=''

            availability=''

            gtin=''

            specifications=[]

            store_name=''

            seller_url=''



            data={
                "url": (url,''),
                "code": '',
                "id": '',
                "title": '',
                "slug": null,
                "description": null,
                "brand": null,
                "image_main": null,
                "images": null,
                "price": null,
                "sale_price": null,
                "discount_price": null,
                "discount_percentage": null,
                "availability": null,
                "gtin": null,
                "specifications": [
                    {
                        "name": null,
                        "value": null
                    }
                ],
                "store_name": "fravega",
                "seller_url": "https://www.fravega.com/"
            }

            self.procesed_data(data)

        except Exception as e:
            self.logger.info(f'error en parser_data {e}')


    def get_data(self, product):
        try:
            response=requests.get(product, impersonate='chrome', verify=False, proxies=config.PROXY, timeout=config.TIMEOUT)

            if response:
                tree=html.fromstring(response.text)

                self.parser_data(tree, product)

                print(response)

        except Exception as e:
            self.logger.error(f'error en PDP run {e}')

    def save_information(self):
        try:
            jsonl_path='output/data.jsonl'
            json_path='output/data_saved.json'

            df=pd.read_json(jsonl_path, lines=True)

            df.to_json(json_path, orient='records', indent=4)
        except Exception as e:
            self.logger.error(f'error en save_information {e}')
        

    def run(self, products):
        try:
            self.logger.info('Start PDP')

            for idx, product in enumerate (products, start=1):
                self.get_data(product)

            self.save_information()

        except Exception as e:
            self.logger.error(f'error en PDP run {e}')

if __name__=='__main__':

    #products=Discovery().run()

    products=[
        'https://www.fravega.com/p/perfume-maison-francis-kurkdjian-baccarat-rouge-540-70-ml-23063901/'

        ]
    
    PDP().run(products)