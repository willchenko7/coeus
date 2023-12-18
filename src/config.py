import json
import os

#see if config file exists
config_path = os.path.join('src','config.json')
if os.path.isfile(config_path):
    #read config file
    with open(config_path) as config_file:
        config = json.load(config_file)
else:
    raise Exception('Config file not found. Please create a config.json file in the src directory.')

#see if openai_api_key_path exists in config file
try:
    key_path = config['openai_api_key_path']
except:
    raise Exception('Config file must contain a key named openai_api_key_path.')

#see if openai_api_key_path exists
if os.path.isfile(key_path):
    with open(key_path) as key_file:
        keys = json.load(key_file)
        openai_key = keys['openai_api_key']
else:
    raise Exception('OpenAI API key not found. Please create a json file at the path specified in the config file.')