Padrondl
========

* [Página del proyecto](https://pmoracho.github.io/padrondl)
* [Proyecto en github](https://github.com/pmoracho/padrondl)
* [Descarga de ejecutable para windows](https://github.com/pmoracho/padrondl/raw/master/dist/padrondl-20161122.zip)

`Padrondl` es una herramienta de linea de comandos para descargar "padrones" de
los organismos públicos. Los "padrones" son archivos en distintos formatos que
organismos públicos como ser el [Afip](https://www.afip.gov.ar) o
[Agip](https://www.agip.gov.ar) publican en sus páginas con información
importante sobre contribuyentes. Más allá de lo comentado `padrondl` funciona
como un "downloader" de archivos publicados en la web.

A la fecha solo procesa archivos definidos en un tag `<href>` o mediante un
link directo, más adelante iremos implementado en la medida de nuestras
necesidades otros métodos para encontrar y descargar archivos desde un página
web.

La configuración de las decargas se realiza en un archivo de configuración
ubicado en la misma carpeta dónde se encuentra esta herramienta y que se
denomina `padrondl.cfg`.

Esta es la configuación actual

```
[padron:rgg]
type		= href
name		= Régimen general de ingresos brutos - CABA
url 		= https://www.agip.gob.ar/agentes/agentes-de-recaudacion-e-informacion
hreftext 	= Padrón de Regímenes Generales - Vigencia
domain 		= https://www.agip.gob.ar/
filemask	= ^\w*.rar

[padron:cfsd]
name		= Condiciones tributarias - Sin denominación
type		= href
domain 		= http://www.afip.gob.ar/genericos/cInscripcion/
url		 	= %(domain)s/archivoCompleto.asp
hreftext 	= Archivo condición tributaria sin denominación
filemask	=

[padron:cfcd]
name		= Condiciones tributarias - Con denominación
type		= href
domain 		= http://www.afip.gob.ar/genericos/cInscripcion/
url		 	= %(domain)s/archivoCompleto.asp
hreftext 	= Archivo condición tributaria con denominación
filemask	=

[padron:2226]
name		= Certificados de Exclusión Ret/Percep del Impuesto al Valor Agregado
type		= link
domain 		= https://www.afip.gob.ar/genericos/rg17/
url		 	= https://www.afip.gob.ar/genericos/rg17/archivos/rg17.zip
hreftext 	= Transferencia del archivo completo - Resolución General 2226
filemask	=
```

Como vemos, hay configurado cuatro padrones:

* AGIP - Régimen general de ingresos brutos - CABA
* AFIP - Condiciones tributarias - Sin denominación
* AFIP - Condiciones tributarias - Con denominación
* AFIP - Certificados de Exclusión Ret/Percep del Impuesto al Valor Agregado

# Detalle de la configuración

* Cada padrón tiene un <id> único que se configura como parte del nombre de la
  sección, por ejemplo `[padron:rgg]` define el <id> "rgg"

* `name`: Es simplemente la descripción del padrón

* `type`: Define el tipo de acceso al archivo. Actualmente ya dijimos solo está
  habilitado el tipo "href" y "link" que indica un proceso dónde lo que se
  espera es que el link al archivo se encuenter asociado a una etiqueta
  `<href>` o sea un enlace directo.

* `domain`: Página inicial, en algunos casos el padrón se publica con una
  referencia relativa a esta página, por lo que en el enlace no tendremos la
  ruta completa, configurando este dato el proceso podrá componer la url exacta
  al archivo.

* `url`: Página dónde se encuentra la refefencia al padrón

* `hreftext`: Texto del enlace (puede ser parte del mismo) sirve para
  aseguraranos que el enlace es el correcto


# Algunos puntos claves de este proyecto:

* Herramienta de línea de comandos
* Descarga de archivos desde páginas web
* Configurable

# Requerimientos e instalación:

En Windows, nada en particular ya que se distribuye la herramienta "congelada"
mediante **Pyinstaller**. Descargarla y copiarla en alguna carpeta del sistema,
idealmente que esté apuntada al path.

* Para descargar *Padrondl**, ir a
  [Releases](padrondl/releases)
* El proyecto original en [**Github**](https://github.com/pmoracho/padrondl)


# Ejemplos de Uso:

## Invocación sin parámetros o con `--help

```
uso: padrondl [-h] [--version] [--show-padrones] [--log-level LOGLEVEL]
              [--output-path OUTPUTPATH]
              [padron]

Descarga de padrones (c) 2016, Patricio Moracho <pmoracho@gmail.com>

argumentos posicionales:
  padron                                   Padrón a descargar

argumentos opcionales:
  -h, --help                               mostrar esta ayuda y salir
  --version, -v                            Mostrar el número de versión y
                                           salir
  --show-padrones, -s                      Verifciación completa. c:
                                           algoritmos de compresión, e:
                                           algoritmos de encriptación.
  --log-level LOGLEVEL, -n LOGLEVEL        Nivel de log
  --output-path OUTPUTPATH, -o OUTPUTPATH  Carpeta de outputh del padrón
                                           descargado.
```

## `padrondl -s`

Listar los padrones habilitados para descarga

```
+----------+---------------------------------------------------------------------+
|   Padrón | Descripción                                                         |
|----------+---------------------------------------------------------------------|
|      rgg | Régimen general de ingresos brutos - CABA                           |
|     cfsd | Condiciones tributarias - Sin denominación                          |
|     cfcd | Condiciones tributarias - Con denominación                          |
|     2226 | Certificados de Exclusión Ret/Percep del Impuesto al Valor Agregado |
+----------+---------------------------------------------------------------------+
```

## `padrondl rgg`

Descarga del padrón del régimen general de ingresos brutos

```
Descargando ARDJU008112016.rar...
 19% ( 761 of 3950) |###################################                                                                                                                                                   | Elapsed Time: 0:00:03 ETA: 0:00:15
```

# Notas para el desarrollador:

## Requerimientos básicos:

Tener instalado y funcionando:

* [Git][git]
* [Python 3.x][python]

## Entorno inicial básico

El primer paso es descargar el repositorio y preparar el entorno inicial que
servirá tanto sea para desarrollo como para eventual ejecución de la
herramienta.

* Clonar repositorio
* Crear entorno virtual
* Activar entorno virtual
* actualizar `pip` y `setuptool`
* Instalar requerimientos

```
git clone <url_https_del_proyecto>
cd <proyecto>
python3 -m venv .venv --prompt=<proyecto>

# En Windows
.venv\Scripts\activate.bat

# En Linux
source .venv/bin/activate

# Actualizar pip y setuptools
python -m pip install --upgrade pip
pip install --upgrade setuptools

# Instalar  paquetes requeridos
pip install -r requirements.txt
```

**Nota**: reemplazar `<url_https_del_proyecto>` por la dirección url que nos da
`github` para este repositorio y `<proyecto>` por el nombre del repositorio,
ejemplo: `padrondl`

## Despliegue

Para instalar o desplegar la herramienta, usamos [`pyinstaller`][https://pyinstaller.org/en/stable/], instalarlo en el entorno virtual del proyecto mediante:

```
pip install pyinstaller
```

Luego, para generar el ejecutable:

```
pyinstaller padrondl.py --onefile --version-file version.txt
```

# Changelog:

#### Version 1.2.0 - 2022-08-02

* Update a **Python 3.10** y actualización de librerías
* Fix por cambio en página del Agip
* Eliminamos carpeta `dist` y creamos `version.txt`

#### Version 1.1 - 2017-07-16
* Descarga por link directo
* Output path configurable medainte parámetro `--output-path -o`
* Log
* Generación de "Flag File" por padrón.

#### Version 1.0 - 2016-11-22
* Primera versión

