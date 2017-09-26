
# Add new column with constant value to first resource
# Column name and value are taken from the processor's parameters
from datapackage_pipelines.wrapper import process
import requests
import os
import base64
import shutil


def modify_datapackage(datapackage, parameters, _):
    datapackage['resources'][0]['schema']['fields'].append({
      'name': parameters['local_image_column'],
      'type': 'string'
    })
    os.makedirs(
        parameters["local_path"],
        exist_ok=True
    )
    return datapackage


def download_image(url, path):
    resp = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, f)


def image_location(url):
    name, ext = os.path.splitext(url)
    newname = base64.b32encode(name.encode("utf-8")).decode("utf-8") + ext
    return newname


def process_row(row, _1, _2, resource_index, parameters, _):
    if resource_index == 0:
        url = row[parameters['remote_image-url']]
        new_location = image_location(
            url,
        )
        row[parameters['local_image_column']] = new_location
        download_image(url, os.path.join(parameters["local_path"], new_location))
    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row,)
