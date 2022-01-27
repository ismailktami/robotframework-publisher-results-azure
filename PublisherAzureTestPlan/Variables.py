from robot.libraries.BuiltIn import BuiltIn

USERNAME = BuiltIn().get_variable_value("${USERNAME}")
JOB_URL = BuiltIn().get_variable_value("${JOB_URL}") or "JOB URL"
JOB_NAME = BuiltIn().get_variable_value("${JOB_NAME}") or  "JOB_NAME"
JOB_ID = BuiltIn().get_variable_value("${JOB_ID}") or "JOB_ID" 
JOB_STARTED_TIME = BuiltIn().get_variable_value("${JOB_STARTED_TIME}") or "JOB_STARTED_TIME" 
ENVIRONNEMENT = BuiltIn().get_variable_value("${ENVIRONNEMENT}") or "ENVIRONNEMENT" 

