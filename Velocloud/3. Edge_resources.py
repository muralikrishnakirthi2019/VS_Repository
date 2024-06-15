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
    
    #edge_url = '/portal/rest/metrics/getEdgeStatusSeries'
    
    edge_url = '/portal/rest/metrics/getEdgeStatusMetrics'
    
    
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
    "total": 94,
    "tunnelCount": {
        "min": 3,
        "max": 4,
        "average": 3.478723404255319
    },
    "memoryPct": {
        "min": 29,
        "max": 29,
        "average": 29
    },
    "flowCount": {
        "min": 9,
        "max": 18,
        "average": 11.787234042553191
    },
    "cpuPct": {
        "min": 8,
        "max": 8,
        "average": 8
    },
    "cpuCoreTemp": {
        "min": 0,
        "max": 0,
        "average": 0
    },
    "handoffQueueDrops": {
        "min": 0,
        "max": 0,
        "average": 0
    },
    "tunnelCountV6": {
        "min": 0,
        "max": 0,
        "average": 0
    }
}
