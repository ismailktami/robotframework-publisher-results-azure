from robot.libraries.BuiltIn import BuiltIn
import json
class VariablesBuiltIn:

    @staticmethod
    def getVariables():
        USERNAME = BuiltIn().get_variable_value("${USERNAME}") or "USERNAME"
        JOB_ID = BuiltIn().get_variable_value("${JOB_ID}") or "JOB_ID" 
        JOB_URL = BuiltIn().get_variable_value("${JOB_URL}") or "JOB URL"
        JOB_NAME = BuiltIn().get_variable_value("${JOB_NAME}") or  "JOB_NAME"
        JOB_STARTED_TIME = BuiltIn().get_variable_value("${JOB_STARTED_TIME}") or "JOB_STARTED_TIME" 
        ENVIRONNEMENT = BuiltIn().get_variable_value("${ENVIRONNEMENT}") or "ENVIRONNEMENT" 
        OUTPUT_DIR = BuiltIn().get_variable_value("${OUTPUT_DIR}") 

        return {"output_dir":OUTPUT_DIR,"username":USERNAME,"job_id":JOB_ID,"job_url":JOB_URL,"job_name":JOB_NAME,"job_started_time":JOB_STARTED_TIME,"environnement":ENVIRONNEMENT}
