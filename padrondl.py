#!python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# padrondl.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation. A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""
padrondl
========

Herramienta de línde de comando para la descarga de padrones
de contribuyanetes de los distintos organismos del estado.

"""

__author__		= "Patricio Moracho <pmoracho@gmail.com>"
__appname__		= "padrondl"
__appdesc__		= "Descarga de padrones"
__license__		= 'GPL v3'
__copyright__	= "(c) 2016, %s" % (__author__)
__version__		= "0.9"
__date__		= "2016/11/11"


try:
	import sys
	import gettext
	from gettext import gettext as _
	gettext.textdomain('padrondl')

	def _my_gettext(s):
		"""Traducir algunas cadenas de argparse."""
		current_dict = {'usage: ': 'uso: ',
						'optional arguments': 'argumentos opcionales',
						'show this help message and exit': 'mostrar esta ayuda y salir',
						'positional arguments': 'argumentos posicionales',
						'the following arguments are required: %s': 'los siguientes argumentos son requeridos: %s'}

		if s in current_dict:
			return current_dict[s]
		return s

	gettext.gettext = _my_gettext

	import argparse
	import requests
	import progressbar
	import codecs
	import re
	import os
	import logging
	from urllib.parse import urlparse
	from bs4 import BeautifulSoup
	from configparser import ConfigParser
	from tabulate import tabulate
	from unicodedata import normalize


except ImportError as err:
	modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
	print(_("No fue posible importar el modulo: %s") % modulename)
	sys.exit(-1)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')

def init_argparse():
	"""Inicializar parametros del programa."""
	cmdparser = argparse.ArgumentParser(prog=__appname__,
										description="%s\n%s\n" % (__appdesc__, __copyright__),
										epilog="",
										add_help=True,
										formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50)
	)

	opciones = {	"padron": {
								"type": str,
								"nargs": '?',
								"action": "store",
								"help": _("Padrón a descargar")
					},
					"--version -v": {
								"action":	"version",
								"version":	__version__,
								"help":		_("Mostrar el número de versión y salir")
					},
					"--show-padrones -s": {
								"action":	"store_true",
								"dest":		"showpadrones",
								"default":	False,
								"help":		_("Verifciación completa. c: algoritmos de compresión, e: algoritmos de encriptación.")
					},
					"--output-path -o": {
								"type": 	str,
								"action": 	"store",
								"dest": 	"outputpath",
								"default":	None,
								"help":		_("Carpeta de outputh del padrón descargado.")

					}
			}

	for key, val in opciones.items():
		args = key.split()
		kwargs = {}
		kwargs.update(val)
		cmdparser.add_argument(*args, **kwargs)

	return cmdparser


def get_UrlFromHref(pageurl, hreftext, domainoverride=None):

	response = requests.get(pageurl)
	parsed_uri = urlparse(pageurl)

	if domainoverride:
		domain = domainoverride
	else:
		domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

	url = None
	soup = BeautifulSoup(response.content, "html.parser")
	for a in soup.find_all('a', href=True):
		if a.string:
			if hreftext in a.string:
				if "http" not in a["href"] and "/" in a["href"]:
					url = domain + a['href']
				elif "http" in a["href"]:
					url = a["href"]

	return url


def show_padrones(available_padrones):

	tablestr = tabulate(
					tabular_data		= available_padrones,
					headers				= ["Padrón", "Descripción" ],
					tablefmt			= "psql",
					stralign			= "left",
					override_cols_align = ["right", "left"]
		)

	print(tablestr)


def normalizefn(text, delim='-'):
	"""Normaliza una cadena para ser usada como nombre de archivo.

	Args:
		text (str): String a normalizar
		delim (str): Caracter de reemplazo de aquellos no vÃ¡lidos

	Ejemplo:
		>>> from openerm.Utils import *
		>>> Start downloading file("Esto, no es vÃ¡lido como nombre de Archivo!", "-")
		'esto-no-es-valido-como-nombre-de-archivo'
	"""
	result = []
	for word in _punct_re.split(text):
		word = normalize('NFKD', word).encode('ascii', 'ignore')
		word = word.decode('utf-8')
		if word:
			result.append(word)
	return delim.join(result)


def download_file(url, filemask=None, outputfile=None):

	logging.info("Start downloading file")
	logging.info("Download url: {0}".format(url))
	logging.info("Filemask: {0}".format(filemask))

	local_filename = url.split('/')[-1]

	if filemask:
		result = re.match(filemask, local_filename)
		local_filename = normalizefn(result.group(0))

	if outputfile:
		local_filename = os.path.join(outputfile, local_filename)

	# Verificar filemask
	# si es valida  descargar sino salir

	chunk_size = 4096
	with open(local_filename, "wb") as f:

		print("Descargando {0}...".format(local_filename))
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None:  # no content length header
			f.write(response.content)
		else:
			total_length = int(total_length)

			num_bars = total_length / chunk_size
			bar = progressbar.ProgressBar(maxval=num_bars).start()
			i = 0
			for data in response.iter_content(chunk_size=chunk_size):
				f.write(data)
				bar.update(i)
				i += 1

			bar.finish()

	logging.info("Local file: {0}".format(local_filename))
	logging.info("Download succesful!")

	return local_filename


def Main():

	cmdparser = init_argparse()

	try:
		args = cmdparser.parse_args()
	except IOError as msg:
		args.error(str(msg))

	if args.outputpath:
		logfile = os.path.join(args.outputpath, 'padrondl.log')
	else:
		logfile = 'padrondl.log'

	logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y/%m/%d %I:%M:%S', filemode='w')

	config = ConfigParser()
	config.read_file(codecs.open("padrondl.cfg", "r", "utf8"))

	available_padrones = []

	for section_name in config.sections():

		if "padron:" in section_name:
			padron_id = section_name.split(":")[1]
			padron_name = config[section_name]["name"]
			available_padrones.append((padron_id, padron_name))

	if args.showpadrones and available_padrones:
		show_padrones(available_padrones)
		sys.exit(0)

	if args.padron:

		padrones = [p for p in available_padrones if p[0] == args.padron or args.padron == "all"]

		for p, n in padrones:

			# name		= Condiciones tributarias - Sin denominación
			# type		= href
			# domain 	= http://www.afip.gob.ar/genericos/cInscripcion/
			# url		= %(domain)s/archivoCompleto.asp
			# hreftext 	= Archivo condición tributaria sin denominación

			section		= "padron:" + p
			tipo 		= config[section]["type"]
			dominio 	= config[section]["domain"]
			url 		= config[section]["url"]
			hreftext	= config[section]["hreftext"]
			filemask	= config[section]["filemask"]

			logging.info("get url: {} | {} | {}".format(url, hreftext, dominio))
			if tipo == "href":
				fileurl = get_UrlFromHref(url, hreftext, dominio)
			else:
				fileurl = url

			if fileurl:
				try:
					download_file(fileurl, filemask, args.outputpath)
				except Exception as e:
					logging.error("%s error: %s" % (__appname__, str(e)))

	else:
		cmdparser.print_help()

if __name__ == "__main__":

	Main()
