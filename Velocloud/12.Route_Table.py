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

    edge_url = '/portal/rest/enterprise/getEnterpriseRouteTable'

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
    "profiles": [
        {
            "id": 8981,
            "name": "Quick Start Profile",
            "description": "Netbrain Technologies Inc"
        },
        {
            "id": 17284,
            "name": "Murali",
            "description": ""
        }
    ],
    "subnets": [
        {
            "subnet": "10.8.81.0/28:0",
            "learnedRoute": {
                "id": 2134124,
                "pinned": false,
                "description": null,
                "logicalId": "17b2a5cf-46b8-4b92-8a02-86e1d7e3f0e0",
                "cidrIp": "10.8.81.0",
                "cidrPrefix": 28,
                "modified": "2023-12-21T14:07:59.000Z",
                "created": "2023-12-21T14:07:58.000Z",
                "segmentId": 0
            },
            "preferredExits": [
                {
                    "type": "DIRECT",
                    "exitType": "ROUTER",
                    "cost": 512,
                    "learnedBy": 1
                },
                {
                    "type": "LEARNED",
                    "exitType": "EDGE",
                    "profileId": 8981,
                    "segmentId": 0,
                    "id": 36413344,
                    "routeId": 2134124,
                    "edgeId": 5681,
                    "enterpriseObjectId": null,
                    "created": "2023-12-21T14:07:58.000Z",
                    "filtered": 0,
                    "isOwner": 1,
                    "advertise": 1,
                    "protocol": "OSPF",
                    "area": 0,
                    "routeType": "OE2",
                    "cost": 4096,
                    "metric": 20,
                    "tag": null,
                    "neighborTag": null,
                    "state": "REACHABLE",
                    "entity": "HUB",
                    "interface": "GE1",
                    "neighborId": "10.8.81.254",
                    "neighborIp": "10.8.81.254",
                    "attributes": null,
                    "nextHopIp": null,
                    "modified": "2023-12-21T14:07:59.000Z",
                    "edgeName": "Velocloud-Hub",
                    "edgeLogicalId": "8df8d506-d03e-4771-9ee9-e7d2781c26a5"
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.16/28:0",
            "learnedRoute": {
                "id": 2134125,
                "pinned": false,
                "description": null,
                "logicalId": "f33e3b75-b108-463a-90d2-ed8e714ab131",
                "cidrIp": "10.8.81.16",
                "cidrPrefix": 28,
                "modified": "2023-12-21T14:07:59.000Z",
                "created": "2023-12-21T14:07:58.000Z",
                "segmentId": 0
            },
            "preferredExits": [
                {
                    "type": "DIRECT",
                    "exitType": "ROUTER",
                    "cost": 512,
                    "learnedBy": 1
                },
                {
                    "type": "LEARNED",
                    "exitType": "EDGE",
                    "profileId": 8981,
                    "segmentId": 0,
                    "id": 36413345,
                    "routeId": 2134125,
                    "edgeId": 5681,
                    "enterpriseObjectId": null,
                    "created": "2023-12-21T14:07:58.000Z",
                    "filtered": 0,
                    "isOwner": 1,
                    "advertise": 1,
                    "protocol": "OSPF",
                    "area": 0,
                    "routeType": "OE2",
                    "cost": 4096,
                    "metric": 20,
                    "tag": null,
                    "neighborTag": null,
                    "state": "REACHABLE",
                    "entity": "HUB",
                    "interface": "GE1",
                    "neighborId": "10.8.81.254",
                    "neighborIp": "10.8.81.254",
                    "attributes": null,
                    "nextHopIp": null,
                    "modified": "2023-12-21T14:07:59.000Z",
                    "edgeName": "Velocloud-Hub",
                    "edgeLogicalId": "8df8d506-d03e-4771-9ee9-e7d2781c26a5"
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "172.16.8.0/22:0",
            "learnedRoute": {
                "id": 2134126,
                "pinned": false,
                "description": null,
                "logicalId": "9108366a-7982-4eb6-977c-d606027379a9",
                "cidrIp": "172.16.8.0",
                "cidrPrefix": 22,
                "modified": "2023-12-21T14:07:59.000Z",
                "created": "2023-12-21T14:07:58.000Z",
                "segmentId": 0
            },
            "preferredExits": [
                {
                    "type": "DIRECT",
                    "exitType": "ROUTER",
                    "cost": 512,
                    "learnedBy": 1
                },
                {
                    "type": "LEARNED",
                    "exitType": "EDGE",
                    "profileId": 8981,
                    "segmentId": 0,
                    "id": 36413346,
                    "routeId": 2134126,
                    "edgeId": 5681,
                    "enterpriseObjectId": null,
                    "created": "2023-12-21T14:07:58.000Z",
                    "filtered": 0,
                    "isOwner": 1,
                    "advertise": 1,
                    "protocol": "OSPF",
                    "area": 0,
                    "routeType": "OE2",
                    "cost": 4096,
                    "metric": 20,
                    "tag": null,
                    "neighborTag": null,
                    "state": "REACHABLE",
                    "entity": "HUB",
                    "interface": "GE1",
                    "neighborId": "10.8.81.254",
                    "neighborIp": "10.8.81.254",
                    "attributes": null,
                    "nextHopIp": null,
                    "modified": "2023-12-21T14:07:59.000Z",
                    "edgeName": "Velocloud-Hub",
                    "edgeLogicalId": "8df8d506-d03e-4771-9ee9-e7d2781c26a5"
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.252/30:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5681,
                    "edgeName": "Velocloud-Hub",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.252",
                    "cidrPrefix": 30,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "192.168.29.4/32:0",
            "preferredExits": [],
            "eligableExits": [
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5681,
                    "edgeName": "Velocloud-Hub",
                    "profileId": 8981,
                    "cidrIp": "192.168.29.4",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                },
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "192.168.29.4",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                },
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "192.168.29.4",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                }
            ],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "192.168.32.17/32:0",
            "preferredExits": [],
            "eligableExits": [
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5681,
                    "edgeName": "Velocloud-Hub",
                    "profileId": 8981,
                    "cidrIp": "192.168.32.17",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                },
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "192.168.32.17",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                },
                {
                    "segmentId": 0,
                    "type": "STATIC",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "192.168.32.17",
                    "cidrPrefix": "32",
                    "cost": 0,
                    "vlanId": null,
                    "advertise": false
                }
            ],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.10.56.0/24:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "10.10.56.0",
                    "cidrPrefix": 24,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.32/28:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.32",
                    "cidrPrefix": 28,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.48/28:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.48",
                    "cidrPrefix": 28,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.250/32:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.250",
                    "cidrPrefix": 32,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.248/32:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5682,
                    "edgeName": "Velocloud-Branch1",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.248",
                    "cidrPrefix": 32,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.10.57.0/24:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "10.10.57.0",
                    "cidrPrefix": 24,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.64/28:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.64",
                    "cidrPrefix": 28,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.80/28:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.80",
                    "cidrPrefix": 28,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.251/32:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.251",
                    "cidrPrefix": 32,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        },
        {
            "subnet": "10.8.81.249/32:0",
            "preferredExits": [
                {
                    "segmentId": 0,
                    "type": "CONNECTED",
                    "exitType": "EDGE",
                    "edgeId": 5698,
                    "edgeName": "Velocloud-Branch2",
                    "profileId": 8981,
                    "cidrIp": "10.8.81.249",
                    "cidrPrefix": 32,
                    "cost": 10,
                    "advertise": true
                }
            ],
            "eligableExits": [],
            "ipVersion": "IPv4"
        }
    ]
}