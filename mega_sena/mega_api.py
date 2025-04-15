import json
import os
import requests

class MegaAPI():

	def __init__(self, path_file):
		self.url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/"
		self.path_file = path_file
		self.results = []
		self.last_contest = 0

	def process_data(self):
		self.__validate_file()
		self.__get_result_mega()
		self.__save_results()

	def __validate_file(self):
		if os.path.exists(self.path_file):
			with open(self.path_file, "r") as file:
				self.results = json.load(file)
				if self.results:
					self.last_contest = max(r["concurso"] for r in self.results)

		self.last_contest += 1

	def __get_result_mega(self):

		while True:
			try:
				response = requests.get(self.url + str(self.last_contest))

				if response.status_code != 200:
					print(f"Erro ao acessar a API: {response.status_code}")
					break

				data = response.json()

				contest = {
					"concurso": data.get("numero"),
					"data": data.get("dataApuracao"),
					"dezenas": data.get("listaDezenas"),
					"ganhadores": {
						"ganhadores": int(data.get("listaRateioPremio", [])[0].get("quantidadeGanhadores", 0)),
						"valor": float(data.get("listaRateioPremio", [])[0].get("valorPremio", 0))
					}
				}

				self.results.append(contest)
				self.last_contest += 1

			except requests.exceptions.RequestException as e:
				print(f"Erro ao acessar a API: {e}")
				break

	def __save_results(self):
		with open(self.path_file, "w") as file:
			json.dump(self.results, file, indent=4)
		print(f"Resultados salvos em {self.path_file}")