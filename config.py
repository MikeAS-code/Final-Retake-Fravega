from dotenv import load_dotenv

load_dotenv(".env")

import os
import re

BASE_URL = "https://www.fravega.com"

NAMESPACES = {
    "sm" : "http://www.sitemaps.org/schemas/sitemap/0.9"
}

REGEX_PG = re.compile("https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$")

REGEX_PROD = re.compile("https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$")


PROXY_NAME = os.environ["PROXY_NAME"]
PROXY_PASSWORD = os.environ["PROXY_PASSWORD"]
PROXY_HOST = os.environ["PROXY_HOST"]
PROXY_PORT = os.environ["PROXY_PORT"]

TIMEOUT = os.environ["TIMEOUT"]

MAX_RETRIES = int(os.environ["MAX_RETRIES"])

PROXY = f"http://{PROXY_NAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"

PROXIES = {
    "http" : PROXY,
    "https" : PROXY
}


COOKIES = {
    'ab-algolia': 'Algolia',
    'AWSALBCORS': '0SIFFcUbiqWOc4++ysr4mZ2o54aLh0LMcZJJ+fPXd+vSTgg8SSxL68rmLS8ODc0MfpPgoZazjVYmUUTYPIWOUyxXi01f39DssbmikwnFW+OTnLtwk0RtxbS4psO4',
    'AWSALB': 'Axus3lcIytvsHVlUPPQJ3BrOdshpQcfGWynITsXWTEKRqzrJjBCCYfZeS3BrUGxb7Kb6brI00E93Vcrrm+eQUdqCtB5csl6DKW5ojHWR1b9PKsoBSiWTOktynkWc',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.fravega.com',
    'priority': 'u=1, i',
    'referer': 'https://www.fravega.com/p/bloques-magneticos-juego-imantado-para-armar-creatividad-64-piezas-23074892/',
    'sec-ch-ua': '"Brave";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    # 'cookie': 'ab-algolia=Algolia; AWSALBCORS=0SIFFcUbiqWOc4++ysr4mZ2o54aLh0LMcZJJ+fPXd+vSTgg8SSxL68rmLS8ODc0MfpPgoZazjVYmUUTYPIWOUyxXi01f39DssbmikwnFW+OTnLtwk0RtxbS4psO4; AWSALB=Axus3lcIytvsHVlUPPQJ3BrOdshpQcfGWynITsXWTEKRqzrJjBCCYfZeS3BrUGxb7Kb6brI00E93Vcrrm+eQUdqCtB5csl6DKW5ojHWR1b9PKsoBSiWTOktynkWc',
}

JSON_DATA = {
    'operationName': 'getProductDetails_Shopping',
    'variables': {
        'isGeoLocated': True,
        'sku': '23074892',
        'postalCode': 'C1406',
        'zoneIds': [],
    },
    'query': 'query getProductDetails_Shopping($sku: NonEmptyString!, $zoneIds: [NonEmptyString!], $postalCode: PostalId, $isGeoLocated: Boolean = false) {\n  sku(code: $sku) {\n    code\n    item {\n      sellerConditions\n      id\n      slug\n      active\n      type\n      title\n      katalogCategoryId\n      gtin {\n        __typename\n        ... on EAN {\n          number\n          __typename\n        }\n      }\n      brand {\n        id\n        name\n        slug\n        image\n        __typename\n      }\n      seoDescription\n      images\n      videos\n      specifications(tagged: ["detailed"]) {\n        id\n        name\n        slug\n        group {\n          id\n          name\n          type\n          __typename\n        }\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      descriptions {\n        id\n        name\n        slug\n        group {\n          id\n          __typename\n        }\n        type\n        valueType\n        value\n        __typename\n      }\n      attributes {\n        id\n        name\n        slug\n        type\n        valueType\n        value\n        measureUnit {\n          name\n          symbol\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seller {\n      id\n      commercialName\n      slug\n      __typename\n    }\n    marketplace\n    images\n    enabledChannels\n    stock(postalCode: null, zoneIds: $zoneIds) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    geoAvailability: stock(postalCode: $postalCode, zoneIds: $zoneIds) @include(if: $isGeoLocated) {\n      labels\n      availability\n      pickup {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      homeDelivery {\n        availability\n        labels\n        locations {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    categorization {\n      id\n      name\n      slug\n      __typename\n    }\n    pricing(channel: "fravega-ecommerce") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    netPricing: pricing(channel: "net-price") {\n      channel\n      listPrice\n      salePrice\n      discount\n      __typename\n    }\n    cockades(tag: "detail") {\n      image\n      position\n      __typename\n    }\n    __typename\n  }\n}\n',
}

API = "https://www.fravega.com/api/v2"