from genericpath import isdir
import requests
import json
import base64
from .variables import *
from .logger import logger
from requests.auth import HTTPBasicAuth
import shutil
from shutil import Error
import os
class AzureTestPlansClient:
    def __init__(self, azure_url_project, token, version='6.0-preview.2'):
        self.version = version
        self.azure_url_project = azure_url_project
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.authbasic=HTTPBasicAuth('',token)

    def get_tests_points(self, testcases):
        logger.info('\n'+str(self.__class__)+'get_tests_points')
        print(testcases)
        url = self.azure_url_project+"/test/points?api-version="+self.version
        payload = json.dumps({
            "PointsFilter": {
                "TestcaseIds": testcases
            }
        })
        response = requests.request(
            "POST", url, headers=self.headers,auth=self.authbasic, data=payload)
        print(response.content)
        return response.json()["points"]

    def get_testscases(self, testplandId, suiteId):
        url = self.azure_url_project+"/testplan/Plans/" + \
            str(testplandId)+"/Suites/"+str(suiteId) + \
            "/TestPoint/?api-version="+self.version
        response = requests.request("GET", url, headers=self.headers,auth=self.authbasic)

    def update_testspoints_outcomes(self, testplanId, suiteId, testspoints):
        print('\n', self.__class__, 'update_testspoints_outcomes')
        url = self.azure_url_project+"/testplan/Plans/"+testplanId + \
            "/Suites/"+suiteId+"/TestPoint?api-version="+self.version
        payload = json.dumps(testspoints)
        response = requests.request(
            "PATCH", url, headers=self.headers,auth=self.authbasic, data=payload)

    def create_run(self, planId, suite_name, starttime, endtime, run_by):
        logger.info('\n'+str(self.__class__)+'create_run')
        url = self.azure_url_project+"/test/runs?api-version=6.0"
        payload = json.dumps({
            "name": suite_name,
            "startDate": starttime,
            "completeDate": endtime,
            "state": "InProgress",
            "plan": {
                "id": planId,
                "url": self.azure_url_project.split("_apis")[0]+"_testPlans/define?planId="+str(planId)
            },
            "automated": True,
            "type": "NoConfigRun",
            "comment": "",
            "owner": {
                    "displayName": run_by
            }
        })
        response = requests.request(
            "POST", url, headers=self.headers,auth=self.authbasic, data=payload)
        print(response.json())
        print("RUN ID = ", response.json()['id'])
        print("RUN URL = ", response.json()['url'])
        return response.json()

    def add_tests_results_to_run(self, run_id, testresults, version=6.0):
        print('\n', self.__class__, 'add_tests_results')
        url = self.azure_url_project+"/test/runs/" + \
            str(run_id)+"/results?api-version="+str(version)
        payload = json.dumps(testresults)
        response = requests.request(
            "POST", url, headers=self.headers,auth=self.authbasic, data=payload)
        if str(response.status_code).startswith('4'):
            raise Exception(str(response)+"\t"+response.reason)
        return response.json()

    def update_run(self, run_id, payload, version=6.0):
        print('\n', self.__class__, 'update_run')
        url = self.azure_url_project+"/test/runs/" + \
str(run_id)+"?api-version="+str(version)
        payload = json.dumps(payload)
        response = requests.request(
            "PATCH", url, headers=self.headers,auth=self.authbasic,  data=payload)
        print(response.text)

    def get_results_run(self, run_id):
        url = self.azure_url_project+"/test/Runs/" + \
            str(run_id)+"/results?detailsToInclude=WorkItems,Iterations&api-version=6.0"
        response = requests.request("GET", url, headers=self.headers,auth=self.authbasic)
        return response.json()

    def add_attachement_to_testresult(self, run_id, test_result_id, filepath,comment):
        with open(filepath, "rb") as report:
            data = base64.b64encode(report.read())
        payload = json.dumps({
            "stream": str(data, 'utf-8'),
            "fileName": str(filepath).split("/")[-1],
            "comment":comment,
            "attachmentType": "GeneralAttachment"
        })
        response = requests.request("POST", self.azure_url_project+"/test/Runs/"+str(run_id)+"/Results/"+str(
            test_result_id)+"/attachments?api-version=6.0-preview.1", headers=self.headers,auth=self.authbasic, data=payload)

    def add_attachement_to_run(self, run_id, attachement_path, zip=False):
        stream = None
        if isdir(attachement_path):
            if not zip:
                shutil.make_archive("report", "zip", attachement_path)
            stream = self.convert_file_zip_to_base64("./report.zip")
            filename="report.zip"
        else :
            stream = self.convert_file_zip_to_base64(attachement_path)
            filename=os.path.basename(attachement_path)
        payload = json.dumps({
            "stream": str(stream, 'utf-8'),
            "fileName": filename,
            "comment": "Test Run attachment",
            "attachmentType": "GeneralAttachment"
        })
        try:
            endpoint = self.azure_url_project+"/test/Runs/" + \
                str(run_id)+"/attachments?api-version=6.0-preview.1"
            response = requests.request(
                "POST", endpoint, headers=self.headers, auth=self.authbasic,data=payload)
            print(response)
        except Error as error:
            print(error)

    def convert_file_zip_to_base64(self, report_zip):
        with open(report_zip, "rb") as report:
            data = base64.b64encode(report.read())
        return data