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
    url = '/portal/rest/metrics/getEdgeLinkMetrics'
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
        "linkId": 14301,
        "linkLogicalId": "00000003-0e58-4e83-9c73-01e58e9a5113",
        "bytesTx": 123762731,
        "bytesRx": 93886501,
        "packetsTx": 1240582,
        "packetsRx": 1176560,
        "totalBytes": 217649232,
        "totalPackets": 2417142,
        "p1BytesRx": 21272212,
        "p1BytesTx": 24850607,
        "p1PacketsRx": 84150,
        "p1PacketsTx": 91789,
        "p2BytesRx": 0,
        "p2BytesTx": 0,
        "p2PacketsRx": 0,
        "p2PacketsTx": 0,
        "p3BytesRx": 0,
        "p3BytesTx": 0,
        "p3PacketsRx": 0,
        "p3PacketsTx": 0,
        "controlBytesRx": 72614289,
        "controlBytesTx": 98912124,
        "controlPacketsRx": 1092410,
        "controlPacketsTx": 1148793,
        "bpsOfBestPathRx": 185583000,
        "bpsOfBestPathTx": 100242000,
        "bestJitterMsRx": 0.02097902097902098,
        "bestJitterMsTx": 0,
        "bestLatencyMsRx": 3.56993006993007,
        "bestLatencyMsTx": 2.486013986013986,
        "bestLossPctRx": 0.003217072962047337,
        "bestLossPctTx": 0.0031949274919249797,
        "scoreTx": 4.39986023369369,
        "scoreRx": 4.399825269525701,
        "signalStrength": 0,
        "state": "STABLE",
        "autoDualMode": 0,
        "link": {
            "id": 14301,
            "created": "2023-02-08T02:24:04.000Z",
            "edgeId": 5682,
            "logicalId": "00:08:e3:ff:ff:fc:0000",
            "internalId": "00000003-0e58-4e83-9c73-01e58e9a5113",
            "interface": "GE3",
            "macAddress": null,
            "overlayType": "IPv4",
            "ipAddress": "104.207.208.109",
            "ipV6Address": "",
            "netmask": null,
            "networkSide": "WAN",
            "networkType": "ETHERNET",
            "displayName": "Lightower Fiber Networks I LLC",
            "userOverride": 1,
            "isp": "Lightower Fiber Networks I, LLC",
            "org": "Lightower Fiber Networks I, LLC",
            "lat": 42.428001,
            "lon": -71.061798,
            "lastActive": "2024-06-15T14:00:26.000Z",
            "state": "STABLE",
            "backupState": "UNCONFIGURED",
            "linkMode": "ACTIVE",
            "vpnState": "STABLE",
            "lastEvent": "2024-05-15T20:35:36.000Z",
            "lastEventState": "STABLE",
            "alertsEnabled": 1,
            "operatorAlertsEnabled": 1,
            "serviceState": "IN_SERVICE",
            "modified": "2024-06-15T14:00:26.000Z",
            "holdingEdgeSerialNumber": null,
            "effectiveState": "STABLE"
        },
        "name": "GE3"
    },
    {
        "linkId": 14444,
        "linkLogicalId": "afe53c50-4959-4dc4-a7fd-c3ab28b85dac",
        "bytesTx": 21877669,
        "bytesRx": 16944060,
        "packetsTx": 229052,
        "packetsRx": 234005,
        "totalBytes": 38821729,
        "totalPackets": 463057,
        "p1BytesRx": 0,
        "p1BytesTx": 0,
        "p1PacketsRx": 0,
        "p1PacketsTx": 0,
        "p2BytesRx": 0,
        "p2BytesTx": 0,
        "p2PacketsRx": 0,
        "p2PacketsTx": 0,
        "p3BytesRx": 0,
        "p3BytesTx": 0,
        "p3PacketsRx": 0,
        "p3PacketsTx": 0,
        "controlBytesRx": 16944060,
        "controlBytesTx": 21877669,
        "controlPacketsRx": 234005,
        "controlPacketsTx": 229052,
        "bpsOfBestPathRx": 376038000,
        "bpsOfBestPathTx": 5000000,
        "bestJitterMsRx": 0,
        "bestJitterMsTx": 0.017482517482517484,
        "bestLatencyMsRx": 1,
        "bestLatencyMsTx": 1,
        "bestLossPctRx": 0,
        "bestLossPctTx": 0,
        "scoreTx": 4.400000095367432,
        "scoreRx": 4.400000095367432,
        "signalStrength": 0,
        "state": "STABLE",
        "autoDualMode": 0,
        "link": {
            "id": 14444,
            "created": "2023-02-10T20:11:37.000Z",
            "edgeId": 5682,
            "logicalId": "aa:bb:cc:00:10:10:0000",
            "internalId": "afe53c50-4959-4dc4-a7fd-c3ab28b85dac",
            "interface": "GE4",
            "macAddress": null,
            "overlayType": "IPv4",
            "ipAddress": "21.21.10.2",
            "ipV6Address": "",
            "netmask": null,
            "networkSide": "WAN",
            "networkType": "ETHERNET",
            "displayName": "MPLS",
            "userOverride": 1,
            "isp": "DNIC",
            "org": "DNIC",
            "lat": 37.750999,
            "lon": -97.821999,
            "lastActive": "2024-06-15T14:00:26.000Z",
            "state": "STABLE",
            "backupState": "UNCONFIGURED",
            "linkMode": "ACTIVE",
            "vpnState": "STABLE",
            "lastEvent": "2024-05-15T20:35:36.000Z",
            "lastEventState": "STABLE",
            "alertsEnabled": 1,
            "operatorAlertsEnabled": 1,
            "serviceState": "IN_SERVICE",
            "modified": "2024-06-15T14:00:26.000Z",
            "holdingEdgeSerialNumber": null,
            "effectiveState": "STABLE"
        },
        "name": "GE4"
    }
]


