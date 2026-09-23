# Web Scraping Essentials — Recuperatorio Final

## Frávega Product Scraper

Este proyecto corresponde al **recuperatorio del examen final del curso Web Scraping Essentials**.

El objetivo consiste en desarrollar un scraper capaz de recopilar el catálogo de productos disponible públicamente en el sitio web de Frávega.

**Sitio objetivo:**

```text
https://www.fravega.com/
```

La solución deberá descubrir los productos disponibles, acceder a sus páginas individuales, extraer la información solicitada y generar una salida estructurada en formato JSON.

El desarrollo deberá contemplar mecanismos de tolerancia a errores, persistencia de datos durante la ejecución, logging y medidas destinadas a reducir bloqueos durante la recopilación.

---

# 1. Objetivo

Desarrollar una solución de Web Scraping que permita:

- Descubrir los productos publicados en Frávega.
- Recorrer las URLs correspondientes a páginas de producto.
- Extraer la información requerida para cada producto.
- Normalizar los datos según el esquema definido.
- Implementar reintentos ante errores temporales.
- Mantener persistencia de los datos durante la ejecución.
- Registrar información relevante mediante logging.
- Gestionar correctamente información sensible mediante variables de entorno.
- Implementar rotación de proxies.
- Generar un archivo JSON con los resultados obtenidos.

La implementación y las decisiones técnicas necesarias para cumplir estos requerimientos forman parte de la evaluación.

---

# 2. Fuente de datos

El dominio principal del proyecto es:

```text
https://www.fravega.com/
```

El scraper deberá ser capaz de obtener los productos disponibles públicamente en el sitio.

Para facilitar la identificación de determinados recursos, se proporcionan las siguientes expresiones regulares.

### Sitemap de productos

```regex
^https:\/\/www\.fravega\.com\/sitemap\/productos-\d+\.xml$
```

Ejemplo:

```text
https://www.fravega.com/sitemap/productos-01.xml
```

### Páginas de producto

```regex
^https:\/\/www\.fravega\.com\/p\/[^\/]+-\d+\/?$
```

Ejemplo:

```text
https://www.fravega.com/p/xiaomi-redmi-15c-4gb-256gb-midnight-black-990305814/
```

Las expresiones regulares anteriores se proporcionan como referencia y podrán utilizarse durante el proceso de descubrimiento y validación de URLs.

---

# 3. Campos requeridos

Por cada producto encontrado deberá generarse un objeto con la siguiente estructura:

```json
{
    "url": null,
    "code": null,
    "id": null,
    "title": null,
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
```

---

# 4. Definición de campos

| Campo | Descripción |
|---|---|
| `url` | URL completa de la página del producto. |
| `code` | Código identificador del producto publicado por el sitio. |
| `id` | Identificador interno del producto. |
| `title` | Nombre o título del producto. |
| `slug` | Slug correspondiente al producto. |
| `description` | Descripción del producto. |
| `brand` | Marca del producto. |
| `image_main` | URL de la imagen principal. |
| `images` | Lista de imágenes adicionales asociadas al producto. |
| `price` | Precio regular/base del producto. |
| `sale_price` | Precio de venta vigente cuando corresponda. |
| `discount_price` | Valor monetario del descuento cuando pueda determinarse. |
| `discount_percentage` | Porcentaje de descuento del producto cuando corresponda. |
| `availability` | Disponibilidad normalizada del producto. |
| `gtin` | GTIN/EAN/UPC u otro GTIN disponible para el producto. |
| `specifications` | Lista de especificaciones técnicas representadas mediante pares `name` / `value`. |
| `store_name` | Valor constante `fravega`. |
| `seller_url` | Valor constante `https://www.fravega.com/`. |

---

# 5. Valores faltantes

Cuando un campo requerido no exista, no se encuentre publicado o no pueda determinarse a partir de la información disponible, deberá utilizarse:

```python
None
```

Al serializar el resultado como JSON, este valor será representado como:

```json
null
```

No deberán utilizarse valores inventados para completar información faltante.

---

# 6. Disponibilidad

El campo `availability` deberá normalizarse exclusivamente a uno de los siguientes valores:

```text
in_stock
out_of_stock
```

Cuando no sea posible determinar la disponibilidad del producto, deberá utilizarse:

```python
None
```

No deberán utilizarse textos propios del sitio como valores finales del campo.

---

# 7. Especificaciones

Las especificaciones técnicas deberán almacenarse utilizando una lista de objetos.

Ejemplo:

```json
"specifications": [
    {
        "name": "Memoria RAM",
        "value": "4 GB"
    },
    {
        "name": "Almacenamiento",
        "value": "256 GB"
    },
    {
        "name": "Color",
        "value": "Midnight Black"
    }
]
```

Cada especificación deberá conservar la relación entre su nombre y su correspondiente valor.

---

# 8. Imágenes

`image_main` deberá contener la imagen principal identificada para el producto.

`images` deberá almacenar las imágenes adicionales disponibles.

Ejemplo:

```json
{
    "image_main": "https://example.com/main.jpg",
    "images": [
        "https://example.com/image-2.jpg",
        "https://example.com/image-3.jpg"
    ]
}
```

Se deberá evitar, cuando sea posible, almacenar URLs duplicadas dentro de `images`.

---

# 9. Reintentos

Las solicitudes HTTP deberán implementar una estrategia de **reintentos**.

El scraper deberá poder recuperarse de errores temporales sin finalizar inmediatamente toda la ejecución.

La estrategia deberá contemplar situaciones como:

- Errores temporales del servidor.
- Timeouts.
- Problemas transitorios de conexión.
- Respuestas HTTP susceptibles de ser reintentadas.
- Fallos temporales relacionados con proxies.

La cantidad de intentos, tiempos de espera y estrategia utilizada quedan a criterio del desarrollador.

---

# 10. Persistencia durante la ejecución

El scraper deberá implementar una estrategia de **guardado durante la ejecución**.

No se considerará suficiente mantener todos los productos únicamente en memoria para escribir el archivo cuando finalice el proceso completo.

La solución deberá reducir el riesgo de pérdida de información frente a situaciones como:

- Interrupción manual.
- Error inesperado.
- Pérdida de conexión.
- Bloqueo del sitio.
- Fallo del proxy.
- Excepción no controlada.
- Cierre inesperado del proceso.

El mecanismo específico de persistencia queda a criterio del desarrollador.

---

# 11. Logging

El proyecto deberá utilizar el módulo `logging` de Python o una solución equivalente correctamente configurada.

Los logs deberán permitir monitorear la ejecución e identificar problemas.

Como mínimo, deberán poder diferenciar eventos de tipo:

```text
INFO
WARNING
ERROR
```

Los mensajes deberán aportar contexto suficiente para diagnosticar problemas durante la ejecución.

No se deberá utilizar exclusivamente `print()` como mecanismo de monitoreo del scraper.

---

# 12. Variables de entorno

La información sensible o dependiente del entorno no deberá estar escrita directamente en el código fuente.

Cuando corresponda, deberán utilizarse variables de entorno para información como:

- Credenciales.
- API Keys.
- Tokens.
- Configuración de proxies.
- Usuarios.
- Contraseñas.

El proyecto deberá incluir:

```text
.env
.env.example
```

El archivo `.env` no deberá ser versionado.

El archivo `.env.example` deberá contener únicamente los nombres de las variables necesarias y valores de ejemplo que no expongan credenciales reales.

---

# 13. Rotación de proxies

El scraper deberá implementar una estrategia de **rotación de proxies** destinada a reducir bloqueos durante la recopilación.

La implementación deberá contemplar correctamente:

- Selección o rotación de proxies.
- Manejo de proxies que fallen.
- Integración con la estrategia de reintentos.
- Protección de credenciales mediante variables de entorno cuando sea necesario.

Las credenciales reales de los proxies no deberán estar hardcodeadas ni incluirse en el repositorio.

---

# 14. Selenium

Selenium podrá utilizarse únicamente cuando sea necesario para obtener información que no pueda recuperarse razonablemente mediante solicitudes HTTP convencionales.

Si Selenium forma parte de la solución, su configuración deberá centralizarse en:

```text
web_driver.py
```

La lógica específica de configuración del navegador no deberá quedar distribuida innecesariamente por el proyecto.

---

# 15. Estructura requerida

El proyecto deberá respetar como mínimo la siguiente estructura:

```text
fravega-scraper/
│
├── main.py
├── config.py
├── log.py
├── web_driver.py
│
├── .env
├── .env.example
├── .gitignore
│
├── requirements.txt
├── README.md
├── docs.md
│
└── output/
    └── ...
```

Podrán agregarse módulos, clases, archivos o directorios adicionales cuando la arquitectura elegida lo requiera.

---

# 16. Responsabilidad de cada archivo

### `main.py`

Deberá contener o coordinar la lógica principal de ejecución del scraper.

### `config.py`

Deberá centralizar:

- Constantes.
- Configuración general.
- Lectura/importación de variables de entorno.
- Parámetros globales necesarios para el scraper.

### `.env`

Contendrá las variables de entorno utilizadas localmente.

No deberá subirse al repositorio.

### `.env.example`

Deberá documentar las variables de entorno necesarias sin incluir credenciales reales.

### `requirements.txt`

Deberá contener las dependencias necesarias para ejecutar el proyecto.

Las dependencias deberán especificarse correctamente y ser reproducibles en otro entorno.

### `log.py`

Deberá contener la configuración relacionada con el sistema de logging.

### `web_driver.py`

Deberá contener la configuración del WebDriver cuando la solución utilice Selenium.

Si Selenium no resulta necesario, el archivo podrá mantenerse sin uso o documentarse esta decisión.

### `.gitignore`

Deberá excluir archivos que no correspondan al repositorio, especialmente:

```text
.env
__pycache__/
*.pyc
```

También deberán excluirse otros archivos temporales o locales que el desarrollador considere necesarios.

### `output/`

Directorio destinado al almacenamiento de los datos obtenidos durante y/o al finalizar la ejecución.

### `docs.md`

Deberá contener la documentación técnica necesaria para instalar y ejecutar el proyecto.

Como mínimo deberá documentar:

- Versión de Python utilizada.
- Procedimiento para iniciar el proyecto localmente.
- Creación y utilización del entorno virtual.
- Instalación de dependencias.
- Variables de entorno requeridas.
- Librerías utilizadas.
- Versión de las librerías.
- Configuración adicional necesaria.
- Comando o mecanismo utilizado para ejecutar el scraper.

`docs.md` deberá permitir que otro desarrollador pueda preparar correctamente el entorno y ejecutar el proyecto.

### `README.md`

Contendrá los requerimientos funcionales y técnicos del proyecto definidos en este documento.

---

# 17. Archivo de salida

El resultado deberá almacenarse dentro del directorio:

```text
output/
```

El formato final requerido será:

```text
JSON
```

El archivo deberá contener los productos procesados utilizando exactamente los campos definidos en este documento.

Ejemplo conceptual:

```json
[
    {
        "url": "https://www.fravega.com/p/example-123/",
        "code": "ABC123",
        "id": "123",
        "title": "Producto de ejemplo",
        "slug": "producto-de-ejemplo",
        "description": "Descripción del producto",
        "brand": "Marca",
        "image_main": "https://example.com/main.jpg",
        "images": [
            "https://example.com/image-2.jpg"
        ],
        "price": 100000,
        "sale_price": 85000,
        "discount_price": 15000,
        "discount_percentage": 15,
        "availability": "in_stock",
        "gtin": "7790000000000",
        "specifications": [
            {
                "name": "Color",
                "value": "Negro"
            }
        ],
        "store_name": "fravega",
        "seller_url": "https://www.fravega.com/"
    }
]
```

Los valores anteriores son únicamente ilustrativos y no representan un producto real.

---

# 18. Calidad de los datos

La solución deberá priorizar la consistencia y calidad de la información obtenida.

Se deberá prestar especial atención a:

- Eliminación de espacios innecesarios.
- Normalización de precios.
- Correcta asociación entre nombres y valores de especificaciones.
- URLs completas y válidas.
- Eliminación de duplicados.
- Consistencia de tipos de datos.
- Correcta representación de valores faltantes.
- Correcta normalización de disponibilidad.
- Evitar información inventada o inferida sin una fuente válida.

---

# 19. Manejo de errores

El scraper deberá manejar adecuadamente errores esperables durante una ejecución de larga duración.

Un error sobre un producto individual no debería provocar, cuando sea técnicamente posible evitarlo, la pérdida completa de la ejecución.

Los errores relevantes deberán quedar registrados mediante el sistema de logging.

---

# 20. Requisitos técnicos obligatorios

La entrega deberá demostrar como mínimo:

- Descubrimiento de los productos disponibles.
- Extracción de los campos solicitados.
- Generación de salida JSON.
- Manejo correcto de valores faltantes.
- Reintentos de solicitudes.
- Persistencia durante la ejecución.
- Logging.
- Rotación de proxies.
- Uso correcto de variables de entorno.
- Separación adecuada de configuración y lógica.
- Archivo `.gitignore`.
- Dependencias declaradas en `requirements.txt`.
- Documentación técnica en `docs.md`.
- Organización del proyecto según la estructura solicitada.

---

# 21. Criterio general de implementación

Este documento define **qué debe cumplir la solución**, pero no prescribe una implementación específica.

El estudiante deberá decidir, justificar e implementar aspectos como:

- Estrategia de descubrimiento de productos.
- Librerías HTTP utilizadas.
- Estrategia de parsing.
- Necesidad o no de utilizar Selenium.
- Estrategia de reintentos.
- Estrategia de rotación de proxies.
- Estrategia de persistencia.
- Organización interna del código.
- Tratamiento de errores.
- Normalización de datos.

Estas decisiones forman parte del recuperatorio y deberán reflejar una solución mantenible, reproducible y apropiada para un proyecto de Web Scraping.

---

## Entrega

La entrega deberá incluir el proyecto completo y todos los archivos necesarios para poder instalarlo y ejecutarlo siguiendo la documentación proporcionada.

No deberán incluirse:

- Credenciales reales.
- Tokens.
- API Keys privadas.
- Contraseñas.
- Credenciales de proxies.
- Archivos `.env` con información sensible versionados en el repositorio.

El proyecto deberá poder configurarse a partir de `.env.example` y de las instrucciones proporcionadas en `docs.md`.

---

**Curso:** Web Scraping Essentials  
**Evaluación:** Recuperatorio del examen final  
**Proyecto:** Frávega Product Scraper