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
        self.tenantId = self.getTenantIdByName(tenantName)
        self.domainId = self.getDomainIdByName(self.tenantId, domainName)

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
        get_domain_api_url = f"ServicesAPI/API/V1/CMDB/Domains/?tenantId={tenantId}"
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
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

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
    domainName = "CJourney_LAB1"
    username = input("Enter the username:")
    password = getpass.getpass("Enter the password: ")

    # Initiate NetBrain object
    nb = Netbrain(endpoint, username, password, tenantName, domainName)
    print("Token:", nb.getTokens(username, password))
    print("Tenant ID:", nb.getTenantIdByName(tenantName))
    print("Domain ID:", nb.getDomainIdByName(nb.tenantId, domainName))
