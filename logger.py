import json
import os

def create_log(file_name, file_type):
    '''Creates json file ({'files': [...]) or creates it if it's not here'''
    
    if 'result.json' in os.listdir():
        with open('result.json','r+') as f:
            data = json.load(f)
            data['files'].append({'file_name': file_name, 'size': file_type})
        with open('result.json','w') as f:
            json.dump(data, f)
    else:
        with open('result.json', 'x') as f:
            json.dump({'files': []}, f)
        create_log(file_name, file_type)
