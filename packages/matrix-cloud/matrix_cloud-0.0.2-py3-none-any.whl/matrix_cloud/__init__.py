# SPDX-FileCopyrightText: 2023-present Filip Strajnar <filip.strajnar@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from simple_matrix_api.client import Client
import simple_matrix_api
from typing import Union
import json
from os import path

READ_SIZE = 50_000_000


def upload_large_file(username: str, password: str, file_path: str,
                      matrix_url: str, out_file: Union[str, None]):
    if not path.isfile(file_path):
        print("Argument file_path doesn't represent a file.")
        return

    client: Union[Client,
                  None] = simple_matrix_api.login(username, password,
                                                  matrix_url)
    if client == None:
        return
    urls: list[str] = []

    with open(file_path, "rb") as input:
        while True:
            content = input.read(READ_SIZE)
            if (len(content) == 0):
                break
            urls.append(client.upload("_", content))

    file_name = path.basename(file_path)
    json_path = f"{file_name}.json"
    with open(json_path if out_file == None else out_file, "w") as output:
        json.dump({"file_name": file_name, "urls": urls}, output)


def download_large_file(username: str, password: str, file_path: str,
                        matrix_url: str, out_file: Union[str, None]):
    if not path.isfile(file_path):
        print("Argument 'file_path' doesn't represent a file.")
        return

    if not file_path.endswith(".json"):
        print(
            "Warning: file_path expects json, but file doesn't end with '.json'."
        )

    client: Union[Client,
                  None] = simple_matrix_api.login(username, password,
                                                  matrix_url)

    if client == None:
        return

    with open(file_path, "r") as input:
        json_data = json.load(input)
        with open(json_data["file_name"] if out_file == None else out_file,
                  "wb") as output:
            for url in json_data["urls"]:
                content_part = client.get_file(url)
                if content_part != None:
                    output.write(content_part)
