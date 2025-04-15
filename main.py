
import os
from mega_sena.mega_api import MegaAPI

ARQUIVO_JSON = "data/mega_sena.json"

class MegaSenaCollector:

	def run(self):
		process = MegaAPI(os.path.abspath(ARQUIVO_JSON))
		process.process_data()


if __name__ == "__main__":
	collector = MegaSenaCollector()
	collector.run()
