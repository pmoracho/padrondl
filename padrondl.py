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
	from urllib.parse import urlparse
	from bs4 import BeautifulSoup
	import requests
	import progressbar
	from configparser import ConfigParser
	import codecs

except ImportError as err:
	modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
	print(_("No fue posible importar el modulo: %s") % modulename)
	sys.exit(-1)

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
								"action": "store",
								"help": _("Padrón a descargar")
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
		print(domain)
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

def download_file(url):
	local_filename = url.split('/')[-1]
	print("Descargando {0}...".format(local_filename))
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				#f.flush() commented by recommendation from J.F.Sebastian
	return local_filename

def download_file2(url):

	local_filename = url.split('/')[-1]
	chunk_size = 4096
	with open(local_filename, "wb") as f:
		print("Descargando {0}...".format(local_filename))
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			total_length = int(total_length)

			num_bars = total_length / chunk_size
			bar = progressbar.ProgressBar(maxval=num_bars).start()
			i = 0
			for data in response.iter_content(chunk_size=chunk_size):
				f.write(data)
				bar.update(i)
				i+=1

	return local_filename

def	Main():

	cmdparser = init_argparse()
	try:
		args = cmdparser.parse_args()
	except IOError as msg:
		args.error(str(msg))


	parser = ConfigParser()
	parser.read_file(codecs.open("padrondl.cfg", "r", "utf8"))

	available_padrones=[]

	for section_name in parser.sections():
		# print('Section:', section_name)
		# print('  Options:', parser.options(section_name))

		if "padron:" in section_name:
			available_padrones.append(section_name.split(":")[1])

		# for name, value in parser.items(section_name):
		# 	print('  {} = {}'.format(name, value))
		# print()

	print(available_padrones)

	"""
	url		 = "http://www.agip.gob.ar/agentes/agentes-de-recaudacion-e-informacion"
	hreftext = "Padrón de Regímenes Generales"

	url		 = "http://www.afip.gob.ar/genericos/cInscripcion/archivoCompleto.asp"
	hreftext = "Archivo condición tributaria sin denominación"

	fileurl = getUrl(url, hreftext, )
	print("Found the URL: {0}".format(fileurl))

	download_file2(fileurl)
	"""

if __name__ == "__main__":

	Main()
