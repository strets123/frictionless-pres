
# Add new column with constant value to first resource
# Column name and value are taken from the processor's parameters
from datapackage_pipelines.wrapper import process
import requests
import os
import base64
import shutil
import urllib3


def modify_datapackage(datapackage, parameters, _):
    # Initially we update the datapackage to include a local field name
    datapackage['resources'][0]['schema']['fields'].append({
      'name': parameters['local_image_column'],
      'type': 'string'
    })
    # Ensure the path to the images exists
    os.makedirs(
        parameters["local_path"],
        exist_ok=True
    )
    return datapackage


def download_image(url, path):
    """
    Download an image from a url and save to disk
    :param url: Remote url
    :param path: path to save to
    :return:
    """
    if not os.path.exists(path):
        if url:
            try:
                resp = requests.get(url, stream=True, timeout=5)
                with open(path, 'wb') as f:
                    resp.raw.decode_content = True
                    shutil.copyfileobj(resp.raw, f)
            except urllib3.exceptions.ReadTimeoutError:
                pass


def image_location(url):
    """
    Generate a name for a downloaded image
    :param url: url the image came from
    :return:
    """
    name, ext = os.path.splitext(url)
    newname = base64.b32encode(name.encode("utf-8")).decode("utf-8") + ext
    return newname


def process_row(row, _1, _2, resource_index, parameters, _):
    """
    Function which processes a row of data
    :param row: A python list representing the row of data
    :param _1:
    :param _2:
    :param resource_index:
    :param parameters: The dictionary of parameters passed to the script from pipeline-spec.yaml
    :param _:
    :return:
    """
    if resource_index == 0:
        url = row[parameters['remote_image-url']]
        if url is not None:
            new_location = image_location(
                url,
            )
            row[parameters['local_image_column']] = new_location
            full_url = parameters["base_url"] + url
            download_image(full_url, os.path.join(parameters["local_path"], new_location))
    return row


process(modify_datapackage=modify_datapackage,
        process_row=process_row,)
