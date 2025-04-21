import requests
import json, os, warnings, logging,sys
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class GitLab_data_collector:

    def __init__(
        self, 
        base_url,
        authentication_token,
        api_version = "v4", 
        api_root = "api",
        session = None,
        headers = None,
        timeout = 45):
        '''
        base_url : URL to which a rest api session has to be created
        authentication_token : Bearer token for authentication
        api_version (optional) : version of api
        session (optional) : A request session if already existing
        headers (optional) : Header to be updated
        '''

        self.base_url = base_url
        self.api_root = api_root
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

#############################        Utilities        #####################################
    def resource_url (self,resource:str = None):
        url = ""
        url = "/".join (str(x).strip("/")\
            for x in [self.base_url, self.api_root, self.api_version, resource] if x is not None)
        return url

################################## Project Information ###################################

    def get_project_info_by_URL (self, encoded_URL:str):
        url = self.resource_url(f"projects")
        response = self.session.get(f"{url}/{encoded_URL}")
        if response.status_code == 200:
            return response.json()
        else:
            print (response.text, end = " ")
            print (f"{url}/{encoded_URL}")
            return None   



##################### Get individual merge requests information by IID ##########################

    def search_commits_by_merge_request_id (self, projectID:str, merge_request_iid:str):
        url = self.resource_url(f"projects/{projectID}/merge_requests/{merge_request_iid}/commits")
        response = self.session.get(url)
        if response.status_code == 200:
            response = response.json()
            data_to_retain = ['id','message','author_name','committer_name','web_url']
            for index in range(0, len(response)):
                response[index] = {k:response[index].get(k, 'N/A') \
                    for k,v in response[index].items()\
                    if  k in data_to_retain }
            return response
        else:
            return None

    def search_by_merge_request_id (self, projectID:str, merge_request_iid:str):
        url = self.resource_url(f"projects/{projectID}/merge_requests/{merge_request_iid}")
        response = self.session.get(url)
        if response.status_code == 200:
            response =  response.json()
            data_to_retain = ["id", "iid","project_id", "title", "description", "state","labels",\
                            "merged_by", "merged_at", "source_project_id", "target_project_id",\
                            "target_branch", "source_branch", "should_remove_source_branch",\
                            "force_remove_source_branch", "references", "web_url", "squash",\
                            "squash_on_merge", "pipeline", "diff_refs"]
            response = {k:response.get(k, 'N/A') for k,v in response.items()\
                        if  k in data_to_retain }   
            return response 

        else:
            return None
   
    def get_merge_request_information_by_IID (self, projectID:str, merge_request_iid:str):
        '''
        params: 
        - projectID = project ID of the repo
        - merge_request_iid = ID of the merge request
        Returns: dictionary containing information from Merge request
        '''
        merge_request = {}
        merge_request ['overview'] = self.search_by_merge_request_id(projectID, merge_request_iid)
        merge_request ['commits'] =  self.search_commits_by_merge_request_id(projectID, merge_request_iid)
        return merge_request

##################### Get merge request information by user #########################

    def search_merge_request_by_user(self, username:str):
        pass

##################### Filter merge requests information by created date of MR ##########################

    def search_by_merge_requests_by_created_date (self, projectID:str, params : None):
        url = self.resource_url(resource = f"projects/{projectID}/merge_requests")
        response = self.session.get(url, params = params)
        merge_requests = []
        if response.status_code == 200:
            for item in response.json():
                merge_requests.append(item['iid'])
        return merge_requests

    
    def get_merge_request_information_by_created_date (self, projectID:str, params: None):
        merge_requests = []
        merge_requests = self.search_by_merge_requests_by_created_date(projectID,params)
        merge_requests = [self.get_merge_request_information_by_IID(projectID, item)\
            for item in merge_requests]
        return merge_requests 



if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    BASE_URL = os.getenv ("GITLAB_URL")
    TOKEN_AUTH = os.getenv("GITLAB_PAT")

    #Test GitLab_data_collector
    Gitlab_obj = GitLab_data_collector(BASE_URL,TOKEN_AUTH)
    print ("Test successful")