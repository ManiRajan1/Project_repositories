import requests
import json, os, warnings, logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv


# Data collection Methods from JIRA by REST API
class jira_data_collector:
    def __init__(
        self, 
        base_url,
        authentication_token,
        api_version = "latest", 
        session = None,
        headers = None,
        timeout = 300):
        '''
        base_url : URL to which a rest api session has to be created
        authentication_token : Bearer token for authentication
        api_version (optional) : version of api
        session (optional) : A request session if already existing
        headers (optional) : Header to be updated
        '''

        self.base_url = base_url
        self.api_root = "rest/api/"
        self.api_version = api_version
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

    def get_issue (self, issue:str) -> dict:
        '''
        issue : Enter issue key to get all fields of an issue
        Return :dict
        '''
        URL = self.resource_url (f"issue/{issue}")
        out = {}
        try:
            response = self.session.get(URL,timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            out ["N/A"] = err.args[0] 
            return out
        response = response.json()
        return response

    def get_remote_link_items (self,issue: str, issue_link_type:str= None) -> dict:
        '''
        issue:  issue key for which remote links are to be collected
        '''
        URL = self.resource_url (f"issue/{issue}/remotelink")
        out = {}
        try:
            response = self.session.get(URL,timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            out ["N/A"] = err.args[0] 
            return out

        response_json = response.json()
        for item in response_json:
            id = item["id"]
            out[id] = {}
            out[id]["url"] = item["object"]["url"]
            try:
                out[id]["name"] = item["application"]["name"]
                out[id]["relationship"] = item["relationship"]    
            except KeyError as e:
                out[id][str(e).replace ("'","")] = f"N/A" 
    
        if issue_link_type == None:
            return out
        else:
            filtered_out = {}
            for k, v in out.items():
                if 'relationship' in v and v['relationship'] == issue_link_type:
                    filtered_out[k] = v    
            return filtered_out

    def get_remote_links_for_list_of_items (self,issues:list, issue_link_type:str = None) -> dict:
        '''
        :param issues: list of issue keys for which remote links are to be collected
        :param issue_link_type (optional) : link type which has to be extract. 
                                            If not provided all links are extracted.
        :return : Dictionary of requirements with links to the remote artifacts
        '''
        out= {}
        for issue in issues:
            out[issue] = self.get_remote_link_items(issue, issue_link_type)
        return out


    def get_jira_defined_links (self,issue: str, issue_link_type:str = None) -> dict:
        """
        Extracts issue keys with the specified link type from the given data.
        If link_type is None, extracts all linked issues and groups them by link type.

        :param issue: issue Key for which the JIRA specific links are to be extracted.
        :param link_type: The link type to search for. If None, all linked issues are extracted.
        :return: Dictionary where keys are link types and values are lists of issue keys.
        """

        data = self.get_issue(issue)
        data = data['fields']
        issue_keys = {}
        
        for link in data.get('issuelinks', []):
            # Check for inward links
            if 'inwardIssue' in link:
                inward_type = link['type']['inward']
                if issue_link_type is None or inward_type == issue_link_type:
                    if inward_type not in issue_keys:
                        issue_keys[inward_type] = []
                    issue_keys[inward_type].append(link['inwardIssue']['key'])

            # Check for outward links
            if 'outwardIssue' in link:
                outward_type = link['type']['outward']
                if issue_link_type is None or outward_type == issue_link_type:
                    if outward_type not in issue_keys:
                        issue_keys[outward_type] = []
                    issue_keys[outward_type].append(link['outwardIssue']['key'])
        return issue_keys


    def get_jira_defined_links_for_list_of_items (self,issues:list, linktype:str=None) -> dict:
        
        issue_keys = {}
        for issue in issues:
            issue_keys[issue] = self.get_jira_defined_links (issue, linktype)
        return  issue_keys

    def get_field_map(self):
        '''
        self.field_map : The object holds an dictionary "field_map" with the mapping 
        between all fields (Jira/custom fields) and their assigned name in JIRA
        as {field_id: name}
        '''
        url = self.resource_url ("field")
        try:
            field_map = self.session.get (url,timeout=self.timeout)
            field_map.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print (err.args[0]) 
            self.field_map = {}

        if field_map.status_code == 200:
            field_map = field_map.json()
            self.field_map = {}
            for index in range (0, len (field_map)):
                self.field_map[field_map[index]["id"]] =\
                    field_map[index]["name"]

    def issue_Filter_by_jql (self, query: str):
        '''
        params: 
            -query: jql query for which the list of issues must be collected
        Return a issueList specific to the query
        '''
        breakcondition = True
        Length = 1000
        Index1 = 0
        issueList = []
        url = self.resource_url ("search") 
        while breakcondition:
            data = {
                "jql": query,
                "startAt": Index1,
                "maxResults":Length,
                 "fields":["*all", "-description"]}
            try:
                response = self.session.post (url, json = data,  timeout=self.timeout )
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print (err.args[0]) 
                return issueList
            
            if response.status_code == 200:
                response = response.json()
                if len(response['issues']) > 0:
                    issueList += response['issues']
                if len(response['issues']) < Length:
                    breakcondition = False
                else:
                    Index1 += Length
            else:
                print (f"Response of issueFilter ended with {response.status_code} at {Index1} result")
                break
        return issueList

    def field_map_response (self, issues:list):
        '''
        params: 
            -issueList: List of all issues with schema for which id of the fields have to replaced by names                            
        Returns list of issues schema with issuefields mapped to names.
        '''
        self.get_field_map()
        for index in range(0,len(issues)):
            issues[index]['fields'] = {self.field_map.get (k, k):v for k, v in issues[index]['fields'].items()}
        return issues

    def archive_issue_list (self, issueList:list, notifyUsers = True):
        '''
        params: 
            -issueList: List of all issues that has to be archived
            -notifyUsers (optional): Parameter disables email notification to owners of the issues
            provided user has admin privileges                                 
        Returns a  the list of issues archived.
        '''
        archive_URL = self.resource_url ("issue/archive")
        response = self.session.post(archive_URL,json=issueList,params={'notifyUsers': notifyUsers})
        return response
    
    def __del__(self):
        self.session.close()
        del(self)

if __name__ == "__main__":
    load_dotenv()
    BASE_URL = os.getenv ("JIRA_BASE_URL")
    TOKEN_AUTH = os.getenv("JIRA_PAT")
    USERNAME = os.getenv ("USERNAME")

    #Test jira_data_collector
    J_obj = jira_data_collector(BASE_URL,TOKEN_AUTH)
    issueList = J_obj.issue_Filter_by_jql (f"issuetype = 'Test' AND assignee = {USERNAME}")
    J_obj.field_map_response(issueList)
    print ("Test successful")
