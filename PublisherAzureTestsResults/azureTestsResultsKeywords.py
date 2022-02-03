import os
from robot.api import ExecutionResult
from .suiteResults import SuiteResults
from .azureTestPlansClient import AzureTestPlansClient
from .publisherReport import PublisherReport
from .formatterPayloadAzure import FormatterPayloadAzure
from utils import *
from datetime import datetime
from .logger import logger
from .variables import VariablesBuiltIn
from .constants import *
from robot.api.deco import keyword,library

class AzureTestsResultsKeywords:
    def __init__(self) -> None:
        self.azure_api = None
        self.output_dir = None
        self.url_project = None
        self.variablesBuiltIn=None

    @keyword
    def get_instance(self,output_dir, url_project, token):
        self.azure_api = AzureTestPlansClient(url_project, token)
        self.output_dir = output_dir
        self.url_project = url_project
        self.variablesBuiltIn=VariablesBuiltIn()
        
    @keyword
    def publish_results_to_test_plan(self,output_dir=None,result_xml_filename='output.xml') -> None:
        """Publish test results to their test plans by creating a run.
        You have to specify the folder that contains the test results and specialy the output.xml
        Exemples:
        ${run_id} = | Publish Results To Test Plan |
        ${run_id} = | Publish Results To Test Plan   /reports/ |
        ${run_id} = | Publish Results To Test Plan | /reports/ | results.xml 
        """
        try:
            path = os.path.join(output_dir or self.output_dir,result_xml_filename)
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
                run = self.azure_api.create_run(suite['planId'], suite['name']+' '+str(self.variablesBuiltIn.ENVIRONNEMENT).upper(), starttime_execution, endtime_execution, self.variablesBuiltIn.USERNAME)
                
                #Format payload to publish results
                payload = FormatterPayloadAzure.format_testresults_payload(testpoints)
                
                #Add Tests Results to run              
                results = self.azure_api.add_tests_results_to_run(run['id'], payload)
                
                self.azure_api.update_run(run['id'], {
                    "comment": NEW_LINE+"JOB ID = "+self.variablesBuiltIn.JOB_ID +
                    NEW_LINE+"JOB URL="+self.variablesBuiltIn.JOB_URL +
                    NEW_LINE+"JOB NAME = "+self.variablesBuiltIn.JOB_NAME +
                    NEW_LINE+"ENVIRONNEMENT = "+self.variablesBuiltIn.ENVIRONNEMENT,
                    "state": "Completed"
                })
                return run['id']

        except Exception as ex:
            logger.error(
                "Publication de resultats AZURE KO : Exception :\n"+str(ex))

    @keyword
    def add_attachements_to_test_result(self, run_id) -> None:
        """Attach the error screenshot to the ko test cases.

        Exemples:
        | Publish Attachements To Test Result | ${run_id} |
        """       
        test_resutls = self.azure_api.get_results_run(run_id)
        for result in test_resutls['value']:
            if result['outcome'] == "Failed":
                filename = PREFIXE_SCREEN_ERROR+'_'+result["testCase"]["id"]+'_'+SUFIXE_SCREEN_ERROR+'.png'
                self.azure_api.add_attachement_to_testresult(run_id, result['id'], self.output_dir, filename)

    @keyword
    def add_attachements_to_run(self, run_id,directory, dir_zip=False) -> None:
        """Attach the error screenshot to the ko test cases.

        Exemples:
        | Publish Attachements To Test Result | ${run_id} |
        """  
        publisher=PublisherReport(self.token)
        publisher.publish(run_id,directory,dir_zip)
