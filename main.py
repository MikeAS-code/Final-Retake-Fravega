from curl_cffi import requests
from lxml import etree
import config


class Discovery:
    def __init__(self):
        self._records = set()

    def get_pages(self):
        res = requests.get(
            "https://www.fravega.com/sitemap/index.xml",
            headers=config.HEADERS,
            timeout=config.TIME_OUT,
        )

        tree = etree.fromstring(res.content)

        urls = tree.xpath(
            "//sm:loc/text()",
            namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
        )

        for url in urls:
            if config.DISCOVER_PATERN.fullmatch(url):
                self.url_products(url)

    def url_products(self, url):
        res = requests.get(url, headers=config.HEADERS, timeout=config.TIME_OUT)
        tree = etree.fromstring(res.content)

        urls = tree.xpath(
            "//sm:loc/text()",
            namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"},
        )

        for url in urls:
            if config.PRODUCT_PATTERN.fullmatch(url):
                self._records.add(url)

    def run(self):
        self.get_pages()

        return self._records


class PDP:
    def __init__(self):
        pass

    def product_data(self, products):
        for product in products:
            # https://www.fravega.com/p/perfume-risala-surur-edp-100-ml-para-unisex-23063754/

            sku = product.split("-")[-1].replace("/", "")

            json_data = {
                "operationName": "getProductDetails_Shopping",
                "variables": {
                    "isGeoLocated": True,
                    "sku": sku,
                    "postalCode": "C1406",
                    "zoneIds": [],
                },
                "query": 'query getProductDetails_Shopping($sku: NonEmptyString!, $zoneIds: [NonEmptyString!], $postalCode: PostalId, $isGeoLocated: Boolean = false) {\n  sku(code: $sku) {\n    code\n    item {\n      sellerConditions\n      id\n      slug\n      active\n      type\n      title\n      katalogCategoryId\n      gtin {\n        __typename\n        ... on EAN {\n          number\n          __typename\n        }\n      }\n      brand {\n        id\n        name\n        slug\n        image\n        __typename\n      }\n      seoDescription\n      images\n      videos\n      specifications(tagged: ["detailed"]) {\n        id\n        name\n        slug\n        group {\n          id\n          name\n          type\n          __typename\n        }\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      descriptions {\n        id\n        name\n        slug\n        group {\n          id\n          __typename\n        }\n        type\n        valueType\n        value\n        __typename\n      }\n      attributes {\n        id\n        name\n        slug\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seller {\n      id\n      commercialName\n      slug\n      __typename\n    }\n    marketplace\n    images\n    enabledChannels\n    stock(postalCode: null, zoneIds: $zoneIds) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    geoAvailability: stock(postalCode: $postalCode, zoneIds: $zoneIds) @include(if: $isGeoLocated) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    categorization {\n      id\n      name\n      slug\n      __typename\n    }\n    pricing(channel: "fravega-ecommerce") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    netPricing: pricing(channel: "net-price") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    cockades(tag: "detail") {\n      image\n      position\n      __typename\n    }\n    __typename\n  }\n}\n',
            }

            res = requests.post('https://www.fravega.com/api/v2', headers=config.HEADERS_PDP, json=json_data)
            data = res.json()

             
    def run(self, products):
        self.product_data(products)


if __name__ == "__main__":
    products = Discovery().run()
    
    PDP().run(products)
