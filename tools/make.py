# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# make.py
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

__author__		= "Patricio Moracho <pmoracho@gmail.com>"
__appname__		= "make.py"
__projectname__	= "parsedl"
__appdesc__		= "Automatización de tareas para el proyecto {0}".format(__projectname__)
__license__		= 'GPL v3'
__copyright__	= "(c) 2016, %s" % (__author__)
__version__		= "0.9"
__date__		= "2016/07/14"

packages 		= {
				"requests":	("2.11.1",	None),
			  	"progressbar2": ("3.11.0",	None),
			  	"beautifulsoup4": ("4.5.1",	None),
				"PyInstaller":	("3.1.1",	None)
}
manualtasks 	= []
tools 			= ["padrondl.py"]

try:
	import gettext
	from gettext import gettext as _
	gettext.textdomain(__projectname__)

	def my_gettext(s):
		"""my_gettext: Traducir algunas cadenas de argparse."""
		current_dict = {'usage: ': '',
						'optional arguments': 'argumentos opcionales',
						'show this help message and exit': 'mostrar esta ayuda y salir',
						'positional arguments': 'argumentos posicionales',
						'the following arguments are required: %s': 'los siguientes argumentos son requeridos: %s'}

		if s in current_dict:
			return current_dict[s]
		return s

	gettext.gettext = my_gettext

	import sys
	import subprocess
	import re
	import argparse
	from argparse import RawTextHelpFormatter
	import textwrap

except ImportError as err:
	modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
	print(_("No fue posible importar el modulo: %s") % modulename)
	sys.exit(-1)


def subprocess_cmd(command):
	process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
	stdout_value, stderr_value = process.communicate()
	if stderr_value:
		return stderr_value.decode("Latin1")
	if stdout_value:
		return stdout_value.decode("Latin1")

class MyMake(object):

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			prog=__appname__,
			description="",
			epilog="",
			# add_help=False,
			formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
			usage='''%s\n%s\n

Uso: make <command> [<args>]

Los comandos más usados:
   devcheck   Hace una verificación del entorno de desarrollo
   devinstall Realiza la instalación del entorno de desarrollo virtual e instala los requerimientos
   docinstall Intalación de Sphinx
   clear      Elimina archivos innecesarios
   test	      Ejecuta todos los tests definidos del proyecto
   build      Construye la distribución binaria de las herramientas del proyecto

''' % (__appdesc__, __copyright__)
		)
		self.parser.add_argument('command', help='Comando a ejecutar')
		# parse_args defaults to [1:] for args, but you need to
		# exclude the rest of the args too, or validation will fail
		args = self.parser.parse_args(sys.argv[1:2])
		if not hasattr(self, args.command):
			self.print_error()
			exit(1)
		# use dispatch pattern to invoke method with same name
		getattr(self, args.command)()

	def test(self):
		self.parser = argparse.ArgumentParser(description='Ejecuta todos los tests del proyecto')
		print("Running make tests")
		self.run_tests()

	def build(self):
		self.parser = argparse.ArgumentParser( description='Ejecuta todos los tests del proyecto')
		print("Running make build")
		self.build_tools(tools)

	def devinstall(self):
		self.parser = argparse.ArgumentParser( description='Realiza la instalación del entorno de desarrollo virtual e instala los requerimientos')
		print("Running make devinstall")
		self.dev_install()
		self.run_devcheck()

	def docinstall(self):
		self.parser = argparse.ArgumentParser( description='Realiza la instalación de Sphinx el documentador')
		print("Running make docinstall")
		self.doc_install()

	def devcheck(self):
		self.parser = argparse.ArgumentParser( description='Hace una verificación del entorno de desarrollo')
		print("Running make devcheck")
		self.run_devcheck()

	def print_error(self):
		self.parser.print_help()
		print('\nError: Comando desconocido\n')

	def run_tests(self, msg=True, debug=False):

		if msg:
			print("----------------------------------------------------------")
			print("Running tests..")
			print("----------------------------------------------------------")

		command = "venv\\Scripts\\activate.bat & python tests\\runtests.py"
		ret = subprocess_cmd(command)

		if debug:
			print("run: {0}".format(command))
			print("ret: {0}".format(ret))

		if msg:
			print(ret)

	def doc_install(self, msg=True, debug=False):
		"""Instalación del entorno de documetación Sphinx

		Args:
			msg (bool)		: Muestra los mensajes
			debug: (bool)	: Muestra info adicional de la ejecución
		"""
		if msg:
			print("----------------------------------------------------------")
			print("Instalando Sphinx..")
			print("----------------------------------------------------------")

		command = "venv\\Scripts\\activate.bat &" + "pip install sphinx & pip install solar-theme"
		ret = subprocess_cmd(command)


	def dev_install(self, msg=True, debug=False):
		"""Instalación del entorno de desarrollo en el proyecto

		Args:
			msg (bool)		: Muestra los mensajes
			debug: (bool)	: Muestra info adicional de la ejecución
		"""

		if msg:
			print("----------------------------------------------------------")
			print("Creando el entorno virtual para desarrollo..")
			print("----------------------------------------------------------")

		#=================================
		# Instalación del entorno Virtual
		#=================================
		if not self.check_virtualenv(False, False):
			if msg:
				print("Creando entorno virtual con virtualenv...")

			command = "virtualenv venv"
			ret = subprocess_cmd(command)

			if not self.check_virtualenv(False, False):
				if msg:
					print("Error: No se ha podido instalar y activar el entorno virtual!!!")
			else:
				if msg:
					print("El entorno virtual se instaló correctamente...")
		else:
			if msg:
				print("El entorno virtual ya existe y está operativo...")


		status	= self.check_packages(packages, msg=False, debug=False)
		command = ""

		# Primero los paquetes que se pueden instalar via pip
		for i in [i for i in status if not i[2] and i[3] != "ok"]:
			command = command + ' & pip install {0} {1}'.format(("-U" if i[3]=="upgrade" else ""),i[0])

		# Luego paquetes que se instaland del wheel que ya está en proyecto
		for i in [i for i in status if i[2] and i[3] != "ok"]:
			command = command + ' & pip install wheels\\{0}'.format(i[2])

		if msg:
			print("Instalando requerimientos...")

		command = "venv\\Scripts\\activate.bat &" + "python -m pip install --upgrade pip" + command
		ret = subprocess_cmd(command)

		if debug and msg:
			print("run: {0}".format(command))
			print("ret: {0}".format(ret))

		if manualtasks:
			if msg:
				print("\n")
				print("---------------------------------------------------------")
				print("Atención, No olvidar las siguientes tareas manuales:\n")
				for i,t in enumerate(manualtasks,1):
					print(textwrap.fill("{0}. {1}".format(i,t),60))
				print("---------------------------------------------------------")
				print("\n")

	def check_virtualenv(self, msg=True, debug=False):
		"""Verifica la activación del entorno virtual del proyecto, ejecutando el activate.bat

		Args:
			msg (bool)		: Muestra los mensajes
			debug: (bool)	: Muestra info adicional de la ejecución

		Return:

			(bool) True si el entorno ha podido ser activado

		"""
		command = "venv\\Scripts\\activate.bat & python -c """""import sys;print(sys.prefix)"""""
		ret = subprocess_cmd(command)

		if debug and msg:
			print("run: {0}".format(command))
			print("ret: {0}".format(ret))

		if "\\venv" in ret:
			if msg:
				print("Activación de virtualenv Ok..")
			return True
		else:
			if msg:
				print("Error: imposible activar entorno virtual!!")
			return False

	def check_packages(self, packages, msg=True, debug=False):

		packages_status = []

		command = "venv\\Scripts\\activate.bat&pip freeze"
		ret = subprocess_cmd(command)

		if debug and msg:
			print("run: {0}".format(command))
			print("ret: {0}".format(ret))

		found = {}
		for l in ret.split():
			if "==" in l:
				p = l.split("==")
				found[p[0]] = p[1]

		for k,v in packages.items():
			ver = found.get(k,None)
			if not ver:
				if msg:
					print("{0} Not found!!".format(k))
				packages_status.append( (k, v[0], v[1], "install") )
			else:
				if ver < v[0]:
					if msg:
						print("{0} found invalid version!! (actual: {1} requiered {2}".format(k,ver,v[0]))
					packages_status.append( (k, v[0], v[1], "upgrade") )
				else:
					if msg:
						print("{0} {1} Ok..".format(k,ver))
					packages_status.append( (k, v[0], v[1], "ok") )

		return	packages_status

	def check_tool(self, tool, command, find, debug=False):

		ret = subprocess_cmd(command)

		if debug:
			print("run: {0}".format(command))
			print("ret: {0}".format(ret))

		if find in ret:
			print("{0} Ok..".format(tool))
		else:
			print("{0} Not found!!".format(tool))


	def clean(self, pattern, debug=False):

		import os, re, os.path
		mypath = "."
		for root, dirs, files in os.walk(mypath):
			for file in filter(lambda x: re.match(pattern, x), files):
				os.remove(os.path.join(root, file))

	def build_tools(self, tools, msg=True, debug=False):

		if msg:
			print("----------------------------------------------------------")
			print("Building..")
			print("----------------------------------------------------------")

		for tool in tools:

			command = "venv\\Scripts\\activate.bat & pyinstaller {0} --onefile	-p venv/Lib/site-packages/".format(tool)
			ret = subprocess_cmd(command)

			if debug and msg:
				print("run: {0}".format(command))
				print("ret: {0}".format(ret))

			if ".exe" in ret:
				if msg:
					print("Build {0} Ok..".format(tool))

	def run_devcheck(self, msg=True, debug=False):

		#########################################################################################
		# Verificar de las herramientas requeridas
		#########################################################################################
		if msg:
			print("----------------------------------------------------------")
			print("Check for required tools..")
			print("----------------------------------------------------------")

		self.check_tool("Python 3.4", "python --version", "Python 3.4")
		self.check_tool("Virtualenv", "pip freeze", "virtualenv")

		#########################################################################################
		# Verificar packages dentro del entorno virtual
		#########################################################################################
		if msg:
			print("----------------------------------------------------------")
			print("Check for required packages in Virtualenv..")
			print("----------------------------------------------------------")
		if self.check_virtualenv():
			self.check_packages(packages)


if __name__ == "__main__":
	MyMake()
