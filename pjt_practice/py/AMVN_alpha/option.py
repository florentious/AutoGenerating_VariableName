import json

fileName = 'config.json'


class Options:
    def __init__(self):
        category = json.loads(open(fileName, 'rb').read().decode('utf-8'))

        self.papago_api = category['papago_api']
        self.base_dictionary_path = category['base_dictionary_path']
        self.webdriver_path = category['webdriver_path']
