import shutil
import os
from Constants import URL_PROJECT
from zipfile import ZipFile
from os import path
from shutil import Error, make_archive
import base64
import requests
import json


class PublisherReport:
    def __init__(self):
        pass

    def publish(self, run_id, report_path, zip=False):
        if not zip:
            shutil.make_archive("report", "zip", report_path)
        stream = self.convert_report_zip_to_base64("./report.zip")
        payload = json.dumps({
            "stream": str(stream, 'utf-8'),
            "fileName": "rapport.zip",
            "comment": "Test attachment upload",
            "attachmentType": "GeneralAttachment"
        })
        headers = {
            'Authorization': 'Basic Omp1YXRzbnNuN3Foa25xcnFwbTdlZGM1dDZxdml1azJtM2I3NjQ1bHZzbXBzamlrc2E0cWE=',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", URL_PROJECT+"/test/Runs/"+str(
                run_id)+"/attachments?api-version=6.0-preview.1", headers=headers, data=payload)
            print(response)
        except Error as error:
            print(error)

    def convert_report_zip_to_base64(self, report_zip):
        with open(report_zip, "rb") as report:
            data = base64.b64encode(report.read())
        return data
