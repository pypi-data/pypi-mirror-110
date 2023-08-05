import pathlib
import os
import json
import subprocess
import requests
import sys
import urllib
from requests.api import request
import urllib3
import socket
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from time import sleep
from typing import Dict
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(category=InsecureRequestWarning)


class IBClient():

    def __init__(self, username: str, account: str, password: str, driver_path: str, client_gateway_path: str = None,):
        self.username = username
        self.account = account
        self.password = password
        self.driver_path = driver_path
        self.client_gateway_path = client_gateway_path
        self.session_state_path: pathlib.Path = pathlib.Path(
            __file__).parent.joinpath('server_session.json').resolve()

        # Define URL Components
        ib_gateway_host = r"https://localhost"
        ib_gateway_port = r"5000"
        self.ib_gateway_path = ib_gateway_host + ":" + ib_gateway_port
        self.api_version = 'v1/'

        if client_gateway_path is None:

            # Grab the Client Portal Path.
            self.client_portal_folder: pathlib.Path = pathlib.Path(__file__).parents[1].joinpath(
                'resources/clientportal.beta.gw'
            ).resolve()
        else:
            self.client_portal_folder = client_gateway_path

        # If the server is not running
        if not self.is_server_running():
            # Start the server
            self.process_id = self.start_server()
            with open(self.session_state_path, 'w') as server_file:
                json.dump(
                    obj={'server_process_id': self.server_process},
                    fp=server_file
                )

            # Login
            self.login_auth()

        # Else check auth
        elif not self.is_authenticated():
            self.login_auth()

    def is_server_running(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        if result == 0:
            return True
        else:
            return False

    def start_server(self):
        """Starts the Server.

        Returns:
        ----
        str: The Server Process ID.
        """

        try:
            if sys.platform == 'win32':
                IB_WEB_API_PROC = ["cmd", "/k",
                                   r"bin\run.bat", r"root\conf.yaml"]
                self.server_process = subprocess.Popen(
                    args=IB_WEB_API_PROC,
                    cwd=self.client_portal_folder,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                ).pid

            elif sys.platform == 'darwin' or sys.platform == 'linux':
                IB_WEB_API_PROC = [r"bin/run.sh", r"root/conf.yaml"]
                self.server_process = subprocess.Popen(
                    args=IB_WEB_API_PROC,
                    cwd=self.client_portal_folder
                ).pid

            return self.server_process
        except Exception as e:
            print(e)
            raise

    def login(self, driver_path: str):

        capabilities = DesiredCapabilities.CHROME
        capabilities["loggingPrefs"] = {
            "performance": "ALL",
        }

        # Settings to get past Chrome local host privacy
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        chromedriver = driver_path
        try:
            driver = webdriver.Chrome(
                executable_path=chromedriver, desired_capabilities=capabilities, options=options)

            # Go to login page
            driver.get("https://localhost:5000")

            # advanced = driver.find_element_by_id("details-button")
            # advanced.click()

            # Type in username and password
            username_textbox = driver.find_element_by_id("user_name")
            username_textbox.send_keys(self.username)
            password_textbox = driver.find_element_by_id("password")
            password_textbox.send_keys(self.password)

            # Click login button / submit
            login_button = driver.find_element_by_id("submitForm")
            login_button.click()

            sleep(4)
            driver.refresh()

            driver.close()
        except Exception as e:
            print(e)

    def _make_request(self, endpoint: str, req_type: str, headers: str = 'json', params: dict = None, data: dict = None, json: dict = None) -> Dict:
        """Handles the request to the client.

        Handles all the requests made by the client and correctly organizes
        the information so it is sent correctly. Additionally it will also
        build the URL.

        Arguments:
        ----
        endpoint {str} -- The endpoint we wish to request.

        req_type {str} --  Defines the type of request to be made. Can be one of four
            possible values ['GET','POST','DELETE','PUT']

        params {dict} -- Any arguments that are to be sent along in the request. That
            could be parameters of a 'GET' request, or a data payload of a
            'POST' request.

        Returns:
        ----
        {Dict} -- A response dictionary.

        """
        # First build the url.
        url = self._build_url(endpoint=endpoint)

        # Define the headers.
        headers = self._headers(mode=headers)

        # Make the request.
        if req_type == 'POST':
            response = requests.post(
                url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'GET':
            response = requests.get(
                url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'DELETE':
            response = requests.delete(
                url=url, headers=headers, params=params, json=json, verify=False)

        # grab the status code
        status_code = response.status_code

        # Check to see if it was successful
        if response.ok:
            return response.json()

        # if it was a bad request print it out.
        elif not response.ok and url != 'https://localhost:5000/v1/portal/iserver/account':
            print(response, response.text)
            if 'content-type' in response.headers.keys() and response.headers['content-type'] == 'application/json;charset=utf-8':
                error = requests.HTTPError(response=response.json())
            else:
                error = requests.HTTPError()
            raise(error)

    def is_authenticated(self, check: bool = False) -> Dict:
        """Checks if session is authenticated.

        Overview:
        ----
        Current Authentication status to the Brokerage system. Market Data and 
        Trading is not possible if not authenticated, e.g. authenticated 
        shows `False`.

        Returns:
        ----
        (dict): A dictionary with an authentication flag.   
        """

        # define request components
        endpoint = 'iserver/auth/status'

        if not check:
            req_type = 'POST'
        else:
            req_type = 'GET'

        try:
            auth_response = self._make_request(
                endpoint=endpoint,
                req_type=req_type,
                headers='none'
            )
            print(auth_response)
            if 'authenticated' in auth_response.keys() and auth_response['authenticated'] == True:
                self.authenticated = True
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def _build_url(self, endpoint: str) -> str:
        """Builds a url for a request.

        Arguments:
        ----
        endpoint {str} -- The URL that needs conversion to a full endpoint URL.

        Returns:
        ----
        {srt} -- A full URL path.
        """

        # otherwise build the URL
        return urllib.parse.unquote(
            urllib.parse.urljoin(
                self.ib_gateway_path,
                self.api_version
            ) + r'portal/' + endpoint
        )

    def _headers(self, mode: str = 'json') -> Dict:
        """Builds the headers.

        Returns a dictionary of default HTTP headers for calls to Interactive
        Brokers API, in the headers we defined the Authorization and access
        token.

        Arguments:
        ----
        mode {str} -- Defines the content-type for the headers dictionary.
            default is 'json'. Possible values are ['json','form']

        Returns:
        ----
        Dict
        """

        if mode == 'json':
            headers = {
                'Content-Type': 'application/json'
            }
        elif mode == 'form':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        elif mode == 'none':
            headers = None

        return headers

    def login_auth(self, i=0):
        i = i
        self.login(self.driver_path)
        authenticated = self.is_authenticated()
        if not authenticated and i < 10:
            print(f"Login failed. Attempting again {i+1}/10")
            self.login_auth(i + 1)
        elif not authenticated:
            print("Unable to login after 10 tries")
            raise
        elif authenticated:
            print("Successfully authenticated")
