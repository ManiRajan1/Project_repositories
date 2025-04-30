import requests


class ConfluenceAPI:


    def __init__(self,base_url, token,api_root ='rest/api/'):
        """
        Initialize the ConfluenceAPI object with base URL and personal access token.
        params:
            base_url (str): The base URL of the Confluence instance.
            personal_access_token (str): The personal access token for authentication.
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.api_root = api_root
        # Set the authorization header with the personal access token
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
    
    def resource_url(self, resource, base_url=None, api_root=None):
        '''
        params
            -resource : resource to which the url has to be generated 
             E.g. archive, search, field
        Returns resource url as per REST api documentation
                   following rest/api/
        '''
        if base_url is None:
            base_url = self.base_url
        if api_root is None:
            api_root = self.api_root
        return "/".join(str(s).strip("/") \
            for s in [base_url, api_root, resource] if s is not None)
    

    def create_body(self, body, representation):
        if representation not in [
            "editor",
            "export_view",
            "view",
            "storage",
            "wiki",
        ]:
            raise ValueError("Wrong value for representation, it should be either wiki or storage")

        return {representation: {"value": body, "representation": representation}}

    def create_confluence_page(self,space,title,body,parent_id,
        type="page",
        representation="storage",
        editor=None,
        full_width=False,
    ):
        """
        Create page from scratch
        :param space:
        :param title:
        :param body:
        :param parent_id:
        :param type: page
        :param representation: OPTIONAL: either Confluence 'storage' or 'wiki' markup format
        :param editor: OPTIONAL: v2 to be created in the new editor
        :param full_width: DEFAULT: False
        :return:
        """
        url = self.resource_url("content")
        data = {
            "type": type,
            "title": title,
            "space": {"key": space},
            "body": self.create_body(body, representation),
            "metadata": {"properties": {}},
        }

        data["ancestors"] = [{"type": type, "id": parent_id}]
        if editor is not None and editor in ["v1", "v2"]:
            data["metadata"]["properties"]["editor"] = {"value": editor}
        if full_width is True:
            data["metadata"]["properties"]["content-appearance-draft"] = {"value": "full-width"}
            data["metadata"]["properties"]["content-appearance-published"] = {"value": "full-width"}
        else:
            data["metadata"]["properties"]["content-appearance-draft"] = {"value": "fixed-width"}
            data["metadata"]["properties"]["content-appearance-published"] = {"value": "fixed-width"}

        try:
            response = self.session.post(url, json=data)
        except requests.exceptions.HTTPError as err:
            out ["N/A"] = err.args[0] 
            return out
        return response

 
    def get_confluence_page_by_id(self, page_id, expand="body.view", status = None, version = None, html = False):
        """
        Retrieve the metadata and existing content of a Confluence page.
        params:
        - page_id (str): The ID of the page to retrieve.
        - expand : To view the contents of the page (Default: xhtml body view)
        - status : To filter based on the status of the page (Default: current)
        - version : To get specific version of the page (Default: Latest)
        Returns:
            dict: The JSON response containing the page data, or None if the request fails.
        """
        url = self.resource_url(f"content/{page_id}")
        params = {}
        if expand:
            params["expand"] = expand
        if status:
            params["status"] = status
        if version:
            params["version"] = version
        response = self.session.get(url, params = params)

        if response.ok:
            if html == False:
                return response
            else:
                out = response.json()
                return out['body']['view']['value']
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None

  

    def __del__(self):
        """
        Destructor method to close the session when the object is deleted.
        """
        self.session.close()
        del(self)
