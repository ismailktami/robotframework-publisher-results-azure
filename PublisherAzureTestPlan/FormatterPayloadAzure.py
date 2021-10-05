from itertools import groupby
from operator import itemgetter
from Constants import *   

class FormatterPayloadAzure:
    def __init__(self):
        pass    

    @staticmethod
    def format_testpoint(testpoints):
        return [{"id": testpoint['id'], 'planId':testpoint['testPlan']['id'],'suiteId':testpoint['suite']['id'],'status':testpoint['status']} for testpoint in testpoints]

    @staticmethod
    def update_status_testcases(testpoints,outcomes):
        for testpoint in testpoints:
           testpoint['status']=STATUS_RBF[outcomes[testpoint['testCase']['id']]]
        return testpoints
        
    @staticmethod
    def format_testpoint_payload(testpoint):
        print(testpoint)
        return {"id": testpoint['id'], "results": {"outcome": testpoint['status']}}

    @staticmethod
    def format_payload_update_testspoints(testpoints,outcomes):
        testpoints=FormatterPayloadAzure.update_status_testcases(testpoints,outcomes)
        testpoints=FormatterPayloadAzure.format_testpoint(testpoints)
        tests = sorted(testpoints, key = itemgetter('planId','suiteId'))
        outcomes={}
        for key, value in groupby(tests,key =itemgetter('planId','suiteId')):
            outcomes[key]=[FormatterPayloadAzure.format_testpoint_payload(k) for k in value]
        return outcomes

    @staticmethod
    def format_payload_create_runs(suites):
        for suite in suites:
            testpoints=FormatterPayloadAzure.update_status_testcases(testpoints,outcomes)
            testpoints=FormatterPayloadAzure.format_testresult_payload(testpoints)
            tests = sorted(testpoints, key = itemgetter('planId','suiteId'))
            outcomes={}
            for key, value in groupby(tests,key =itemgetter('planId','suiteId')):
                outcomes[key]=[FormatterPayloadAzure.format_testpoint_payload(k) for k in value]
        return outcomes
    
    @staticmethod
    def format_testresults_payload(testresults):
        return [{
                "AutomatedTestName": testresult['name'],
                "comment": "",
                "createdDate": "",
                "completedDate": "",
                "durationInMs": float(testresult['elapsedtime']),
                "errorMessage": testresult['message'],
                "owner": testresult['assignedTo'],
                "runBy": {
                    "displayName": "Ismail Ktami"
                },
                "state": "Completed",
                "testCaseTitle": testresult['name'],
                "testCase": testresult['testCase'],
                "testPoint": {
                    "id": testresult['id']
                },
                "testPlan": testresult['testPlan'],
                "priority": 1,
                "outcome": testresult['status'],
                "testCaseRevision": 1
            }
            for testresult in testresults
        ]
            