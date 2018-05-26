import yaml
import os


def Config():
    current_path = os.path.abspath(os.path.dirname(__file__))
    path = current_path + '/config.yaml'
    with open(path, 'r', encoding='utf-8') as f:
        group = yaml.load(f.read())['group'][0]
    return group
