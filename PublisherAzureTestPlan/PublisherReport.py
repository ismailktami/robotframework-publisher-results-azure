from Constants import URL_PROJECT
import shutil
from shutil import Error
import base64
import requests
import json

class PublisherReport:

    def __init__(self,token):
      self.token=token
      self.headers = {
          'Authorization':token,
          'Content-Type': 'application/json'
        }

    @staticmethod
    def publish(self,run_id,report_path,zip=False):
        if not zip:
            shutil.make_archive("report","zip",report_path)
        stream=self.convert_report_zip_to_base64("./report.zip")
        payload = json.dumps({
          "stream": str(stream,'utf-8'),
          "fileName": "rapport.zip",
          "comment": "Test attachment upload",
          "attachmentType": "GeneralAttachment"
        })
        try:
          endpoint=URL_PROJECT+"/test/Runs/"+str(run_id)+"/attachments?api-version=6.0-preview.1"
          response = requests.request("POST",endpoint, headers=self.headers, data=payload)
          print(response)
        except Error as error:
          print(error)

    @staticmethod
    def convert_report_zip_to_base64(self,report_zip):
        with open(report_zip, "rb") as report:
            data = base64.b64encode(report.read())
        return data        


