import json
from lxml import html, etree
import pandas as pd
from curl_cffi import requests
import time
import random
import os

import config
from log import Log


class Discovery:

    def __init__(self):
        self.log = Log().get_logger(f"{config.CRAWLER_NAME}-discovery.log")
        self._records = set()

    def make_requests(
        self,
        url,
        headers={},
        timeout=30,
        proxies={},
        params={},
        impersonate="chrome124",
        verify=False,
    ):

        attempt = 0
        while attempt < config.MAX_RETRIES:
            try:
                response = requests.get(
                    url=url,
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    impersonate=impersonate,
                    proxies=proxies,
                    verify=verify,
                )
                if response and response.status_code == 200:
                    return response
                else:
                    raise (f"Error! - The status code is {response.status_code}")
            except Exception as e:
                self.log.error(f"The requests has failed - Error:{e} - Retrying")
                attempt += 1

        self.log.error("The target number of attempts was reached")
        return None

    def get_pages(self):
        try:
            response = self.make_requests(
                f"{config.BASE_URL}/sitemap/index.xml", proxies=config.PROXY
            )

            if response:

                tree = etree.fromstring(response.content)
                # Sitemap XML normalmente utiliza namespace
                urls = tree.xpath(
                    "//sm:loc/text()",
                    namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
                )

                pages = []

                for url in urls:
                    if config.PAGES_PATTERN.fullmatch(url):
                        pages.append(url)

                return pages

        except Exception as e:
            self.log.error(f"There was an error on get_pages - Error: {e}")
            return []

    def get_products(self, page):
        try:
            response = self.make_requests(page, proxies=config.PROXY)

            if response:

                tree = etree.fromstring(response.content)
                # Sitemap XML normalmente utiliza namespace
                urls = tree.xpath(
                    "//sm:loc/text()",
                    namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
                )

                for url in urls:
                    if config.PRODUCT_PATTERN.fullmatch(url):
                        self._records.add(url)

        except Exception as e:
            self.log.error(f"There was an error on get_products - Error: {e}")

    def run(self):
        try:
            self.log.info(f"Start Discovery")

            pages = self.get_pages()

            if not pages:
                self.log.critical("There are not pages to search")
                return

            total = len(pages)
            self.log.info(f"Found {total} pages")
            for idx, page in enumerate(pages):
                self.log.info(f"Page #{idx}/{total}")

                self.get_products(page)

            if not self._records:
                self.log.critical("URLs products not found")
                return []

            self.log.info("End Discovery")
            return list(self._records)
        except Exception as e:
            self.log.error(f"There was an error on run - Error:{e}")


class PDP:

    def __init__(self):
        self.log = Log().get_logger(f"{config.CRAWLER_NAME}-pdp.log")

    def make_requests(
        self,
        url,
        headers={},
        timeout=30,
        proxies={},
        params={},
        json={},
        impersonate="chrome124",
        verify=False,
    ):

        attempt = 0
        while attempt < config.MAX_RETRIES:
            try:
                response = requests.post(
                    url=url,
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    impersonate=impersonate,
                    proxies=proxies,
                    verify=verify,
                    json=json,
                )
                if response and response.status_code == 200:
                    return response
                else:
                    raise Exception(
                        f"Error! - The status code is {response.status_code}"
                    )
            except Exception as e:
                self.log.error(f"The requests has failed - Error:{e} - Retrying")
                time.sleep(random.randint(3, 6))
                attempt += 1

        self.log.error("The target number of attempts was reached")
        return None

    def proccesed_data(self, data):
        try:
            file_path = "output/data.jsonl"

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "a", encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False) + "\n")

        except Exception as e:
            self.log.error(f"There was an error on proccesed_data - Error:{e}")

    def parser_data(self, data, product_url):

        try:
        
            url = product_url

            code = data.get("code", None)

            data_item=data['item']
            try:
                id = data_item.get("id", None)
            except:
                id=None

            try:
                slug=data_item.get('slug',None)
            except:
                slug=None

            try:
                title=data_item.get('title',None)

            except:
                title=None

            try:
                gtin=data_item.get('gtin',{}).get("number",None)

            except:
                gtin=None

            
            try:
                brand=data_item.get('brand',{}).get('name')

            except:
                brand=None


            
            try:
                description=data_item.get('seoDescription',None)

            except:
                description=None
            
            try:
                images_raw=data_item.get('images',[])
            except:
                images_raw=None

            try:



                specifications_raw=data_item.get('specifications',[])

                if not specifications_raw:
                    specifications=None
                else:
                    specifications=[]
                    for spec in specifications_raw:
                        specification={
                            "name":spec.get("name",None),
                            "value":spec.get("value",None)
                        }

                        specifications.append(specification)

            except:
                specifications=None

            if not images_raw:
                images=None

            else:
                images=[]
                for img in images_raw:
                    image=f'https://images.fravega.com/f300/{img}.webp'
                    images.append(image)

            if images:
                image_main=images[0]
            else:
                image_main=None

            stock_raw=data.get('stock',{}).get('availability',None)

            if stock_raw != None:
                if stock_raw:
                    stock='in_stock'
                else:
                    stock='out_of_stock'
            else:
                stock=None

            pricing=data.get('pricing',[])

            price=None
            sale_price=None

            if pricing:
                price = pricing[0].get("listPrice", None)
                sale_price = pricing[0].get("salePrice", None)

            if sale_price:
                discount_price=float(price-sale_price)
                percentage=int((sale_price*100)/price)
                discount_percentage=100-percentage

            else:
                discount_price=None
                discount_percentage=None

            data = {
                "url": url,
                "code": code,
                "id": id,
                "title": title,
                "slug":slug,
                "description":description,
                "brand": brand,
                "image_main": image_main,
                "images": images,
                "price": price,
                "sale_price": sale_price,
                "discount_price": discount_price,
                "discount_percentage": discount_percentage,
                "availability": stock,
                "gtin": gtin,
                "specifications": specifications,
                "store_name": "fravega",
                "seller_url": "https://www.fravega.com/",
            }

            self.proccesed_data(data)

                        
        except Exception as e:
            self.log.error(f'There was an error on parser_data - Error: {e}')

    def get_data(self, product):
        try:

            sku = product.split("-")[-1].replace("/", "").strip()

            json_data = {
                "operationName": "getProductDetails_Shopping",
                "variables": {
                    "isGeoLocated": False,
                    "sku": sku,
                    "postalCode": "C1406",
                    "zoneIds": [],
                },
                "query": 'query getProductDetails_Shopping($sku: NonEmptyString!, $zoneIds: [NonEmptyString!], $postalCode: PostalId, $isGeoLocated: Boolean = false) {\n  sku(code: $sku) {\n    code\n    item {\n      sellerConditions\n      id\n      slug\n      active\n      type\n      title\n      katalogCategoryId\n      gtin {\n        __typename\n        ... on EAN {\n          number\n          __typename\n        }\n      }\n      brand {\n        id\n        name\n        slug\n        image\n        __typename\n      }\n      seoDescription\n      images\n      videos\n      specifications(tagged: ["detailed"]) {\n        id\n        name\n        slug\n        group {\n          id\n          name\n          type\n          __typename\n        }\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      descriptions {\n        id\n        name\n        slug\n        group {\n          id\n          __typename\n        }\n        type\n        valueType\n        value\n        __typename\n      }\n      attributes {\n        id\n        name\n        slug\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seller {\n      id\n      commercialName\n      slug\n      __typename\n    }\n    marketplace\n    images\n    enabledChannels\n    stock(postalCode: None, zoneIds: $zoneIds) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    geoAvailability: stock(postalCode: $postalCode, zoneIds: $zoneIds) @include(if: $isGeoLocated) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    categorization {\n      id\n      name\n      slug\n      __typename\n    }\n    pricing(channel: "fravega-ecommerce") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    netPricing: pricing(channel: "net-price") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    cockades(tag: "detail") {\n      image\n      position\n      __typename\n    }\n    __typename\n  }\n}\n',
            }

            response = self.make_requests(
                f"{config.BASE_URL}/api/v2",
                headers=config.HEADERS_PDP,
                proxies=config.PROXY,
                json=json_data,
            )

            if response:
                data_raw = response.json()

                data=data_raw.get('data',{}).get('sku',{})

                self.parser_data(data, product)
            else:
                self.log.error(f"Product : {product} not found")

        except Exception as e:
            self.log.error(f"There was an error on get_data - Error: {e}")

    def save_information(self):
        try:

            jsonl_path = "output/data.jsonl"
            json_path = "output/data_saved.json"

            df = pd.read_json(jsonl_path, lines=True)

            if df.empty:
                self._log.warning("There is no information to save.")
                return

            df.to_json(json_path, orient="records", force_ascii=False, indent=4)

            self.log.info("Information saved successfully")

        except Exception as e:
            self.log.error(f"There was an error on save_information - Error:{e}")

    def run(self, products):

        self.log.info("Start PDP")

        if not products:
            self.log.critical("There are not urls products to get info")

        try:
            for idx, product in enumerate(products, 1):
                self.log.info(f"Get data from product {idx}/{len(products)}")
                self.get_data(product)

            self.save_information()

        except Exception as e:
            self.log.error(f"There was an error on run - Error: {e}")

        self.log.info("End PDP")


if __name__ == "__main__":

    products = Discovery().run()

    PDP().run(products)
