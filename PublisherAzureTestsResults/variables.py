from robot.libraries.BuiltIn import BuiltIn
import json
class VariablesBuiltIn:

    @staticmethod
    def getVariables():
        USERNAME = BuiltIn().get_variable_value("${USERNAME}") or "USERNAME"
        ENVIRONNEMENT = BuiltIn().get_variable_value("${ENVIRONNEMENT}") or "ENVIRONNEMENT" 
        JOB_ID = BuiltIn().get_variable_value("${JOB_ID}") or "" 
        JOB_URL = BuiltIn().get_variable_value("${JOB_URL}") or ""
        JOB_NAME = BuiltIn().get_variable_value("${JOB_NAME}") or  ""
        OUTPUT_DIR = BuiltIn().get_variable_value("${OUTPUT_DIR}") 

        return {"output_dir":OUTPUT_DIR,"username":USERNAME,"job_id":JOB_ID,"job_url":JOB_URL,"job_name":JOB_NAME,"environnement":ENVIRONNEMENT}
