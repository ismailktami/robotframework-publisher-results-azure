from robot.libraries.BuiltIn import BuiltIn

class VariablesBuiltIn:
    def __init__(self) -> None:
        self.USERNAME = BuiltIn().get_variable_value("${USERNAME}") or "USERNAME"
        self.JOB_URL = BuiltIn().get_variable_value("${JOB_URL}") or "JOB URL"
        self.JOB_NAME = BuiltIn().get_variable_value("${JOB_NAME}") or  "JOB_NAME"
        self.JOB_ID = BuiltIn().get_variable_value("${JOB_ID}") or "JOB_ID" 
        self.JOB_STARTED_TIME = BuiltIn().get_variable_value("${JOB_STARTED_TIME}") or "JOB_STARTED_TIME" 
        self.ENVIRONNEMENT = BuiltIn().get_variable_value("${ENVIRONNEMENT}") or "ENVIRONNEMENT" 
  