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
    
    