'''
Begin Declare Input Parameters
 [
 ]
 End Declare
 '''
import time
import json

def BuildParameters(context, device_name, params):
    node_dn = GetDeviceProperties(context, device_name, {'techName': 'VELOCLOUD', 'paramType': 'SDN', 'params':['id', 'nbPathSchema', 'nbPathValue', 'enterpriseId']})
    #raise NameError (node_dn)
    edge_id = node_dn['params'].get('id')
    enterprise_id = node_dn['params'].get('enterpriseId')
    #raise NameError (enterprise_id)
    dev_schema = node_dn['params'].get('nbPathSchema')
    rtn_params = { 'name':device_name, 'edge_id' : edge_id, 'enterprise_id':enterprise_id, 'dev_schema': dev_schema}
    return rtn_params

def RetrieveData(rtn_params):
    edge_id = int(rtn_params['edge_id'])
    enterprise_id = int(rtn_params['enterprise_id'])
    dev_name = rtn_params['name']
    if not (edge_id and enterprise_id):
        return {'error:':'params not correct', 'rtn_params':rtn_params}
    #edge_url = '/portal/rest/edge/getEdgeConfigurationModules'
    
    edge_url = '/portal/rest/edge/getEdge'
    
    #edge_url = '/portal/rest /enterprise/getEnterpriseConfigurations'
    
    body = {
        "enterpriseId": enterprise_id,
        "edgeId": edge_id,
        "modules": ["deviceSettings"]
    }
    rtn_params['url'] = edge_url
    rtn_params['body'] = body
    data = json.loads(getData(rtn_params))
    return json.dumps(data,indent = 4)



    
################################################################################################
##########################    Expected Output on vedges   ##############################################
################################################################################################


{
    "id": 5682,
    "created": "2023-02-07T19:21:14.000Z",
    "enterpriseId": 1309,
    "enterpriseLogicalId": "136697a9-7a99-447b-8faa-009f718d59b5",
    "siteId": 5723,
    "activationKey": "ULPP-23N2-NF3S-MCZ3",
    "activationKeyExpires": "2023-03-09T19:21:15.000Z",
    "activationState": "ACTIVATED",
    "activationTime": "2023-02-08T02:23:18.000Z",
    "softwareVersion": "5.0.1.2",
    "buildNumber": "R5012-20221107-GA-abdaf158ef",
    "factorySoftwareVersion": "3.4.1",
    "factoryBuildNumber": "R341-20200410-GA-8695e50275",
    "platformFirmwareVersion": "",
    "platformBuildNumber": "",
    "modemFirmwareVersion": "",
    "modemBuildNumber": "",
    "softwareUpdated": "2023-03-22T02:58:09.000Z",
    "selfMacAddress": "00:50:56:b6:07:70",
    "deviceId": "00:50:56:b6:07:70",
    "logicalId": "1ff38377-0e58-4e83-9c73-01e58e9a5113",
    "serialNumber": "VMware-4236746fb5fb4fe7-29cf3df1f2a97bdf",
    "modelNumber": "vmware",
    "deviceFamily": "VIRTUAL_EDGE",
    "lteRegion": null,
    "name": "Velocloud-Branch1",
    "dnsName": null,
    "description": null,
    "alertsEnabled": 1,
    "operatorAlertsEnabled": 1,
    "edgeState": "CONNECTED",
    "edgeStateTime": "0000-00-00 00:00:00",
    "isLive": 0,
    "systemUpSince": "2023-12-19T04:11:39.000Z",
    "serviceUpSince": "2023-12-19T04:12:06.000Z",
    "lastContact": "2024-06-15T14:08:09.618Z",
    "serviceState": "IN_SERVICE",
    "endpointPkiMode": "CERTIFICATE_OPTIONAL",
    "haState": "UNCONFIGURED",
    "haPreviousState": "UNCONFIGURED",
    "haLastContact": "2023-07-07T06:21:59.000Z",
    "haSerialNumber": null,
    "bastionState": "UNCONFIGURED",
    "modified": "2024-06-03T06:13:45.000Z",
    "customInfo": "",
    "haMode": null,
    "standbySystemUpSince": "0000-00-00 00:00:00.000",
    "standbyServiceUpSince": "0000-00-00 00:00:00.000",
    "standbySoftwareVersion": null,
    "standbyFactorySoftwareVersion": null,
    "standbyFactoryBuildNumber": null,
    "standbyBuildNumber": null,
    "standbyModelNumber": null,
    "standbyDeviceId": null,
    "haWifiCapabilityMismatch": null
}