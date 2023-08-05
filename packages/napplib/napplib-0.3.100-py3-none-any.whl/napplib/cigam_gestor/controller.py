import requests
import json
import logging

from datetime import datetime
from typing import Union, Tuple

# ---- documentantion ---- #
# https://documenter.getpostman.com/view/1261739/TzCV45Kw#00658c24-e9c1-4b99-aad8-329b64c2d030

class CigamGestorController:

	@staticmethod
	def get_products(url: str, token: str, store: str, referencia: str = None):
		headers = dict()
		headers['Content-Type'] = 'application/json'
		headers['Authorization'] = f'Bearer {token}'

		params = dict()
		params['loja'] = store
		if referencia:
			params['referencia'] = referencia

		response = requests.get(f'http://{url}/Gestor.Api.IntegracaoHub/IntegracaoHub/product', headers=headers, params=params)

		if response.status_code != 200:
			logging.info(f"Error: {response.status_code} - {response.text}")

		try:
			response = response.json()
		except:
			raise Exception('Response returned is not a valid json\n' + response.content.decode('utf-8'))

		return response

	@staticmethod
	def get_stocks(url: str, token: str, store: str, referencia: str = None):
		headers = dict()
		headers['Content-Type'] = 'application/json'
		headers['Authorization'] = f'Bearer {token}'

		params = dict()
		params['loja'] = store
		if referencia:
			params['referencia'] = referencia

		response = requests.get(f'http://{url}/Gestor.Api.IntegracaoHub/IntegracaoHub/stock', headers=headers, params=params)

		if response.status_code != 200:
			logging.info(f"Error: {response.status_code} - {response.text}")

		try:
			response = response.json()
		except:
			raise Exception('Response returned is not a valid json\n' + response.content.decode('utf-8'))

		return response
		
	@staticmethod
	def get_prices(url: str, token: str, store: str, referencia: str = None):
		headers = dict()
		headers['Content-Type'] = 'application/json'
		headers['Authorization'] = f'Bearer {token}'

		params = dict()
		params['loja'] = store
		if referencia:
			params['referencia'] = referencia

		response = requests.get(f'http://{url}/Gestor.Api.IntegracaoHub/IntegracaoHub/price', headers=headers, params=params)

		if response.status_code != 200:
			logging.info(f"Error: {response.status_code} - {response.text}")

		try:
			response = response.json()
		except:
			raise Exception('Response returned is not a valid json\n' + response.content.decode('utf-8'))

		return response



