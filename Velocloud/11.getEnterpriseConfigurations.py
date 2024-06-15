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

    edge_url = '/portal/rest/enterprise/getEnterpriseConfigurations'

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

[
    {
        "id": 8981,
        "created": "2023-01-27T09:37:18.000Z",
        "name": "Quick Start Profile",
        "logicalId": "30d58381-9e26-11ed-a9be-0ac41fae19c1",
        "enterpriseLogicalId": "136697a9-7a99-447b-8faa-009f718d59b5",
        "version": "1674812238359",
        "description": "Netbrain Technologies Inc",
        "configurationType": "SEGMENT_BASED",
        "bastionState": "UNCONFIGURED",
        "schemaVersion": "3.0.0",
        "effective": "2021-06-10T08:35:57.000Z",
        "modified": "2023-01-27T09:37:18.000Z",
        "isStaging": 0
    },
    {
        "id": 17284,
        "created": "2024-06-12T16:49:24.000Z",
        "name": "Murali",
        "logicalId": "b991fb10-28db-11ef-a9a5-0ac41fae19c1",
        "enterpriseLogicalId": "136697a9-7a99-447b-8faa-009f718d59b5",
        "version": "1718210964806",
        "description": "",
        "configurationType": "SEGMENT_BASED",
        "bastionState": "UNCONFIGURED",
        "schemaVersion": "3.0.0",
        "effective": "2021-06-10T08:35:57.000Z",
        "modified": "2024-06-12T16:49:25.000Z",
        "isStaging": 0
    }
]