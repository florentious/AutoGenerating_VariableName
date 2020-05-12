import json

fileName = 'config.json'


class Options:
    def __init__(self):
        jsonObj = json.loads(open(fileName, 'rb').read().decode('utf-8'))

        self.papago_api = jsonObj['papago_api']
        self.colab_base_path = jsonObj['colab_base_path']
        self.base_dictionary_path = jsonObj['base_dictionary_path']
        self.webdriver_path = jsonObj['webdriver_path']

        self.w2idx_model = jsonObj['w2idx_model']
        self.w2idx_embed = jsonObj['w2idx_embed']
        self.vocab_path = jsonObj['vocab_path']
        self.weight_path = jsonObj['weight_path']
        self.weight_name = jsonObj['weight_name']

        self.train_raw_path = jsonObj['train_raw_path']
        self.test_raw_path = jsonObj['test_raw_path']
        self.pos_raw_path = jsonObj['pos_raw_path']
        self.train_data_path = jsonObj['train_data_path']
        self.test_data_path = jsonObj['test_data_path']
        self.pos_data_path = jsonObj['pos_data_path']

        self.host_ip = jsonObj['host_ip']
        self.host_port = jsonObj['host_port']

        self.n_hidden = jsonObj['n_hidden']
        self.max_seq_len = jsonObj['max_seq_len']
        self.gpu_count = jsonObj['gpu_count']
        self.batch_size = jsonObj['batch_size']
