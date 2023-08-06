import logging
import sys
import requests
import time 
import json

class VirtualisationEngineSessionManager:
    def __init__(self, address, username, password, major, minor, micro):
        logging.basicConfig(filename='DelphixEngineSessionManager.log',
                            level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filemode='w')
        logging.info(30 * '=' + '| RUN BEGINS |' + 30 * '=')
        self.address = address
        self.username = username
        self.password = password
        self.major = major
        self.minor = minor
        self.micro = micro

    def __str__(self):
        return f'Virtualisation Engine Session Manager: {self.address}'

    def _login(self):
        "This function logs into the Virtualisation Engine."
        
        session = requests.session()
        session_url = f"http://{self.address}/resources/json/delphix/session"
        data = {
            "type": "APISession",
            "version": {
                "type": "APIVersion",
                "major": self.major,
                "minor": self.minor,
                "micro": self.micro
            }
        }
        response = session.post(session_url, json=data)
        if not response.ok:
            logging.info(f"Session FAILED to established on {self.address}. Response: {response.status_code}")
            sys.exit()
        url = f"http://{self.address}/resources/json/delphix/login"
        data = {
            "type": "LoginRequest",
            "username": self.username,
            "password": self.password
        }
        response = session.post(url, json=data)
        if not response.ok:
            logging.error(f"login FAILED - Response: {response.status_code}")
            sys.exit()
        return session

    def replicate(self, replicationName): 
        """
        This method executes a replication job. 
        
        Args:
            replicationName: This is the name of the replication job. 
        
        Returns: 
            This method returns True if the replication was successful and False if it fails. 
        """
        session = self._login() 
        spec_url = f"http://{self.address}/resources/json/delphix/replication/spec" 
        APIQuery = session.get(spec_url)
        for replication in APIQuery.json()["result"]:
            if replication['name'] == replicationName: 
                replicationSpec = replication['reference']   
        replication_url = f"http://{self.address}/resources/json/delphix/replication/spec/{replicationSpec}/execute"
        data = {}
        response = session.post(replication_url,json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"==========| Replication Successful! |========== \n Replication Name: {replicationName}\n Engine: {self.address}")
            return True
        else:
            session.close()
            return False 
    
    def refreshContainer(self, containerName): 
        """
        This method refreshes the container on the Delphix Engine. 

        Args: 
            containerName: This is the name of the container to be refreshed on the Delphix Engine.

        Returns: 
            This method returns True is the refresh was made successfully & returns False if it failed to refresh.
        """
        session = self._login()
        container_url = f"http://{self.address}/resources/json/delphix/selfservice/container"
        APIQuery = session.get(container_url)
        for container in APIQuery.json()["result"]:
            if container['name'] == containerName: 
                containerReference = container['reference']
        refresh_url = f"http://{self.address}/resources/json/delphix/selfservice/container/{containerReference}/refresh"
        data = {"type": "JSDataContainerRefreshParameters", "forceOption": False}
        response = session.post(refresh_url,json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"==========| Refresh Successful! |========== \n Container Name: {containerName}\n Engine: {self.address}")
            return True
        else:
            session.close()
            return False 

    def createBookmark(self, containerName, bookmarkName):
        # Set up the session object
        """ 
        This method creates a bookmark on the container of the Delphix Engine. 

        Args: 
            containerName: This is the name of the container to be bookmarked on the Delphix Engine. 
            bookmarkName: This argument is the name of the bookmark to be made on the containerName.
        
        Returns: 
            This method returns True is the bookmark was made successfully & returns False if it failed to create a bookmark. 
        """
        containerReference, containerBranch = self._getTemplateBranch(containerName)
        # Send a POST request to the bookmark endpoint with cookies set from the session
        bookmark_url = f"http://{self.address}/resources/json/delphix/selfservice/bookmark"
        data = {
            "type": "JSBookmarkCreateParameters",
            "bookmark": {
                "type": "JSBookmark",
                "name": bookmarkName,
                "branch": containerBranch
            },
            "timelinePointParameters": {
                "type": "JSTimelinePointLatestTimeInput",
                "sourceDataLayout": containerReference
            }
        }
        session = self._login()
        response = session.post(bookmark_url, json=data)
        action = response.json()['action']
        if self._checkActionLoop(action):
            session.close()
            logging.info(f"==========| Bookmark has been created! |========== \n Bookmark: {bookmarkName} \n Container: {containerName} \n Engine: {self.address}")
            return True
        else:
            session.close()
            return False 

    def _checkActionLoop(self, action): 
        while True:
            if self._checkAction(action):
                return True
            elif self._checkAction(action) == "FAILED":
                logging.error("Failed to create Bookmark. Please see Engine logs.")
                return False
            else:
                print("Not yet Completed, check again in 10 seconds")
                time.sleep(10)

    def _checkAction(self, action):
        session = self._login()
        action_url = f"http://{self.address}/resources/json/delphix/action"
        APIQuery = session.get(action_url)
        for actions in APIQuery.json()["result"]:
            if actions['reference'] == action:
                state = actions['state']
                if state == "COMPLETED":
                    session.close()
                    return True
                elif state == "FAILED":
                    state = "FAILED"
                    session.close()
                    return state
                else:
                    return False
    
    def _getTemplateBranch(self, containerName):
        # Log in and obtain the session object
        session = self._login()   
        # Send a GET request to the selfservice/template endpoint with cookies set from the session
        template_url = f"http://{self.address}/resources/json/delphix/selfservice/container"
        response = session.get(template_url)
        # Extract the template reference and active branch from the API response
        container_reference = None
        container_branch = None
        for container in response.json()["result"]:
            if container['name'] == containerName:
                container_reference = container["reference"]
                container_branch = container["activeBranch"]
                break
        logging.debug(f"container reference: {container_reference} & Template branch: {container_branch}")
        session.close()
        return container_reference, container_branch 
    
class MaskingEngineSessionManager(VirtualisationEngineSessionManager): 
    def __init__(self, address, username, password, major, minor, micro): 
        super().__init__(address, username, password, major, minor, micro)

    def __str__(self):
        return f'Masking Engine Session Manager: {self.address}'
    
    def login(self) -> str:
        """
        This method logs in to the Delphix Masking Engine. 
        
        Returns: 
            str: Authentication key used to send API requests to the engine. 
        """ 
        url = f"http://{self.address}/masking/api/v5.1.14/login"

        payload = json.dumps({"username": self.username, "password": self.password})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        responseDict = response.json()
        authKey = responseDict['Authorization']
        logging.info(f"Authentication key established for Masking Engine {self.address}. Key: {authKey}")
        return authKey
    
    def runMaskingJob(self, environment, maskingRule, connectorName=None) -> bool:
        """
        This method executes pre-configured masking jobs on the masking engine.

        Args: 
            environment: This is the environent on the Delphix masking engine on which to run the masking job. 
            maskingRule: This is the ruleset that we want to run on the delphix engine. 
            connectorName: This is the name of the connector for which connects the masking job to the data. This variable need only be provided if the masking job is mulit-tennant and can be omitted if this is not the case.
        
        Returns: 
            bool: This returns True if it has run successfully and False if there is an Error. 
        """
        
        authKey = self.login()
        envID = self._getEnvironment(authKey, environment)
        ruleID = self._getJobId(authKey, maskingRule, envID)
        if connectorName != None: 
            targetConnectorID = self._getTargetConnectorID(authKey, connectorName, envID)
            self._execute_job(authKey, ruleID, targetConnectorID)
        else: 
            self._execute_job(authKey, ruleID)
        logging.info(f"Masking job triggered. Job: {maskingRule}")
        executionID = self._getExecutionID(authKey, ruleID)
        jobStatus = self._checkStatus(executionID) 

        if jobStatus == "SUCCEEDED":
            logging.info(f"Masking Successful. Job: {maskingRule}")
            return True
        else:
            logging.error(f"Please check error logs for masking job: {maskingRule}")
            return False
    
    def _getEnvironment(self, authKey, envName) -> int:
        """API call to get an environment ID from the environment name

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            envName (int): Name of the environment.

        Returns:
            int: ID of the environment
        """        
        response = self._getRequest(authKey, "environments")
        response = json.loads(response)
        for env in response["responseList"]:
            if env["environmentName"] == envName:
                envID = env["environmentId"]
        return envID
    

    def _getRequest(self, authKey, endPoint) -> str:
        """Generic get request blueprint

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            endPoint (str): HTTP endpoint of chosen API call.

        Returns:
            str: Text response from API request.
        """        
        url = f"http://{self.address}/masking/api/v5.1.14/{endPoint}"
        payload = {}
        headers = {
            'Authorization': authKey
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def _getExecutionID(self, authKey, jobID) -> int:
        """API call to get an execution ID from the job ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            jobID (int): ID of the job.

        Returns:
            int: ID of the execution
        """        
        endPoint = f"executions?job_id={jobID}&page_number=1&execution_status=RUNNING"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        executionID = response['responseList'][0]['executionId']
        return executionID

    def _getJobId(self, authKey, jobName, envID) -> int:
        """API call to get a job ID from the job name and environment ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            jobName (str): Name of the job.
            envID (int): ID of the environment.

        Returns:
            int: ID of the job.
        """        
        endPoint = f"masking-jobs?environment_id={envID}"
        response = self._getRequest(authKey, endPoint)
        response = json.loads(response)
        for job in response["responseList"]:
            if job["jobName"] == jobName:
                jobID = job['maskingJobId']
        return jobID

    def _getTargetConnectorID(self, authKey, connectorName, environmentId) -> int:
        """API call to get a target connector ID from the connector name and environment ID.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            connectorName (str): Name of the connector.
            environmentId (int): ID of the environment.

        Returns:
            int: ID of the target connector.
        """        
        response = self._getRequest(authKey, "database-connectors")
        response = json.loads(response)
        for connectors in response["responseList"]:
            if connectors["connectorName"] == connectorName and connectors["environmentId"] == environmentId:
                targetConnectorID = connectors["databaseConnectorId"]
        return targetConnectorID
     
    def _execute_job(self, auth_key, job_id, targetConnectorID=None) -> str:
        """API call to get a target connector ID from the connector name and environment ID.

        Args:
            auth_key (str): Authentication key used to send API requests to the engine. 
            job_id (_type_): ID of the job.
            targetConnectorID (int, optional): ID of the target connector. Used for multi-tenant jobs. Defaults to None.

        Returns:
            str: Text response from API request.
        """        
        url = f"http://{self.address}/masking/api/v5.1.14/executions"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_key
        }
        if targetConnectorID != None: 
            data = {
                'jobId': job_id, 
                'targetConnectorId': targetConnectorID
            }
        else:
            data = {'jobId': job_id}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text
    
    def _getStatus(self,authKey,executionID) -> str: 
        """API call to get the status of a running job.

        Args:
            authKey (str): Authentication key used to send API requests to the engine. 
            executionID (int): ID of the execution.

        Returns:
            str: Status of the execution.
        """        
        response = self._getRequest(authKey, f"executions/{executionID}")
        response = json.loads(response)
        status = response["status"]
        return status    
    
    def _checkStatus(self, executionID) -> str:
        """Checks the status of an execution.

        Args:
            executionID (int): ID of the execution.

        Returns:
            str: Status of the execution
        """        
        authKey = self.login()
        timeBetweenChecks=60
        while True:
            status = self._getStatus(authKey, executionID)
            
            if status == "RUNNING":
                time.sleep(timeBetweenChecks)
                print(f"Job is still running, check again in {round(timeBetweenChecks / 60, 2)} minute(s).")
            else:
                print(f"Job has finished running. Job Status is: {status}")
                return status
            
    def refreshRuleSets(self, EnvironmentName):
        """This function refreshes all rulesets in an environment which it is able to refresh. 
           If it is not able to refresh a ruleset, then it simply skips over this ruleset and 
           attempts to refresh the next. It records which rulesets it is able to refresh and 
           which it cannot in the log file. 

        Args:
            EnvironmentName (str): Name of the environment.
        """        
        authKey = self.login()
        environmentID = self._getEnvironment(authKey,EnvironmentName)
        response = self._getRequest(authKey, f"database-rulesets?environment_id={environmentID}")
        response = json.loads(response)
        ruleSetIDList = [ruleSet["databaseRulesetId"] for ruleSet in response["responseList"]]
        
        for ruleSetID in ruleSetIDList: 
            url = f"http://{self.address}/masking/api/v5.1.14/database-rulesets/{ruleSetID}/refresh"
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': authKey
            }
            response = requests.put(url, headers=headers)
            json_response = response.json()
            try: 
                async_task_id = json_response['asyncTaskId']
            except KeyError:
                print(f"There's a problem with refreshing id: {ruleSetID} \n Message: {json_response}") 
                logging.error(f"There's a problem with refreshing id: {ruleSetID} \n Message: {json_response}")
                print("Skipping checking loop.")
                ERROR = True
            else:
                ERROR = False
            if not ERROR: 
                while True: 
                    response = self._getRequest(authKey, f"async-tasks/{async_task_id}")
                    response = json.loads(response)
                    if response["status"] == "SUCCEEDED": 
                        print(f"Successful for id: {ruleSetID}")
                        logging.info(f"Successful for id: {ruleSetID}") 
                    else:
                        print("Not yet Completed, check again in 10 seconds")
                        time.sleep(10) 