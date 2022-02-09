from inspect import trace
import os
from robot.api import ExecutionResult
from .suiteResults import SuiteResults
from .azureTestPlansClient import AzureTestPlansClient
from .formatterPayloadAzure import FormatterPayloadAzure
from utils import *
from datetime import datetime
from .logger import logger
from .variables import VariablesBuiltIn
from .constants import *
from robot.api.deco import keyword,not_keyword
from robot.libraries.BuiltIn import BuiltIn
import traceback

class AzureTestsResultsKeywords:
    
    def __init__(self) -> None:
        self.azure_api = None
        self.output_dir = None
        self.url_project = None
        self.variablesBuiltIn=None

    @keyword
    def create_instance_azure_publisher(self,output_dir, url_project, token):
        self.output_dir = output_dir
        self.url_project = self.parseUrlProjectAPI(url_project)
        self.variablesBuiltIn=VariablesBuiltIn().getVariables()
        self.azure_api = AzureTestPlansClient(self.url_project, token)
        
    @keyword
    def publish_results_to_test_plan(self,result_xml_filename='output.xml') -> None:
        """Publish test results to their test plans by creating a run.
        You have to specify the folder that contains the test results and specialy the output.xml
        Exemples:
        ${run_id} = | Publish Results To Test Plan |
        ${run_id} = | Publish Results To Test Plan | results.xml 
        """
        try:
            path = os.path.join(self.output_dir,result_xml_filename)
            results = ExecutionResult(path)
            suitesresults = SuiteResults(self.output_dir)
            results = results.visit(suitesresults)

            for suite in suitesresults.suites:
                #Get the test cases based on their IDs injected in the test case tags
                testpoints = self.azure_api.get_tests_points(suitesresults.get_testcase_ids(suite))
                
                #Filter and let the test cases match the test plan and test suite concerned
                testpoints = [testpoint for testpoint in testpoints if (testpoint['testPlan']['id'] == str(suite['planId']) and testpoint['suite']['id'] == str(suite['id']))]
                
                if testpoints:
                #Build the content of the tests point to publish them
                    for testpoint in testpoints:
                        tc = suite['testcases'][str(testpoint['testCase']['id'])]
                        testpoint["status"] = STATUS_RBF[tc['status']]
                        testpoint['starttime'] = tc['starttime']
                        testpoint['endtime'] = tc['endtime']
                        testpoint['elapsedtime'] = tc['elapsedtime']
                        testpoint['critical'] = tc['critical']
                        testpoint['message'] = tc['message']
                        testpoint['name'] = tc['name']
                else:
                    raise Exception('There is no testpoints to pubblish outcomes')

                starttime_execution = datetime.strptime(suite['starttime'], "%Y%m%d %H:%M:%S.%f").isoformat()
                endtime_execution = datetime.strptime(suite['endtime'], "%Y%m%d %H:%M:%S.%f").isoformat()
                #Create run execution
                run = self.azure_api.create_run(suite['planId'], suite['name']+' '+str(self.variablesBuiltIn["environnement"]).upper(), starttime_execution, endtime_execution, self.variablesBuiltIn["username"])
                #Format payload to publish results
                payload = FormatterPayloadAzure.format_testresults_payload(testpoints)
                #Add Tests Results to run              
                results = self.azure_api.add_tests_results_to_run(run['id'], payload)
                self.azure_api.update_run(run['id'], {
                    "state": "Completed",
                    "comment": 
                        NEW_LINE+"JOB ID = "+self.variablesBuiltIn["job_id"] +
                        NEW_LINE+"JOB URL="+self.variablesBuiltIn["job_url"] +
                        NEW_LINE+"JOB NAME = "+self.variablesBuiltIn["job_name"] +
                        NEW_LINE+"ENVIRONNEMENT = "+self.variablesBuiltIn["environnement"],
                })
                return run['id']

        except Exception as ex:
            BuiltIn().fail(str(traceback.print_exc()))

    @keyword
    def add_screen_failure_to_test_result(self, run_id) -> None:
        """Attach the error screenshot to the ko test cases.

        Exemples:
        | Add Screen Failure To Test Result | ${run_id} |
        """       
        test_resutls = self.azure_api.get_results_run(run_id)
        for result in test_resutls['value']:
            if result['outcome'] == "Failed":
                file_path =self.output_dir+"/"+PREFIXE_SCREEN_ERROR+'_'+result["testCase"]["id"]+'_'+SUFIXE_SCREEN_ERROR+'.png'
                self.azure_api.add_attachement_to_testresult(run_id, result['id'],file_path)

    @keyword
    def add_report_to_run(self, run_id, dir_zip=False) -> None:
        """Attach report to run using run id
        Exemples:
        | Add Report To Run | ${run_id} |
        """  
        self.azure_api.add_attachement_to_run(run_id,self.output_dir,dir_zip)
    
    @keyword
    def add_attachement_to_testresult(self, run_id,test_result_id,file_path,comment="Capture Page Error") -> None:
        """Attach the error screenshot to the ko test cases.

        Exemples:
        | Publish Attachements To Test Result | ${run_id} |
        """       
        test_resutls = self.azure_api.get_results_run(run_id)
        self.azure_api.add_attachement_to_testresult(run_id,test_result_id, self.output_dir, file_path,comment)


    @keyword
    def add_attachement_to_run(self, run_id,attachement, dir_zip=False) -> None:
        """Attach the error screenshot to the ko test cases.

        Exemples:
        | Publish Attachements To Test Result | ${run_id} | ${OUTPUT DIR}
        """  
        self.azure_api.add_attachement_to_run(run_id,attachement,dir_zip)

    @keyword
    def get_test_results_run_by_id(self,run_id):
        return self.azure_api.get_results_run(run_id)
    
    @not_keyword
    def parseUrlProjectAPI(self,url):
        if str(url).endswith('/'): 
            return url+"_apis" 
        else :
             return url +"/_apis"
