from curl_cffi import requests
from log import Log
from lxml import etree

import json
import config

class Discovery:
    def __init__(self):
        self.log = Log().get_logger("logs/logs")
        self.pages=[]
        self.prods = []

    def make_requests(self,url=None,params=None,headers=None,impersonate=None,proxies=None,timeout=None):
        for intent in range(config.MAX_RETRIES):
            try:
                self.log.info(f"peticion URL: {url}| intento: {intent +1}")
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
                    self.log.warning(f"fallo en la peticion {url}| intento numero: {intent +1}")
            except Exception as e:
                self.log.error(f"error en peticion: {url}| intentos: {intent+1} | error en : {e}")

    def get_pags(self):
        try:
            response = self.make_requests(
                url=f"{config.BASE_URL}/sitemap/index.xml",
                impersonate="chrome",
                timeout=config.TIMEOUT,
                # proxies=config.PROXIES
            )
            arbol_pags_xml = etree.fromstring(response.content)

            arbol_pags = arbol_pags_xml.xpath("//sm:loc/text()",namespaces=config.NAMESPACES)
            
            for pag in arbol_pags:
                self.log.info(f" obteniendo paginados de productos: {pag}")
                if config.REGEX_PG.fullmatch(pag):
                    self.pages.append(pag)
            # print(self.pages)   
        except Exception as e:
            self.log.error(f"error en {e}")

    def get_prods(self):
        try:
            for url_prods in self.pages:
                # print(url_prods)
                response = self.make_requests(
                    url = str(url_prods),
                    impersonate="chrome",
                    timeout=config.TIMEOUT,
                    # proxies=config.PROXIES
                )
            
                if response.status_code == 200:
                    arbol_prods_xml = etree.fromstring(response.content)
                    
                    arbol_prods = arbol_prods_xml.xpath("//sm:loc/text()",namespaces=config.NAMESPACES)
                                
                    for prod in arbol_prods:
                        if config.REGEX_PROD.fullmatch(prod):
                            self.prods.append(prod)
                else:
                    self.log.warning(f"no se obtuvo respuesta en {url_prods}")
                    # print(self.prods[0])
        except Exception as e:
            self.log.error(f"error en {e}")

    def run(self):
        self.get_pags()
        self.get_prods()
        return self.prods

class PDP:
    def __init__(self,prods):
        self.log = Log().get_logger("logs/logs")
        self.prods = prods
        self._records = []
    def make_requests(self,url=None,params=None,headers=None,impersonate=None,proxies=None,timeout=None,json=None,cookies=None):
        for intent in range(config.MAX_RETRIES):
            try:
                self.log.info(f"peticion URL: {url}| intento: {intent +1}")
                response = requests.get(
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=timeout,
                    proxies=proxies,
                    impersonate=impersonate,
                    json=json,
                    cookies=cookies
                )

                if response.status_code == 200:
                    return response
                else:
                    self.log.warning(f"fallo en la peticion {url}| intento numero: {intent +1}")
            except Exception as e:
                self.log.error(f"error en peticion: {url}| intentos: {intent+1} | error en : {e}")

    def parse_prods(self):

        # print(self.prods[32])
        # input("press any key")
        for prod in self.prods[:2]:
            #obtengo SKU
            handler = prod.replace("https://www.fravega.com/p/","").replace("/","")
            sku = handler.split("-")[-1]
            json_data = config.JSON_DATA
            json_data["variables"]["sku"] = sku
            # print(json_data)
            # print(prod)
            response = requests.post(
                url=config.API,
                timeout=config.TIMEOUT,
                impersonate="chrome",
                json=json_data,
                # proxies=config.PROXIES,
                headers=config.HEADERS,
                cookies=config.COOKIES
            )
            
            sku_prod_json = json.loads(response.content)
            sku_prod = sku_prod_json["data"]["sku"]
            #parseo
            self.parse_prod(sku_prod,prod)
            #guardo

            self.log.info(f"guardando dato - {prod}")
            self.save_data()

            # self.verificacion()

    def parse_prod(self,sku_prod,prod):
        #limpio description
        # seodescription_notclean = sku_prod["item"].get("seoDescription",None)
        # seodescription = html.fromstring("string(seodescription_notclean)")
        # print(sku_prod)
        # input("press any key")
        # item_prueba = sku_prod["item"]
        # print(item_prueba)
        #limpio specifications
        if sku_prod["item"].get("specifications"):
            specifications = []
            for ver in sku_prod["item"].get("specifications"):
                spec = {
                    "name" : ver["name"],
                    "value" : ver["value"]
                }
                specifications.append(spec)


        json_parse = {
            "url": prod,
            "code": sku_prod.get("code",None),
            "id": sku_prod["item"].get("id",None),
            "title":  sku_prod["item"].get("title",None),
            "slug":  sku_prod["item"]["brand"].get("slug",None),
            "description": sku_prod["item"].get("seoDescription",None),
            "brand": sku_prod["item"].get("brand",None),
            "image_main": None,
            "images": None,
            "price": None,
            "sale_price": None,
            "discount_price": None,
            "discount_percentage": None,
            "availability": "in_stock" if sku_prod["stock"].get("availability") else "out_of_stock",
            "gtin": None,
            "specifications": specifications if specifications else None,
            "store_name": "fravega",
            "seller_url": "https://www.fravega.com/"
        }
        self._records.append(json_parse)

    def verificacion(self):
        with open("output/data.json","r",encoding="utf-8") as file:
            
            datos = file.readline()
            print(len(datos))
    def save_data(self):
        try:
            
            with open("output/data.json","a",encoding="utf-8")as file:
                file.write(f"{json.dump(self._records,file,ensure_ascii=False)}\n")

        except Exception as e:
            self.log.error(f"error {e}")

    def run(self):
        self.parse_prods()

if __name__ == "__main__":
    prods = Discovery().run()
    # prods = ["https://www.fravega.com/p/alfombra-united-weavers-30x91-cm-sky-blue-portsmouth-23061934/"]
    PDP(prods).run()