import PySimpleGUI as sg
import os
import json
from matrix_cloud import download_large_file, upload_large_file


def run_gui():
    default_username = ''
    default_password = ''
    default_matrix_url = 'matrix.org'

    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
            default_username = config["username"]
            default_password = config["password"]
            default_matrix_url = config["matrix_url"]

    layout = [[
        sg.Text('Username', size=(8, 1)),
        sg.Input(key="username", default_text=default_username)
    ],
              [
                  sg.Text('Matrix URL', size=(8, 1)),
                  sg.Input(key="matrix_url", default_text=default_matrix_url)
              ],
              [
                  sg.Text('Password', size=(8, 1)),
                  sg.Input(password_char="*",
                           key="password",
                           default_text=default_password)
              ],
              [
                  sg.Text('File name', size=(8, 1)),
                  sg.Input(key="file_name"),
                  sg.FileBrowse()
              ],
              [
                  sg.Text('Output file name', size=(8, 1)),
                  sg.Input(key="out_file_name", default_text=""),
                  sg.FileSaveAs()
              ],
              [
                  sg.Radio('Download', 1, default=True, key="download_choice"),
                  sg.Radio('Upload', 1, key="upload_choice")
              ], [sg.Button('Start')]]

    window = sg.Window('Matrix Cloud GUI', layout)
    input_values = window.read()
    if input_values == None:
        return
    _, values = input_values

    window.close()

    if values["download_choice"]:
        download_large_file(
            values["username"], values["password"], values["file_name"],
            values["matrix_url"],
            values["out_file_name"] if values["out_file_name"] != "" else None)

    if values["upload_choice"]:
        upload_large_file(values["username"], values["password"],
                          values["file_name"], values["matrix_url"],
                          values["out_file_name"])
