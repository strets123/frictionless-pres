import ijson
import os

with open(os.path.join(os.path.dirname(__file__), '../data/smdataset?page[number]=0')) as f:
    for prefix, event, value in ijson.parse(f):
        if event in ('string', 'number', 'boolean', 'null'):
            print(prefix)
            print(str(value)[:100])
            print("===================")