import os
from robot.api import ExecutionResult
from SuiteResults import SuiteResults
from AzureApiPlans import AzureApiPlans
from utils import *
from FormatterPayloadAzure import FormatterPayloadAzure
from Constants import *   
from datetime import datetime
from Logger import logger
from robot.api.deco import keyword,library
from Variables import *
@library(scope='GLOBAL', auto_keywords=True)
class PublisherAzureTestPlan:
    def __init__(self,output_dir,token,url_project) -> None:
        self.azure_api=AzureApiPlans(url_project,token)
        self.output_dir=output_dir
        self.url_project=url_project

    @keyword
    def publish_results(self) -> None:
        try:
            path = os.path.join(self.output_dir, 'output.xml')
            results = ExecutionResult(path)
            suitesresults = SuiteResults(self.output_dir)
            results = results.visit(suitesresults)
            for suite in suitesresults.suites:
                    testpoints=self.azure_api.get_tests_points(suitesresults.get_testcase_ids(suite))
                    testpoints=[testpoint for testpoint in testpoints if ( testpoint['testPlan']['id'] == str(suite['planId']) and testpoint['suite']['id'] == str(suite['id']))]
                    if testpoints:
                            for testpoint in testpoints:
                                    tc=suite['testcases'][str(testpoint['testCase']['id'])]
                                    testpoint['starttime']=tc['starttime']
                                    testpoint['endtime']=tc['endtime']
                                    testpoint['elapsedtime']=tc['elapsedtime']
                                    testpoint['critical']=tc['critical']
                                    testpoint['message']=tc['message']
                                    testpoint['name'] = tc['name']
                                    testpoint["status"] = STATUS_RBF[tc['status']]
                    else: 
                            raise Exception('There is no testpoints to pubblish outcomes')

                    endtime= datetime.strptime(suite['endtime'],"%Y%m%d %H:%M:%S.%f").isoformat()
                    starttime= datetime.strptime(suite['starttime'],"%Y%m%d %H:%M:%S.%f").isoformat()
                    run=self.azure_api.create_run(suite['planId'],suite['name']+' '+str(ENVIRONNEMENT).upper(),starttime,endtime,USERNAME)
                    payload=FormatterPayloadAzure.format_testresults_payload(testpoints)
                    results=self.azure_api.add_tests_results(run['id'],payload)
                    self.azure_api.update_run(run['id'],{
                    "comment": NEW_LINE+"JOB ID = "+JOB_ID+
                            NEW_LINE+"JOB URL="+JOB_URL+
                            NEW_LINE+"JOB NAME = "+JOB_NAME+
                            NEW_LINE+"ENVIRONNEMENT = "+ENVIRONNEMENT,
                    "state":"Completed"
                    })
                    
                    return run['id']

        except Exception as ex:
                logger.error("Publication de resultats AZURE KO : Exception :\n"+str(ex))   

    @keyword
    def publish_attachements_to_results(self,run_id) -> None:
        test_resutls=self.azure_api.get_results_run(run_id)
        for result in test_resutls['value']:
            if result['outcome']=="Failed":
                                    filename='ID-'+result["testCase"]["id"]+'_TEST_FAILED.png'
                                    self.azure_api.add_attachement_to_testresult(run_id,result['id'],self.output_dir,filename)
    @keyword
    def publish_report_to_run(self,run_id) -> None:
        self.azure_api.publish_report_to_run(run_id,self.output_dir)


