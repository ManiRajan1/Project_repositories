from libs.Jira_handler import jira_data_collector
from libs.DNG_handler import dng_data_collector
from libs.Xray_handler import Xray_data_collector
import re, sys, json, logging
from os import getenv
from jinja2 import Template
from datetime import datetime
'''
This implementation can be directly replaced into the projects using the below tools for SWE.6:
    Software Requirement Management :  DOORS Next Gen
    System Requirement Management and Planning : JIRA
    Test Management :  JIRA+XRAY
    Defect Management : JIRA
Refer to libraries to understand how the APIs are handled:
    - Jira_handler 
    - Xray_handler 
    - DNG_handler
'''

class TestTraceabilityMapper:
    """
    A class to aggregate, map, and analyze traceability data for SWE.6
    Tools used : 
        - requirement management (DOORS NG),
        - Issue tracking (JIRA)
        - Test management systems (JIRA + Xray).

    This class performs the following operations:
    - Collects System requirements planned on a specific SW release from JIRA
    - Gathers linked software requirements for the system 
    - Maps software requirements to associated tests stored in DOORS
    - Retrieves execution data from Xray and links test executions to test cases
    - Computes and returns a full traceability matrix for reporting and analytics
    """

    def __init__ (self, url, auth, release_id = None, logger = None):
        #### Creating an Object that connects to JIRA via REST API
        self.jiraObj = jira_data_collector(url, auth)
        ### The collection of data from Doors Next Gen is handled by using the report builder function
        ### However based on the project authorisation RRA (Reportable Rest API can be used)
        self.dngObj = dng_data_collector("Requirements_report.xlsx")
        #### Creating an object that connects to xray via Rest API
        self.XrayObj = Xray_data_collector (url, auth)

        if logger == None:
            logging.basicConfig(
            filename="./temp/report.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filemode="w")           
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    def get_System_requirements(self):
        self.logger.info ("Getting information on system_reqs releated to Release Version")
        system_reqs = self.jiraObj.issue_Filter_by_jql(f"project='GENERIC' AND version={self.release_id} ORDER BY priority ASC")
        return system_reqs

    def get_SW_reqs(self, system_reqs=None):
        self.logger.info ("Getting information on SW_requirments Linked to system_reqs")
        System_requirement_keys = [f['key'] for f in system_reqs]
        SW_Reqs = self.jiraObj.get_remote_links_for_list_of_items(System_requirement_keys, link_type="generic_link")
        return SW_Reqs

    def get_SW_req_matrix (self, SW_Req_matrix ):   
        self.logger.info ("Completing the Test Matrix from requirements to Tests")    
        for req_id, req_data in SW_Req_matrix.items():
            if isinstance(req_data, dict):
                for id_key, id_data in req_data.items():
                    if isinstance(id_data, dict):
                        url = id_data.get('url')
                        #### SW requirement objects in DOORS NG require a URL and their global config to be extracted.
                        #### Reference : https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors-next/7.0.3?topic=reporting-reportable-rest-api
                        url = self.dngObj.resource_url(req_URL=url, global_config="XXX")
                        url = url[3]
                        if url:
                            test_cases_dict = self.dngObj.get_linked_issue_IDs(url, link_type="generic_test_link")
                            test_cases = test_cases_dict.get('Tests', [])
                            id_data['tests'] = test_cases if test_cases else None
        return SW_Req_matrix

    def get_test_information_from_SW_Req_matrix (self, SW_Req_matrix):
        tests = []
        for Function, Func_Data in SW_Req_matrix.items():
            for Req, Req_Data in Func_Data.items():
                if Req_Data['tests']:
                    tests += Req_Data['tests']
        return tests

    def get_test_executions(self):
        self.logger.info ("Getting information of test executions related to the tests")
        ### version is a default field within JIRA which is used to tag the Releases
        ### Issue types Test, Test Execution are supported by Xray and can be integrated to JIRA
        jql_query = f"project = 'GENERIC' AND issuetype = 'Test Execution' AND version='{self.release_id}' AND status = Approved"
        test_executions = self.jiraObj.issue_Filter_by_jql(jql_query)

        if test_executions:
            test_executions = self.jiraObj.field_map_response(test_executions)

        self.test_executions = {
            issue["key"]: {
                'resolution_date': issue["fields"].get("Resolved"),
                'Test Activity': issue["fields"].get("Test Activity"),
                'Leading-Team': issue["fields"].get("Leading-Team"),
                'SW Bundle' : issue["fields"].get("SW Bundle"),
                'test_data': {}
            }
            for issue in test_executions
        }

        test_execution_keys = list(self.test_executions.keys())
        test_execution_testdata = self.XrayObj.get_tests_from_test_executions(test_execution_keys)

        for key in self.test_executions:
            self.test_executions[key]['test_data'] = test_execution_testdata.get(key, {})

    def map_tests_and_test_executions (self, Sw_Reqs_Matrix_Tests):
        self.logger.info(f"Mapping the tests to latest test execution results for {self.release_id}")
        test_executions = self.test_executions
        tests = self.get_test_information_from_SW_Req_matrix(Sw_Reqs_Matrix_Tests) 
        test_matrix = {}

        for test_id in tests:
            latest_data = None
            latest_date = None
            for key, value in test_executions.items():
                if test_id in list(value['test_data'].keys()):
                    resolution_date = datetime.strptime(value['resolution_date'], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if latest_date is None or resolution_date > latest_date:
                        latest_date = resolution_date
                        latest_data = {
                            "Test_Execution_Key": key,
                            "resolution_date": value['resolution_date'],
                            "status": value['test_data'][test_id]
                        }
            test_matrix[test_id] = latest_data
        test_matrix_keys = list(test_matrix.keys())

        for function_id, function_details in Sw_Reqs_Matrix_Tests.items():
            for req_id, req_details in function_details.items():
                if 'tests' in req_details and req_details['tests'] is not None:
                    updated_tests = {}
                    for test in req_details['tests']:
                        if test in test_matrix_keys:
                            updated_tests[test] = test_matrix[test]
                    Sw_Reqs_Matrix_Tests[function_id][req_id]['tests'] = updated_tests

        return Sw_Reqs_Matrix_Tests

    def get_data (self):
        system_reqs = self.get_System_requirements()
        SW_Reqs_Matrix = self.get_SW_reqs(system_reqs)
        self.get_test_executions()
        del(self.jiraObj)
        del(self.XrayObj)
        SW_Reqs_Matrix = self.get_SW_req_matrix(SW_Reqs_Matrix)
        Sw_Reqs_Matrix_Tests = self.map_tests_and_test_executions(SW_Reqs_Matrix)
        return Sw_Reqs_Matrix_Tests

class DefectRetestMatrix(TestTraceabilityMapper):
    def test_association_with_defects ()

class Test_execution_Matrix ():
    """
    Utility class for summarizing and analyzing test execution data across different dimensions.
    Provides functions for generating table summaries and team-based classifications of test results.
    """

    @staticmethod
    def process_test_data(data):
        table_info = []
        for test_execution, details in data.items():
            sw_bundle = details.get("SW ID",[])
            test_activity = details.get("Type of test activity", [])
            leading_team = details.get("Team", [])
            test_data = details.get("test_data", {})

            '''
            The implementation uses 
            '''

            num_pass = sum(1 for status in test_data.values() if status == "PASS")
            num_fail = sum(1 for status in test_data.values() if status == "FAIL")
            num_no_verdict = sum(1 for status in test_data.values() if status not in ["PASS", "FAIL"])
            total_tests = len(test_data)
            pass_rate = (num_pass / total_tests * 100) if total_tests > 0 else 0

            table_info.append({
                "test_execution": test_execution,
                "sw_bundle": sw_bundle,
                "test_activity": ", ".join(test_activity),
                "leading_team": ", ".join(leading_team),
                "num_pass": num_pass,
                "num_fail": num_fail,
                "num_no_verdict": num_no_verdict,
                "pass_rate": pass_rate
            })

        return table_info

    @staticmethod
    def classify_tests_by_leading_team(data):
        latest_tests = {}
        for test_execution, details in data.items():
            resolution_date = datetime.strptime(details["resolution_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
            leading_team = details.get("Team", [])
            test_data = details.get("test_data", {})

            for test_id, status in test_data.items():
                if test_id not in latest_tests or resolution_date > latest_tests[test_id]["resolution_date"]:
                    latest_tests[test_id] = {
                        "resolution_date": resolution_date,
                        "status": status,
                        "leading_team": leading_team
                    }

        classified_tests = {}
        for test_id, test_info in latest_tests.items():
            leading_team = ", ".join(test_info["Team"])
            if leading_team not in classified_tests:
                classified_tests[leading_team] = {"PASS": 0, "FAIL": 0, "NO_VERDICT": 0}

            if test_info["status"] == "PASS":
                classified_tests[leading_team]["PASS"]+=1
            elif test_info["status"] == "FAIL":
                classified_tests[leading_team]["FAIL"]+=1
            else:
                classified_tests[leading_team]["NO_VERDICT"]+=1

        return classified_tests

class GeneralInfo:
    def __init__(self, author_name:str = None, releaseinfo:str = None, date:str =None):
        self.author = author_name
        self.releaseinfo = releaseinfo
        if date == None:
            self.date = str(datetime.today())
        else: 
            self.date = date

    def compute_rates(self,data):
        total_tests = 0
        passed_tests = 0
        total_system_reqs = 0
        system_reqs_with_tests = 0

        for req_value in data.values():
            if req_value:
                total_system_reqs += len(req_value)
                for sw_value in req_value.values():
                    if sw_value.get('tests'):
                        system_reqs_with_tests += 1
                        for test_value in sw_value['tests'].values():
                            total_tests += 1
                            if test_value and test_value['status'] == 'PASS':
                                passed_tests += 1

        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        coverage_rate = (system_reqs_with_tests / total_system_reqs * 100) if total_system_reqs > 0 else 0

        return pass_rate, coverage_rate

    def test_execution_info (self,data):
        total_tests = sum(len(details['test_data']) for details in data.values())
        total_pass_tests = sum(sum(1 for status in details['test_data'].values() if status == "PASS") for details in data.values())
        overall_pass_rate = (total_pass_tests / total_tests * 100) if total_tests > 0 else 0
        return overall_pass_rate
