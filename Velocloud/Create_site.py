import requests
import json
import time
import sys

class Netbrain():

    endpoint = ""
    tenantId = ""
    domainId = ""
    username = ""
    token = ""
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    def __init__(self, endpoint, username, password, tenantName, domainName):
        self.endpoint = endpoint
        self.username = username
        #self.token = self.getTokens(username,password)
        #self.headers["token"] = self.token
        
        self.headers["token"] = "eyJhbGciOiJIUzUxMiIsImtpZCI6IklEIiwidHlwIjoiSldUIn0.eyJTRVNTSU9OX0lEIjoiNTBhYzM4MDktYTZjMi00ZmVmLThlNmMtMjVmNGU3MjY0ZDkzIiwiVVNFUl9JRCI6ImVmNzA3OTk5LTU3YTItNGI4Ny1hODkwLTM1ZDZjNjExZjNkYSIsIlVTRVJfTkFNRSI6InRlc3RhcGkiLCJDTElFTlRfQVBQIjoiUkVTVGZ1bEFQSSIsIlJFQUxNX1RZUEUiOiJBdXRvbWF0aW9uVG9rZW4iLCJSRUFMTV9JRCI6IiIsIlJFQUxNX0FMSUFTIjoiTmV0QnJhaW4iLCJuYmYiOjE3MjI5MzM0NTIsImV4cCI6MTg4MDY5OTg1MiwiaWF0IjoxNzIyOTMzNDUyLCJpc3MiOiJuZXRicmFpbiIsImF1ZCI6ImllIn0.1IuMXBuOLGtcNNyV9AEp4H06fs8SnhZFGwaxgLzltqdAJg3NM5pVkaOnncCsLBh98TfibSx_M-wsxS84mVRPdw"
        
        
        self.tenantId = self.getTenantIdByName(tenantName)
        self.domainId = self.getDomainIdByName(self.tenantId, domainName)


    def getTokens(self, username, password):
        login_api_url = "/ServicesAPI/API/V1/Session"
        login_url = self.endpoint + login_api_url
        body_data = {}
        try:
            token = requests.post(login_url, data=json.dumps(body_data), headers=self.headers, verify=True)
            print(token)
            if token.status_code == 200:
                return token.json()["token"]
            else:
                return token.text
        except Exception as e:
            return str(e)
        
    def CreateSite(self):
        create_site_url = "/ServicesAPI/API/V1/CMDB/Sites"
        createsiteurl = self.endpoint + create_site_url
        body_data = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(createsiteurl, headers=self.headers, data=json.dumps(body_data), verify=True)
            if response.status_code == 200:
                response_json = response.json()
                return response_json
            else:
                return response.text
        except Exception as e:
            return str(e)

    def setCurrentDomain(self):
        set_domain_api_url = "/ServicesAPI/API/V1/Session/CurrentDomain"
        set_domain_url = self.endpoint + set_domain_api_url
        body = {
            "tenantId":self.tenantId,
            "domainId":self.domainId
        }
        try:
            response = requests.put(set_domain_url, headers=self.headers, data=json.dumps(body), verify=True)
            if response.status_code == 200:
                # print(response.json())
                print("Session set to Tenant ID: {}/Domain ID: {}".format(body["tenantId"], body["domainId"]))
                return True
            else:
                return response.text
        except Exception as e:
            return str(e)
        
    def getTenantIdByName(self, tenantName):
        get_tenant_api_url = "/ServicesAPI/API/V1/CMDB/Tenants"
        get_tenant_url = self.endpoint + get_tenant_api_url
        try:
            response = requests.get(get_tenant_url, headers=self.headers, verify=True)
            if response.status_code == 200:
                response_json = response.json()
                tenants = response_json['tenants']
                for tenant in tenants:
                    if tenant['tenantName'] == tenantName:
                        tenantId = tenant["tenantId"]
                        return tenantId
            else:
                return response.text
        except Exception as e:
            return str(e)

    def getDomainIdByName(self, tenantId, domainName):
        get_domain_api_url = "/ServicesAPI/API/V1/CMDB/Domains/?" + tenantId
        get_domain_url = self.endpoint + get_domain_api_url
        try:
            response = requests.get(get_domain_url, headers=self.headers, verify=True)
            if response.status_code == 200:
                response_json = response.json()
                domains = response_json['domains']
                for domain in domains:
                    if domain['domainName'] == domainName:
                        domainId = domain["domainId"]
                        return domainId
            else:
                return response.text
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
    
    endpoint = "https://customer-journey-lab.netbrain.com"
    tenantName = "Initial Tenant"
    domainName = "Murali_DND"
    username = "muralikirthi"
    password = "Murali@2024"
    
    #request_body = {
    #"folderPath": "Public/Rakesh",
    #"fileTypes": [999]
    #}
    
    sitePath = "My Network/Test_Container/TestSite123"
    isContainer = False
    
    request_body = {
        "sites":        [
                {
                    "sitePath" : sitePath,
                    "isContainer": isContainer
                }
            ]
    }         




    # Initiate NetBrain object
    nb = Netbrain(endpoint, username, password, tenantName, domainName)
    
    # If set working domain successfully, continue...
    if nb.setCurrentDomain():
        response = nb.CreateSite()
        print(response)