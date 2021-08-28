import json
def load_config(conf_file):
    with open (conf_file, 'r') as f:
        cf = json.load(f)
    return cf