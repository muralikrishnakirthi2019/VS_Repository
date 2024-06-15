'''
Begin Declare Input Parameters
[
]
End Declare
 
For sample
[
    {"name": "$param1"},
    {"name": "$param2"}
]
'''
import datetime
import json
  
def BuildParameters(context, device_name, params):
    get_dn = GetDeviceProperties(context, device_name, {'techName': 'VELOCLOUD', 'paramType': 'SDN', 'params': ['*']})
    edge_id = get_dn['params'].get('id')
    enterprise_id = get_dn['params'].get('enterpriseId')
    dev_schema = get_dn['params'].get('nbPathSchema')
    rtn_params = {'name':device_name, 'edge_id':edge_id, 'enterprise_id' :enterprise_id, 'dev_schema':dev_schema}
    #raise NameError(rtn_params)
    return rtn_params
     
def RetrieveData(rtn_params):
    edge_id = int(rtn_params['edge_id'])
    enterprise_id = int(rtn_params['enterprise_id'])
    device_name = rtn_params['name']
    #raise NameError(device_name)
    #write error code BuildParameters
    if not (edge_id and enterprise_id):
        return {'error' : 'params not correct', 'rtn_params':rtn_params}
    time_end = datetime.datetime.now()
    time_start = time_end-datetime.timedelta(days=1)
    js_end = int(datetime.datetime.timestamp(time_end)*1000)
    js_start = int(datetime.datetime.timestamp(time_start)*1000)
    url = '/portal/rest/edge/getEdgeSDWANPeers'
    body = {'edgeId':edge_id, 'enterpriseId' :enterprise_id, 'interval':{"end":js_end,"start":js_start}}
    rtn_params['url'] = url
    rtn_params['body'] = body
    data = json.loads(getData(rtn_params))
    #raise NameError(getData(rtn_params))
    return json.dumps(data,indent =4)
    
    
    
################################################################################################
##########################    Expected Output on vedges   ##############################################
################################################################################################


[
    {
        "peerType": "HUB",
        "peerHAType": null,
        "clusterId": null,
        "peerName": "Velocloud-Hub",
        "description": null,
        "edgeLogicalId": "1ff38377-0e58-4e83-9c73-01e58e9a5113",
        "scoreAfterVoice": 10,
        "scoreAfterVideo": 10,
        "scoreAfterTrans": 10,
        "pathQoe": 10,
        "deviceLogicalId": "8df8d506-d03e-4771-9ee9-e7d2781c26a5",
        "pathStatusCount": {
            "stable": 1,
            "unstable": 0,
            "standby": 0,
            "dead": 0,
            "unknown": 0,
            "total": 1
        }
    },
    {
        "peerType": "GATEWAY",
        "peerName": "vcg31-nyc4",
        "description": null,
        "edgeLogicalId": "1ff38377-0e58-4e83-9c73-01e58e9a5113",
        "scoreAfterVoice": 9.98951048951049,
        "scoreAfterVideo": 9.98951048951049,
        "scoreAfterTrans": 9.994755244755245,
        "pathQoe": 9.991258741258742,
        "deviceLogicalId": "576881c5-5933-4af9-91fb-0994e7668806",
        "pathStatusCount": {
            "stable": 1,
            "unstable": 0,
            "standby": 0,
            "dead": 0,
            "unknown": 0,
            "total": 1
        }
    },
    {
        "peerType": "GATEWAY",
        "peerName": "vcg31-yyz1",
        "description": null,
        "edgeLogicalId": "1ff38377-0e58-4e83-9c73-01e58e9a5113",
        "scoreAfterVoice": 9.966783216783217,
        "scoreAfterVideo": 9.958041958041958,
        "scoreAfterTrans": 10,
        "pathQoe": 9.974941724941724,
        "deviceLogicalId": "4bf173e6-a59d-48d6-8612-f69f3fbc6158",
        "pathStatusCount": {
            "stable": 1,
            "unstable": 0,
            "standby": 0,
            "dead": 0,
            "unknown": 0,
            "total": 1
        }
    },
    {
        "peerType": "BRANCH",
        "peerHAType": null,
        "clusterId": null,
        "peerName": "Velocloud-Branch2",
        "description": null,
        "edgeLogicalId": "1ff38377-0e58-4e83-9c73-01e58e9a5113",
        "scoreAfterVoice": 10,
        "scoreAfterVideo": 10,
        "scoreAfterTrans": 10,
        "pathQoe": 10,
        "deviceLogicalId": "72afd8df-43a1-4e70-b4dc-8ff528bcaf29",
        "pathStatusCount": {
            "stable": 0,
            "unstable": 0,
            "standby": 0,
            "dead": 1,
            "unknown": 0,
            "total": 1
        }
    }
]