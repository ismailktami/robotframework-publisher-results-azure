
class YourLibrary(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self._path_to_report = BuiltIn().get_variable_value('${REPORT_FILE}')

    def _close(self):
        self.call_your_method_to_send_the_report(self._path_to_report)


from robot.api import logger

def log_to_console(arg):
   logger.console('Got arg %s' % arg)

def log_to_console_and_log_file(arg):



