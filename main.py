from curl_cffi import requests
from lxml import etree, html
from log import Log
import config
import json
import pandas as pd
import os




class Discovery:
    def __init__(self):
        self.log = Log().get_logger(f"{config.NAME_CRAWLER}-Discovery.log")
        self._records = set()

    def make_requests(
            self,
            url,
            headers={},
            timeout=20,
            proxies={},
            params={},
            impersonate="chrome",
        ):

        attempt = 0
        while attempt < config.MAX_RETRIES:
            try:
                response = requests.get(
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    impersonate=impersonate
                )
                if response.status_code == 200:
                    return response
                else:
                    raise(f"Error - status code: {response.status_code}")

            except Exception as e:
                self.log.error(f"the request has failed - {e}")
                attempt +=1

        self.log.warning("the target of number of attempt has reachead")

    def get_pages(self):
        try:
            response = self.make_requests("https://www.fravega.com/sitemap/index.xml")

            if response:
                
                tree = etree.fromstring(response.content)
                urls = tree.xpath(
                    "//sm:loc/text()",
                    namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
                )
                
                pages = []
                for url in urls:
                    if config.PAGES_PATTERN.fullmatch(url):
                        pages.append(url)
                print(pages)
                return pages

        except Exception as e:
            self.log.error(f"there was an error on GET_PAGES - Error:{e}")
            return []

    def get_products(self,pages):
        try:
            for products in pages:
                response = self.make_requests(products)

                if response:
                    
                    tree = etree.fromstring(response.content)
                    urls = tree.xpath(
                        "//sm:loc/text()",
                        namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
                    )
                    
                
                    for url in urls:
                        if config.PRODUCT_PATTERN.fullmatch(url):
                            self._records.add(url)
                    print(len(self._records))
                    

        except Exception as e:
            self.log.error(f"there was an error on GET_PRODUCTS - Error {e}")

    def run(self):
        try:
            self.log.info("start Discovery")
            pages= self.get_pages()
            self.get_products(pages)
            self.log.info("End Discovery")

        except Exception as e:
            self.log.error(f"there was an error on Discovery-RUN - Error:{e}")




class PDP:
    def __init__(self):
        self.log = Log().get_logger(f"{config.NAME_CRAWLER}-PDP.log")
        
    def make_requests(
            self,
            url=None,
            headers=None,
            timeout=None,
            proxies=None,
            params=None,
            impersonate=None,
        ):
        attempt = 0
        while attempt < config.MAX_RETRIES:
            try:
                response = requests.get(
                    url=f"{config.BASE_URL}",
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    impersonate=impersonate
                )
                if response.status_code == 200:
                    return response
                else:
                    raise(f"Error - status code: {response.status_code}")

            except Exception as e:
                self.log.error("the request has failed - {e}")
                attempt +=1
        self.log.error("the target of number of attempt has reachead")

    def product_data():
        pass

    def parser_data():
        pass

    def get_data(self):
        try: 
            response = self.make_requests("https://www.fravega.com/sitemap/index.xml")

            
            if response:
                
                tree = etree.fromstring(response.content)
                urls = tree.xpath(
                    "//sm:loc/text()",
                    namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
                )
                
                # pages = []
                # for url in urls:
                #     if config.PAGES_PATTERN.fullmatch(url):
                #         pages.append(url)
                # print(pages)
                # return pages

            
        except Exception as e:
            self.log.error(f"there was an error on GET_DATA - Error: {e}")
        
    def save_data():
        #while
        pass

    def run(self):
        try:
            self.log.info("start PDP")
            self.get_data()

            self.log.info("End PDP")

        except Exception as e:
            self.log.error(f"there was an error on Discovery-RUN - Error:{e}")




if __name__ == "__main__":
   
   products = Discovery().run()
   PDP().run(products)