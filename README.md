Padrondl
========

* [Página del proyecto](https://pmoracho.github.io/padrondl)
* [Proyecto en github](https://github.com/pmoracho/padrondl)
* [Descarga de ejecutable para windows](None)


`Padrondl` es una herramienta de linea de comandos para descargar "padrones" de
los organismos públicos. Los "padrones" son archivos en distintos formatos que
organismos públicos como ser el Afip o Agip publican en sus páginas con
información importante sobre contribuyentes. Más allá de lo coemtado `padrondl`
funciona como un "downloader" de archivos publicados en la web.

A la fecha solo procesa archivos definidos en un tag `<href>`, más adelante
iremos implementado en la medida de nuestras necesidades otros métodos para
encontrar y descargar archivos desde un página web.

La configuración de las decargas se realiza en un archivo de configuración 
ubicado en la misma carpeta dónde se encuentra esta herramienta y que se
denomina `padrondl.cfg`.

Esta es la configuación actual

```
[general]
outputpath	= c:\Tmp

[padron:rgg]
type		= href
name		= Régimen general de ingresos brutos - CABA
url 		= http://www.agip.gob.ar/agentes/agentes-de-recaudacion-e-informacion
hreftext 	= Padrón de Regímenes Generales
domain 		= http://www.agip.gob.ar/

[padron:cfsd]
name		= Condiciones tributarias - Sin denominación
type		= href
domain 		= http://www.afip.gob.ar/genericos/cInscripcion/
url		 	= %(domain)s/archivoCompleto.asp
hreftext 	= Archivo condición tributaria sin denominación

[padron:cfcd]
name		= Condiciones tributarias - Con denominación
type		= href
domain 		= http://www.afip.gob.ar/genericos/cInscripcion/
url		 	= %(domain)s/archivoCompleto.asp
hreftext 	= Archivo condición tributaria con denominación
```

Como vemos, hay configurado tres padrones:

* AGIP - Régimen general de ingresos brutos - CABA
* AFIP - Condiciones tributarias - Sin denominación
* AFIP - Condiciones tributarias - Con denominación

# Detalle de la configuración

* Cada padrón tiene un <id> único que se configura como parte del nombre de la
  sección, por ejemplo `[padron:rgg]` define el <id> "rgg"

* `name`: Es simplemente la descripción del padrón

* `type`: Define el tipo de acces al archivo. Actualmente ya dijimos solo está
  habilitado el tipo "href" que indica un proceso dónde lo que se espera es que
  el link al archivo se encuenter asociado a una etiqueta `<href>`

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

* Para descargar y descomprimir **Padrondl**, hacer click
  [aqui](None)
* El proyecto en [**Github**](https://github.com/pmoracho/padrondl)


# Ejemplos de Uso:

## Invocación sin parámetros o con `--help

```
uso: padrondl [-h] [--show-padrones] [--version] [padron]

Descarga de padrones (c) 2016, Patricio Moracho <pmoracho@gmail.com>

argumentos posicionales:
  padron               Padrón a descargar

argumentos opcionales:
  -h, --help           mostrar esta ayuda y salir
  --show-padrones, -s  Verifciación completa. c: algoritmos de compresión, e:
                       algoritmos de encriptación.
  --version, -v        Mostrar el número de versión y salir

```

## `padrondl -s` 

Listar lospadrones habilitados para descarga

```
+----------+--------------------------------------------+
|   Padrón | Descripción                                |
|----------+--------------------------------------------|
|      rgg | Régimen general de ingresos brutos - CABA  |
|     cfsd | Condiciones tributarias - Sin denominación |
|     cfcd | Condiciones tributarias - Con denominación |
+----------+--------------------------------------------+
```

## `padrondl rgg`

Descarga del padrón del régimen general de ingresos brutos

```
Descargando ARDJU008112016.rar...
 19% ( 761 of 3950) |###################################                                                                                                                                                   | Elapsed Time: 0:00:03 ETA: 0:00:15
```

# Notas para el desarrollador:

## Requisitos iniciales

El proyecto **parseit** esta construido usando el lenguaje **python**, a la
fecha no se usan librerías adicionales a las propias de python, pero de todas
formas es recomendable preparar antes que nada, un entorno de desarrollo. A
continuación expondremos en detalle cuales son los pasos para tener preparado
el entorno de desarrollo. Este detalle esta orientado a la implementación sobre
Windows 32 bits, los pasos para versiones de 64 bits son sustancialmente
distintos, en particular por algunos de los "paquetes" que se construyen a
partir de módulos en C o C++, de igual forma la instalación sobre Linux tiene
sus grandes diferencias. Eventualmente profundizaremos sobre estos entornos,
pero en principio volvemos a señalar que el siguiente detalle aplica a los
ambientes Windows de 32 bits:

* Obviamente en primer lugar necesitaremos
  [Python](https://www.python.org/ftp/python/3.4.0/python-3.4.0.msi), por ahora
  únicamente la versión 3.4. La correcta instalación se debe verificar desde la
  línea de comandos: `python --version`. Si todo se instaló correctamente se
  debe ver algo como esto `Python 3.4.0`, sino verificar que Python.exe se
  encuentre correctamente apuntado en el PATH.

* Es conveniente pero no mandatorio hacer upgrade de la herramienta pip:
  `python -m pip install --upgrade pip`

* [Virutalenv](https://virtualenv.pypa.io/en/stable/). Es la herramienta
  estándar para crear entornos "aislados" de python. Para no tener conflictos
  de desarrollo lo que haremos mediante esta herramienta es crear un "entorno
  virtual" de python en una carpeta del proyecto (venv). Este "entorno virtual"
  contendrá una copia completa de Python, al activarlo se modifica el PATH al
  python.exe que apuntará ahora a nuestra carpeta del entorno, evitando
  cualquier tipo de conflicto con un entorno Python ya existente. La
  instalación de virtualenv se hara mediante `pip install virtualenv`

* Descargar el proyecto desde [Github](https://github.com/pmoracho/parseit), se
  puede descargar desde la página el proyecto como un archivo Zip, o si
  contamos con [Git](https://git-for-windows.github.io/) sencillamente haremos
  un `git clone https://github.com/pmoracho/parseit`.

* El proyecto una vez descomprimido o luego del clonado del repositorio tendrá
  una estructura de directorios similar a la siguiente:

```
parseit.git
   |-dist
   |-tests
   |-tools
```

## Preparación del entorno virtual local

Para poder ejecutar, o crear la distribución de la herramientas, lo primero que
deberemos hacer es armar un entorno python "virtual" que alojaremos en una
subcarpeta del directorio principal que llamaremos "venv". En el proyecto
incorporamos una herramienta de automatización de algunas tareas básicas. Se
trata de `make.py`, la forma de ejecutarlo es la siguiente: `python
tools\make.py <comando>` la ejecución si parámetros o mediante el parámetro
`--help` arrojará una salida como lo que sigue:

```
Automatización de tareas para el proyecto Paresit
(c) 2016, Patricio Moracho <pmoracho@gmail.com>

Uso: make <command> [<args>]

Los comandos más usados:
   devcheck   Hace una verificación del entorno de desarrollo
   devinstall Realiza la instalación del entorno de desarrollo virtual e instala los requerimientos
   docinstall Intalación de Sphinx
   clear      Elimina archivos innecesarios
   test       Ejecuta todos los tests definidos del proyecto
   build      Construye la distribución binaria de las herramientas del proyecto

argumentos posicionales:
  command     Comando a ejecutar

argumentos opcionales:
  -h, --help  mostrar esta ayuda y salir
```

Para preparar el entorno virtual simplemente haremos `python tools\make.py
devinstall`, este proceso si resulta exitoso deberá haber realizado las
siguientes tareas:

* Creación de un entorno pyhton virtual en la carpeta "venv", invocable
  mediante `venv\Scripts\activate.bat` en Windows o `source
  venv/Scripts/activate` en entornos Linux o Cygwin/Mingw (en Windows)
* Instalado todas las dependencias necesarias


## Notas adicionales:

* Es recomendable y cómodo, pero entiendo que no es mandatorio, contar con un
  entorno estilo "Linux", por ejemplo [MinGW](http://www.mingw.org/), tal como
  dice la página del proyecto: "MinGW provides a complete Open Source
  programming tool set which is suitable for the development of native
  MS-Windows applications, and which do not depend on any 3rd-party C-Runtime
  DLLs. (It does depend on a number of DLLs provided by Microsoft themselves,
  as components of the operating system; most notable among these is
  MSVCRT.DLL, the Microsoft C runtime library. Additionally, threaded
  applications must ship with a freely distributable thread support DLL,
  provided as part of MinGW itself)." De este entorno requerimos algunas
  herramientas de desarrollo: Bash para la línea de comandos y Make para la
  automatización de varias tareas del proyecto. 

* Usar "soft tabs": Con cualquier editor que usemos configurar el uso del <tab>
  en vez de los espacios, yo prefiero el <tab> puro al espacio, entiendo que es
  válido el otro criterio pero ya los fuentes están con esta configuración, por
  lo que para evitar problemas al compilar los .py recomiendo seguir usando
  este criterio. Asimismo configurar en 4 posiciones estos <tab>.


# Changelog:

#### Version 1.0 - 2016-11-22
* Primera versión
