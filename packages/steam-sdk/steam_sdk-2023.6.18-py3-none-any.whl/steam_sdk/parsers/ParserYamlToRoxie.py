import yaml
import ruamel
class ParserYamlToRoxie:
    """
    This class is working as a helper to the RoxieParser. In some cases ex MED_C_COMB and MBRD, the windings are ambigous.
    Therefore the exact layers must be parsed through model_data.yaml files. Specifically the key:
     CoilWindings.electrical_pairs.group_together
    """
    def __init__(self, model_data_yaml_path: str = None):
        if model_data_yaml_path == None:
            print("No model_data.yaml path, ParserYamlToRoxie won't execute")
        else:
            self.model_data_yaml_path = model_data_yaml_path
            #self.__update_groups()

    def __update_groups(self):
        pass

    def read_model_data_yaml(self):
        with open(self.model_data_yaml_path, 'r') as stream:
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            yaml_str = yaml.load(stream)
            return yaml_str['CoilWindings']['electrical_pairs']['group_together']
