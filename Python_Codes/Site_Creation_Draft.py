import requests
import json
import time
import sys
import urllib3
urllib3.disable_warnings


class Netbrain():
    endpoint = ""
    tenantId = ""
    domainId = ""
    username = ""
    token = ""
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    def __init__(self, endpoint, username, password, tenantName, domainName):
        self.endpoint = endpoint

        
        self.headers["token"] = "eyJhbGciOiJIUzUxMiIsImtpZCI6IklEIiwidHlwIjoiSldUIn0.eyJTRVNTSU9OX0lEIjoiNTBhYzM4MDktYTZjMi00ZmVmLThlNmMtMjVmNGU3MjY0ZDkzIiwiVVNFUl9JRCI6ImVmNzA3OTk5LTU3YTItNGI4Ny1hODkwLTM1ZDZjNjExZjNkYSIsIlVTRVJfTkFNRSI6InRlc3RhcGkiLCJDTElFTlRfQVBQIjoiUkVTVGZ1bEFQSSIsIlJFQUxNX1RZUEUiOiJBdXRvbWF0aW9uVG9rZW4iLCJSRUFMTV9JRCI6IiIsIlJFQUxNX0FMSUFTIjoiTmV0QnJhaW4iLCJuYmYiOjE3MjI5MzM0NTIsImV4cCI6MTg4MDY5OTg1MiwiaWF0IjoxNzIyOTMzNDUyLCJpc3MiOiJuZXRicmFpbiIsImF1ZCI6ImllIn0.1IuMXBuOLGtcNNyV9AEp4H06fs8SnhZFGwaxgLzltqdAJg3NM5pVkaOnncCsLBh98TfibSx_M-wsxS84mVRPdw"
        
        
        self.tenantId = self.getTenantIdByName(tenantName)
        self.domainId = self.getDomainIdByName(self.tenantId, domainName)



            
    def createSiteTransaction(self):
        self.endpoint = endpoint
        self.tenantId = self.getTenantIdByName(tenantName)
        self.domainId = self.getDomainIdByName(self.tenantId, domainName)
        token="eyJhbGciOiJIUzUxMiIsImtpZCI6IklEIiwidHlwIjoiSldUIn0.eyJTRVNTSU9OX0lEIjoiNTBhYzM4MDktYTZjMi00ZmVmLThlNmMtMjVmNGU3MjY0ZDkzIiwiVVNFUl9JRCI6ImVmNzA3OTk5LTU3YTItNGI4Ny1hODkwLTM1ZDZjNjExZjNkYSIsIlVTRVJfTkFNRSI6InRlc3RhcGkiLCJDTElFTlRfQVBQIjoiUkVTVGZ1bEFQSSIsIlJFQUxNX1RZUEUiOiJBdXRvbWF0aW9uVG9rZW4iLCJSRUFMTV9JRCI6IiIsIlJFQUxNX0FMSUFTIjoiTmV0QnJhaW4iLCJuYmYiOjE3MjI5MzM0NTIsImV4cCI6MTg4MDY5OTg1MiwiaWF0IjoxNzIyOTMzNDUyLCJpc3MiOiJuZXRicmFpbiIsImF1ZCI6ImllIn0.1IuMXBuOLGtcNNyV9AEp4H06fs8SnhZFGwaxgLzltqdAJg3NM5pVkaOnncCsLBh98TfibSx_M-wsxS84mVRPdw"
        nb_url = self.endpoint
        full_url = nb_url + "/ServicesAPI/API/V1/CMDB/Sites/Transactions"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers["Token"] = token
        print("we are in transcation")
        try:
            response = requests.post(full_url, headers = headers, verify = True)
            if response.status_code == 200:
                result = response.json()
                print (result)
                print("we are in transcation result")
            else:
                print ("Get User Report failed! - " + str(response.text))
            
        except Exception as e:
            print (str(e)) 
   
   
      def CreateSite(self):
        create_site_url = "/ServicesAPI/API/V1/CMDB/Sites"
        createsiteurl = self.endpoint + create_site_url
        sitePath = "My Network/Test_Container/Krishna123"
        isContainer = True
        print("we are in Create Site")
        body_data = {
        "sites":[
                    {
                        "sitePath" : sitePath,
                        "isContainer": isContainer
                    }
				]
        }           
        try:
            response = requests.post(createsiteurl, headers=self.headers, data=json.dumps(body_data), verify=True)
            if response.status_code == 200:
                response_json = response.json()
                return response_json
                print("we are in Createsite result")
            else:
                return response.text
        except Exception as e:
            return str(e)

    def CommitSite(self):
        token="eyJhbGciOiJIUzUxMiIsImtpZCI6IklEIiwidHlwIjoiSldUIn0.eyJTRVNTSU9OX0lEIjoiNTBhYzM4MDktYTZjMi00ZmVmLThlNmMtMjVmNGU3MjY0ZDkzIiwiVVNFUl9JRCI6ImVmNzA3OTk5LTU3YTItNGI4Ny1hODkwLTM1ZDZjNjExZjNkYSIsIlVTRVJfTkFNRSI6InRlc3RhcGkiLCJDTElFTlRfQVBQIjoiUkVTVGZ1bEFQSSIsIlJFQUxNX1RZUEUiOiJBdXRvbWF0aW9uVG9rZW4iLCJSRUFMTV9JRCI6IiIsIlJFQUxNX0FMSUFTIjoiTmV0QnJhaW4iLCJuYmYiOjE3MjI5MzM0NTIsImV4cCI6MTg4MDY5OTg1MiwiaWF0IjoxNzIyOTMzNDUyLCJpc3MiOiJuZXRicmFpbiIsImF1ZCI6ImllIn0.1IuMXBuOLGtcNNyV9AEp4H06fs8SnhZFGwaxgLzltqdAJg3NM5pVkaOnncCsLBh98TfibSx_M-wsxS84mVRPdw"
        nb_url = self.endpoint
        full_url = nb_url + "/ServicesAPI/API/V1/CMDB/Sites/Transactions"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        headers["Token"] = token
        rebuildSite = True
        body = {"rebuildSite" : rebuildSite}
        try:
            response = requests.put(full_url, data = json.dumps(body), headers = headers, verify = True)
            if response.status_code == 200:
                result = response.json()
                print("we are in CommitSite result")
                print (result)
            else:
                print ("Site commit Failed! - " + str(response.text))
    
        except Exception as e:
            print (str(e)) 
      

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
        get_tenant_api_url = "ServicesAPI/API/V1/CMDB/Tenants"
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
        get_domain_api_url = "ServicesAPI/API/V1/CMDB/Domains/?" + tenantId
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
    nb = Netbrain(endpoint, username, password, tenantName, domainName)
    if nb.setCurrentDomain():
        res = nb.createSiteTransaction()
        print(res)
        response = nb.CreateSite()
        print(response)
        response1 = nb.CommitSite()
        print(response1)