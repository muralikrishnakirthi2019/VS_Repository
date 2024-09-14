import requests
import json
import urllib3
import pprint
import getpass
urllib3.disable_warnings

class Netbrain:
    endpoint = ""
    tenantId = ""
    domainId = ""
    username = ""
    token = ""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, endpoint, username, password, tenantName, domainName):
        self.endpoint = endpoint
        self.username = username
        self.token = self.getTokens(username, password)
        self.headers["token"] = self.token

    def getTokens(self, username, password):
        login_api_url = "/ServicesAPI/API/V1/Session"
        login_url = self.endpoint + login_api_url
        body_data = {
            "username": username,
            "password": password
        }
        try:
            token = requests.post(login_url, data=json.dumps(body_data), headers=self.headers, verify=True)
            if token.status_code == 200:
                return token.json()["token"]
            else:
                return token.text
        except Exception as e:
            return str(e)


    def logout(self):
        logout_api_url = "/ServicesAPI/API/V1/Session"
        logout_url = self.endpoint + logout_api_url
        try:
            response = requests.delete(logout_url, headers=self.headers, verify=True)
            if response.status_code == 200:
                print("Logout successfully.")
            else:
                return response.text
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    endpoint = "https://customer-journey-lab.netbrain.com/"
    tenantName = "Initial Tenant"
    domainName = "Murali_DND"
   #username = input("Enter the username:")
   #password = getpass.getpass("Enter the password: ")
    username = "muralikrishna.kirthi@netbrain.com"
    password = "Ossr@2024"

    # Initiate NetBrain object
    nb = Netbrain(endpoint, username, password, tenantName, domainName)
    print("Token:", nb.getTokens(username, password))
