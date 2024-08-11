from utils.exception_util import ExceptionUtil

import yaml

class YamlUtil:

    @staticmethod
    def converter_yaml_para_dict(arquivo_yaml: str) -> dict:
        try:
            with open(file=arquivo_yaml, mode="r") as stream:
                return yaml.safe_load(stream)
        except Exception as e:
            raise e
