'''
Begin Declare Input Parameters
 [
 ]
 End Declare
 '''
import time
import datetime
import json

def BuildParameters(context, device_name, params):
    node_dn = GetDeviceProperties(context, device_name, {'techName': 'VELOCLOUD', 'paramType': 'SDN', 'params':['id', 'nbPathSchema', 'nbPathValue', 'enterpriseId']})
    edge_id = node_dn['params'].get('id')
    enterprise_id = node_dn['params'].get('enterpriseId')
    dev_schema = node_dn['params'].get('nbPathSchema')
    rtn_params = { 'name':device_name, 'edge_id' : edge_id, 'enterprise_id':enterprise_id, 'dev_schema': dev_schema}
    return rtn_params

def RetrieveData(rtn_params):
    edge_id = int(rtn_params['edge_id'])
    enterprise_id = int(rtn_params['enterprise_id'])
    dev_name = rtn_params['name']
    if not (edge_id and enterprise_id):
        return {'error:':'params not correct', 'rtn_params':rtn_params}
    edge_url = '/portal/rest/linkQualityEvent/getLinkQualityEvents'
    time_end = datetime.datetime.now()
    time_start = time_end - datetime.timedelta(days=1) # to show metrics of 1 day
    js_end = int(datetime.datetime.timestamp(time_end)*1000) #time in ms
    js_start = int(datetime.datetime.timestamp(time_start)*1000) #time in ms
    body = {
        "enterpriseId": enterprise_id,
        "edgeId": edge_id,
        "interval":{
            "end": js_end,
            "start": js_start
            }
        }
    rtn_params['url'] = edge_url
    rtn_params['body'] = body
    data = json.loads(getData(rtn_params))
    for key in data:
        if key == 'overallLinkQuality':
            data =data[key]
    return json.dumps(data,indent = 4)
