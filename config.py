from dotenv import load_dotenv
import os
import re

load_dotenv(".env")


BASE_URL= "https://www.fravega.com/"


HEADERS= {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.1034203465.1790182740; _gcl_gs=2.1.k1$i1790182738$u61301243; ab-algolia=Algolia; _twpid=tw.1790182741001.125144287583586680; _gcl_aw=GCL.1790182742.EAIaIQobChMImsfsqZaFlwMVn1JIAB3lXjKKEAAYAyAAEgK_4fD_BwE; _gcl_dc=GCL.1790182742.EAIaIQobChMImsfsqZaFlwMVn1JIAB3lXjKKEAAYAyAAEgK_4fD_BwE; _ga=GA1.1.372318314.1790182742; quanticId=216a2ea7-127d-4774-b3ef-af592f31d8ab; datajazztrackingsession=a08e8625-0197-426a-88a2-4ed3d0b06a00; _fbp=fb.1.1790182742501.400822304759102915; _tt_enable_cookie=1; _ttp=01M37K9PKYMM86QY8FET7NNX9R_.tt.1.1790182742654; _hjSession_242925=eyJpZCI6IjcxNWU3OWFmLTViMDItNDJmMC1iM2Q2LWY4MTIzMTg5MWU0YSIsImMiOjE3OTAxODI3NzkyNTYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=; _hjSessionUser_242925=eyJpZCI6ImEwMzA1ZGFkLTYzNmItNTViNi1iZTMxLWQxYjg2MDY1ZGM1MCIsImNyZWF0ZWQiOjE3OTAxODI3NzkyNTQsImV4aXN0aW5nIjp0cnVlfQ==; AWSALBCORS=/MCrTWcpzFQfpPdN9grcbfDHjs896OS8NtEbopiA3h64NWBUV8JtFq7Tl0xyocWXr52GZywKQhxciCpHMuorphHzed+m9JpimHr/LBwh/BHChcyHH8I02/1f/KmE; wcsid=H8B4IkqSdmuwvUKm1A89U0SoBUAa6k0r; hblid=MXXBvgoAwTNSWEjD1A89U0S606rUboFa; _okdetect=%7B%22token%22%3A%2217901837008160%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D; olfsk=olfsk27166769245347777; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1790183701180%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=4912-307-10-8101; _oklv=1790184601895%2CH8B4IkqSdmuwvUKm1A89U0SoBUAa6k0r; __gads=ID=c0bd7b6285729243:T=1790182727:RT=1790185365:S=ALNI_MYD9vqs2Z5kZkF4tyMitkjjwhAxbw; __gpi=UID=0000164a9282d5af:T=1790182727:RT=1790185365:S=ALNI_Ma-c_vg_E5KOvstwNMaB0P-cbZPIA; __eoi=ID=2dcff1c5def65db6:T=1790182727:RT=1790185365:S=AA-AfjZdYrAEOOCQTt5wYREZ8G7z; _twsid=1790182741001-376024521.1.1790185368922; _uetsid=1421da00b77011f18379730bde4335a9|1jdk6g4|2|g9p|0|2457; cto_bundle=R8FYYV9TZGRhYjklMkJ1JTJGNzBtUjgyaE9lTVpWQWdaaTJEczdKY0xsZHVaVWw5Und0Uk4wUUxjUVh3MDM3ZmdhMXhSVnVyOVJLVFREejIlMkZUWjZQU0VWQlp0JTJCTm9ialoyblJDdHpabSUyRndWRVphZ1JuZmltNUpRM3ZJWmFXejB6OU1MYTFmUjUlMkJYNnRPTGdrUVVHc0puY2ZQRTNUJTJGZyUzRCUzRA; AWSALB=phRv9gllygP5/aEqUStgUeOe4fgRKnQmAc7dh70ScnyDHBvIoRwH6SJIaMM3uekMkIBhhyxS8UrEugOQQ2FVfc8LKcTPRTRDIBBbcVndfX4jG28uukvrJslYGxaK; _ga_QPFFLXY66S=GS2.1.s1790182742$o1$g1$t1790185372$j53$l0$h981348673; _uetvid=1421fc70b77011f1869a31554eb8c083|1ity9o|1790185374194|15|1|bat.bing.com/p/insights/c/b; ttcsid=1790182742668::qGo0O7DdTdCYRCzROIkS.1.1790185374247.0::1.2624378.2628760::1004758.9.182.40::2623746.442.0; ttcsid_CII5303C77U0E450O1Q0=1790182742667::ZD2X5X5-H6EHflcLZ0nK.1.1790185374247.1',
}

DISCOVER_PATERN = re.compile("^https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$")

PRODUCT_PATTERN  = re.compile("^https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$")

TIME_OUT = 30

HEADERS_PDP= {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.fravega.com',
    'priority': 'u=1, i',
    'referer': 'https://www.fravega.com/p/perfume-risala-surur-edp-100-ml-para-unisex-23063754/',
    'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.1034203465.1790182740; _gcl_gs=2.1.k1$i1790182738$u61301243; ab-algolia=Algolia; _twpid=tw.1790182741001.125144287583586680; _gcl_aw=GCL.1790182742.EAIaIQobChMImsfsqZaFlwMVn1JIAB3lXjKKEAAYAyAAEgK_4fD_BwE; _gcl_dc=GCL.1790182742.EAIaIQobChMImsfsqZaFlwMVn1JIAB3lXjKKEAAYAyAAEgK_4fD_BwE; _ga=GA1.1.372318314.1790182742; quanticId=216a2ea7-127d-4774-b3ef-af592f31d8ab; datajazztrackingsession=a08e8625-0197-426a-88a2-4ed3d0b06a00; _fbp=fb.1.1790182742501.400822304759102915; _tt_enable_cookie=1; _ttp=01M37K9PKYMM86QY8FET7NNX9R_.tt.1.1790182742654; _hjSessionUser_242925=eyJpZCI6ImEwMzA1ZGFkLTYzNmItNTViNi1iZTMxLWQxYjg2MDY1ZGM1MCIsImNyZWF0ZWQiOjE3OTAxODI3NzkyNTQsImV4aXN0aW5nIjp0cnVlfQ==; AWSALBCORS=/MCrTWcpzFQfpPdN9grcbfDHjs896OS8NtEbopiA3h64NWBUV8JtFq7Tl0xyocWXr52GZywKQhxciCpHMuorphHzed+m9JpimHr/LBwh/BHChcyHH8I02/1f/KmE; wcsid=H8B4IkqSdmuwvUKm1A89U0SoBUAa6k0r; hblid=MXXBvgoAwTNSWEjD1A89U0S606rUboFa; _okdetect=%7B%22token%22%3A%2217901837008160%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D; olfsk=olfsk27166769245347777; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1790183701180%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=4912-307-10-8101; _oklv=1790184601895%2CH8B4IkqSdmuwvUKm1A89U0SoBUAa6k0r; _hjSession_242925=eyJpZCI6ImM4YWZjMzEwLTRhODQtNDI3Yy1iMGZjLTFjMmRkOTNkZTUwNCIsImMiOjE3OTAxODc4MTAzODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; __gads=ID=c0bd7b6285729243:T=1790182727:RT=1790188614:S=ALNI_MYD9vqs2Z5kZkF4tyMitkjjwhAxbw; __gpi=UID=0000164a9282d5af:T=1790182727:RT=1790188614:S=ALNI_Ma-c_vg_E5KOvstwNMaB0P-cbZPIA; __eoi=ID=2dcff1c5def65db6:T=1790182727:RT=1790188614:S=AA-AfjZdYrAEOOCQTt5wYREZ8G7z; cto_bundle=RUZ83l9TZGRhYjklMkJ1JTJGNzBtUjgyaE9lTVpWQkRhR2NTeFl0alYybHB2ekpoVnljUGYyVFhhTGlUWHZOZG94SEJCeHRxZERUU2hObFclMkYwVWhKODUxYzdTVVlGaUZCJTJGVXBpWm1DUzZUcmRQdlpLQWN4VElOakR6MzA5YUxlZjFFM2c3MUFuOTVnc25mMUFkazdtJTJGb3NiUWxTOGN3JTNEJTNE; _uetsid=1421da00b77011f18379730bde4335a9|1jdk6g4|2|g9p|0|2457; _uetvid=1421fc70b77011f1869a31554eb8c083|1y0tl62|1790188616721|5|1|bat.bing.com/p/insights/c/g; ttcsid_CII5303C77U0E450O1Q0=1790187810168::KAkskSMOLMcBQq30sf5I.2.1790188617988.1; ttcsid=1790187810169::4hUQUyAW3tTMvzy_nO6M.2.1790188617988.0::1.802432.805783::92198.5.467.2091::808178.109.0; _twsid=1790187809212-40451268.2.1790188623314; AWSALB=8F7DT1y8MttkmshBejhronLtfUKrVVL1opMVCivQhyaiRI1RAi1Xk6SkmxoPtq1xzcd8hm9fkeuP2bfc2jsJ2Vg6jj1o35EyHqiawpvlzUS3PQ3tg3+/9MVGf0I5; _ga_QPFFLXY66S=GS2.1.s1790187809$o2$g1$t1790188655$j9$l0$h2105533747',
}
