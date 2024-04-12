import json
import traceback
import sys


class Utils:
    def load_config(conf_path):
        if conf_path is None or conf_path == '':
            raise Exception('Archivo de Configuración no puede ser Nulo')

        with open(conf_path) as f_in:
            json_str = f_in.read()
            return json.loads(json_str)
