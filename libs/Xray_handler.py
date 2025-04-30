import requests
import json, os, warnings, logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv

class Xray_data_collector ():
    def __init__ (        
        self, 
        base_url,
        authentication_token,
        api_version = "latest", 
        session = None,
        headers = None,
        timeout = 120):
        '''
        base_url : URL to which a rest api session has to be created
        authentication_token : Bearer token for authentication
        api_version (optional) : version of api
        session (optional) : A request session if already existing
        headers (optional) : Header to be updated
        '''

        self.base_url = base_url
        self.api_root = "rest/raven"
        self.api_version = "1.0/api"
        self.timeout = timeout
        if (session is None):
            self.session = requests.Session()
        else:
            self.session = session
        headers = {'Authorization': 'Bearer '+authentication_token, 
                   'Content-Type': 'application/json'}
        self.session.headers.update(headers)
        warnings.filterwarnings('ignore', category=InsecureRequestWarning)


    def resource_url(self, resource, base_url=None, api_root=None, api_version=None):
        '''
        params
            -resource : resource to which the url has to be generated 
             E.g. archive, search, field
        Returns resource url as per REST api documentation
                   following rest/api/{api_version}/
        '''
        if base_url is None:
            base_url = self.base_url
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return "/".join(str(s).strip("/") \
            for s in [base_url, api_root, api_version, resource] if s is not None)

    def get_tests_from_test_executions(self, test_executions_list: list):
        '''
        params: 
        - test_executions_list : List of the TMX IDs of the test execution
        Returns:  List of all tests with status as a dictionary of list of tests
        '''
        testexecutions = {}
        for testExecKey in test_executions_list:
            url = self.resource_url (f"testexec/{testExecKey}/test")
            test_exec_results = self.session.get (url, params = {'detailed': 'True'})
            if test_exec_results.status_code == 200:
                test_exec_results = test_exec_results.json()
            else:
                test_exec_results = {}
            testExec = {}
            for item in test_exec_results:
               testExec[item['key']] = item ['status']
            testexecutions[testExecKey] = testExec
        return testexecutions

    def __del__ (self):
        self.session.close()
        del(self)


              