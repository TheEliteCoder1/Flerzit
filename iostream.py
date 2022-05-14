import json, os

def load_json_data(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as sf:
            data = sf.read()
            sf.close()
        jsonified_data = json.loads(data)
        return jsonified_data
    else:
        return None

def save_json_data(json_file, data, overwrite=False):
    if overwrite == True:
        file=open(json_file, 'w').close()
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        if os.path.exists(json_file):
            file=open(json_file, 'w').close()
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            raise FileNotFoundError()