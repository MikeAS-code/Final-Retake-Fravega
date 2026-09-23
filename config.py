from dotenv import load_dotenv
import os
import re

load_dotenv('.env')

NAME_CRAWLER = "Fravega-Crawler"

BASE_URL = "https://www.fravega.com/"

MAX_RETRIES = 3

PROXY={
    'http':'PROXY',
    'https:':'PROXY'
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'es-419,es-US;q=0.9,es;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://www.fravega.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.fravega.com/',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    'x-browser-channel': 'stable',
    'x-browser-copyright': 'Copyright 2026 Google LLC. All Rights Reserved.',
    'x-browser-validation': 'Nvr5k+iFMPN1OOuTAQHMfJ+Q6a8=',
    'x-browser-year': '2026',
    'x-client-data': 'CKmdygEIkqHLAQiFoM0BCLDilDAIlOeUMA==',
    # 'cookie': '__Secure-3PAPISID=KhZNHW1phkN6MRPd/AFToziGlQpyJy-6dN; __Secure-3PSID=g.a000CwnDOvICyw7_aIGizqwugMhNLCtRWIw8hVL69sKaY74xARNPr096_XO1JRoqQdW6-j4iiQACgYKAa0SARISFQHGX2MiAGd_2O70NG_LlPpBlMa5WhoVAUF8yKp4EiRCaGsg6lVT8Fv5tFaS0076; __Secure-3PSIDTS=sidts-CjIBXMw41UavdIAcLN67rdvDS3gxlER3wqQ8bss2l0xG3BBWHF5ZCf4e46hij3BfuuPjQxAA; NID=CvECCAESowIBOxGDSCLeuE7CU_yMUiO6HveaKhpOrbWMMih-7_2Z8uvEq2YKf7dLwIRn44pQiPqStPvg3MWbqDI5pq4VhnC_wU6T-2qNPUq-r3S3YTtVMRjgfd8BmLmVLrdWUCQB8Hq-2sVj69QHawYEQRGAxQbSr2-hsscRUJKEf71oD_mDIm4-ULzJ-NRGYDs9dLdDQD5tV-x_2RbtZjnonhzO9GR9XeZUpKuNslMn6-ofPvgXbIRcbCoFbDFjA0fRck8j1c3_DEnf7YYun4nkDsfVfWcnZ77Pqw8WlBDxa_vzd3VH0K3JBbIJF8hZx2yJ_8fe8aQNvCnskNjhEUYewZIDFKibdYZdW_BGzzb0nsyrIa9lX2Lzo8q6n3nG49ANoV1gYFU_j3UoATJFAdKsB88cC4RjpfSZciMd9Ph9t_gU6a_i9gXgAdIRUu1ZUT8RG9oIeJS71uCIFEAn-ByFNgn7-2Pw3p_1UuxzHGTM9z8I; __Secure-3PSIDCC=AKEyXzXLVL3jz4QO2kyw9xv6UMEV_izI-cGlw1bhh3nXH2PyfZS0KpAflSFHQsCbpUfj5vgw1A',
}


PAGES_PATTERN = re.compile("https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$")

PRODUCT_PATTERN = re.compile("https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$")
