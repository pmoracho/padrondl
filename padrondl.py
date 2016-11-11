#!/usr/bin/env python

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import requests
import progressbar

def getUrl(pageurl, hreftext):

	response = requests.get(pageurl)

	parsed_uri = urlparse(pageurl)
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
			dl = 0
			total_length = int(total_length)

			num_bars = total_length / chunk_size
			bar = progressbar.ProgressBar(maxval=num_bars).start()
			i = 0
			for data in response.iter_content(chunk_size=chunk_size):
				f.write(data)
				bar.update(i)
				i+=1

	return local_filename



url		 = "http://www.agip.gob.ar/agentes/agentes-de-recaudacion-e-informacion"
hreftext = "Padrón de Regímenes Generales"

fileurl = getUrl(url, hreftext)
print("Found the URL: {0}".format(fileurl))

download_file2(fileurl)
