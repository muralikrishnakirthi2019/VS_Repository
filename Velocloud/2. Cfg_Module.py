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
    edge_url = '/portal/rest/edge/getEdgeConfigurationModules'
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
    "deviceSettings": {
        "version": "1713974826900",
        "schemaVersion": "3.0.0",
        "type": "ENTERPRISE",
        "data": {
            "snmp": {
                "port": 161,
                "snmpv2c": {
                    "community": "nb",
                    "allowedIp": [],
                    "enabled": true,
                    "communityList": [
                        "nb"
                    ]
                },
                "snmpv3": {
                    "users": [
                        {
                            "name": "admin",
                            "passphrase": "velocloud",
                            "authAlg": "MD5",
                            "privacy": false,
                            "encrAlg": "DES",
                            "authentication": true
                        }
                    ],
                    "enabled": false
                }
            },
            "routedInterfaces": [
                {
                    "name": "GE3",
                    "disabled": false,
                    "addressing": {
                        "netmask": "255.255.255.0",
                        "type": "STATIC",
                        "gateway": "192.168.180.1",
                        "cidrIp": "192.168.180.241",
                        "cidrPrefix": 24
                    },
                    "wanOverlay": "AUTO_DISCOVERED",
                    "natDirect": false,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "evdslModemAttached": null,
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "rpf": "SPECIFIC",
                    "dhcpServer": {
                        "enabled": false,
                        "leaseTimeSeconds": 3600,
                        "options": [],
                        "baseDhcpAddr": 2,
                        "numDhcpAddr": 254,
                        "staticReserved": 10
                    },
                    "dnsProxy": false
                },
                {
                    "name": "GE4",
                    "disabled": false,
                    "wanOverlay": "USER_DEFINED",
                    "natDirect": true,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "rpf": "SPECIFIC",
                    "dhcpServer": {
                        "enabled": false,
                        "leaseTimeSeconds": 3600,
                        "options": [],
                        "baseDhcpAddr": "",
                        "numDhcpAddr": 0,
                        "staticReserved": 10
                    },
                    "addressing": {
                        "type": "STATIC",
                        "cidrPrefix": 24,
                        "cidrIp": "21.21.10.2",
                        "netmask": "255.255.255.0",
                        "gateway": null,
                        "username": null,
                        "password": null
                    },
                    "advertise": true,
                    "dnsProxy": false
                },
                {
                    "name": "GE5",
                    "disabled": false,
                    "addressing": {
                        "type": "DHCP",
                        "cidrPrefix": null,
                        "cidrIp": null,
                        "netmask": null,
                        "gateway": null,
                        "username": null,
                        "password": null
                    },
                    "wanOverlay": "AUTO_DISCOVERED",
                    "natDirect": true,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "trusted": false,
                        "rpf": "SPECIFIC",
                        "natDirect": true,
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "rpf": "SPECIFIC",
                    "dnsProxy": false,
                    "subinterfaces": []
                },
                {
                    "name": "GE6",
                    "disabled": false,
                    "addressing": {
                        "type": "DHCP",
                        "cidrPrefix": null,
                        "cidrIp": null,
                        "netmask": null,
                        "gateway": null,
                        "username": null,
                        "password": null
                    },
                    "wanOverlay": "AUTO_DISCOVERED",
                    "natDirect": true,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "trusted": false,
                        "rpf": "SPECIFIC",
                        "natDirect": true,
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "dnsProxy": false,
                    "subinterfaces": []
                },
                {
                    "name": "GE7",
                    "disabled": false,
                    "addressing": {
                        "type": "DHCP",
                        "cidrPrefix": null,
                        "cidrIp": null,
                        "netmask": null,
                        "gateway": null,
                        "username": null,
                        "password": null
                    },
                    "wanOverlay": "AUTO_DISCOVERED",
                    "natDirect": true,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "trusted": false,
                        "rpf": "SPECIFIC",
                        "natDirect": true,
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "dnsProxy": false,
                    "subinterfaces": []
                },
                {
                    "name": "GE8",
                    "disabled": false,
                    "addressing": {
                        "type": "DHCP",
                        "cidrPrefix": null,
                        "cidrIp": null,
                        "netmask": null,
                        "gateway": null,
                        "username": null,
                        "password": null
                    },
                    "wanOverlay": "AUTO_DISCOVERED",
                    "natDirect": true,
                    "pingResponse": true,
                    "encryptOverlay": true,
                    "ospf": {
                        "enabled": false,
                        "area": 0,
                        "authentication": false,
                        "authId": 0,
                        "authPassphrase": "",
                        "helloTimer": 10,
                        "deadTimer": 40,
                        "mode": "BCAST",
                        "md5Authentication": false,
                        "cost": 1,
                        "MTU": 1380,
                        "passive": false,
                        "inboundRouteLearning": {
                            "defaultAction": "LEARN",
                            "filters": []
                        },
                        "outboundRouteAdvertisement": {
                            "defaultAction": "IGNORE",
                            "filters": []
                        }
                    },
                    "vlanId": null,
                    "segmentId": -1,
                    "l2": {
                        "autonegotiation": true,
                        "speed": "100M",
                        "duplex": "FULL",
                        "MTU": 1500,
                        "losDetection": false,
                        "probeInterval": "3"
                    },
                    "disableV4": false,
                    "disableV6": true,
                    "overlayPreference": "IPv4",
                    "v6Detail": {
                        "addressing": {
                            "cidrPrefix": null,
                            "netmask": null,
                            "type": "DHCP_STATELESS",
                            "gateway": null,
                            "cidrIp": null
                        },
                        "wanOverlay": "AUTO_DISCOVERED",
                        "trusted": false,
                        "rpf": "SPECIFIC",
                        "natDirect": true,
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "helloTimer": 10,
                            "mode": "BCAST",
                            "deadTimer": 40,
                            "enableBfd": false,
                            "cost": 1,
                            "MTU": 1380,
                            "passive": false,
                            "inboundRouteLearning": {
                                "defaultAction": "LEARN",
                                "filters": []
                            },
                            "outboundRouteAdvertisement": {
                                "defaultAction": "IGNORE",
                                "filters": []
                            }
                        }
                    },
                    "underlayAccounting": true,
                    "radiusAuthentication": {
                        "enabled": false,
                        "macBypass": [],
                        "aclCheck": false
                    },
                    "multicast": {
                        "igmp": {
                            "enabled": false,
                            "type": "IGMP_V2"
                        },
                        "pim": {
                            "enabled": false,
                            "type": "PIM_SM"
                        },
                        "pimHelloTimerSeconds": null,
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "dnsProxy": false,
                    "subinterfaces": []
                }
            ],
            "loopbackInterfaces": {
                "LO1": {
                    "cidrIp": "10.8.81.250",
                    "cidrPrefix": 32,
                    "segmentId": 0,
                    "pingResponse": true,
                    "advertise": true,
                    "disableV4": false,
                    "disableV6": true,
                    "ospf": {
                        "enabled": false,
                        "area": []
                    },
                    "v6Detail": {
                        "cidrIp": "",
                        "cidrPrefix": 128,
                        "advertise": true,
                        "ospf": {
                            "enabled": false,
                            "area": []
                        }
                    }
                },
                "LO10": {
                    "cidrIp": "10.8.81.248",
                    "cidrPrefix": 32,
                    "segmentId": 0,
                    "pingResponse": true,
                    "advertise": true,
                    "disableV4": false,
                    "disableV6": true,
                    "ospf": {
                        "enabled": false,
                        "area": []
                    },
                    "v6Detail": {
                        "cidrIp": "",
                        "cidrPrefix": 128,
                        "advertise": true,
                        "ospf": {
                            "enabled": false,
                            "area": []
                        }
                    }
                }
            },
            "autoSimSwitchover": {
                "enabled": false,
                "switchoverInterval": 60
            },
            "vnfs": {
                "edge": {
                    "ref": "deviceSettings:vnfs:edge",
                    "logicalId": "6bbb51a1-d82c-4715-a5f1-e8efa9d7ea27"
                },
                "hasVnfs": true,
                "info": {
                    "msg": [
                        "deviceSettings security VNF not found"
                    ]
                }
            },
            "lan": {
                "interfaces": [
                    {
                        "space": "Corporate Network",
                        "name": "GE1",
                        "type": "wired",
                        "cwp": false,
                        "portMode": "trunk",
                        "vlanIds": [
                            10,
                            20
                        ],
                        "untaggedVlan": "drop",
                        "disabled": false,
                        "l2": {
                            "autonegotiation": true,
                            "speed": "100M",
                            "duplex": "FULL",
                            "MTU": 1500,
                            "losDetection": false,
                            "probeInterval": "3"
                        },
                        "override": true
                    },
                    {
                        "name": "GE2",
                        "type": "wired",
                        "cwp": false,
                        "portMode": "access",
                        "vlanIds": [
                            1
                        ],
                        "disabled": false,
                        "l2": {
                            "autonegotiation": true,
                            "speed": "100M",
                            "duplex": "FULL",
                            "MTU": 1500,
                            "losDetection": false,
                            "probeInterval": "3"
                        }
                    }
                ],
                "networks": [
                    {
                        "vlanId": 1,
                        "name": "Corporate",
                        "segmentId": 0,
                        "disabled": false,
                        "advertise": true,
                        "pingResponse": true,
                        "cost": 10,
                        "cidrIp": "10.10.56.1",
                        "cidrPrefix": 24,
                        "netmask": "255.255.255.0",
                        "dhcp": {
                            "enabled": true,
                            "leaseTimeSeconds": 86400,
                            "dhcpRelay": {
                                "enabled": false,
                                "servers": [],
                                "sourceFromSecondaryIp": false
                            },
                            "options": []
                        },
                        "staticReserved": 10,
                        "baseDhcpAddr": 13,
                        "numDhcpAddr": 242,
                        "disableV4": false,
                        "disableV6": true,
                        "v6Detail": {
                            "override": true,
                            "advertise": true,
                            "addressing": {
                                "cidrIp": null,
                                "cidrPrefix": 64,
                                "netmask": "ffff:ffff:ffff:ffff:0000:0000:0000:0000"
                            },
                            "dhcpServer": {
                                "enabled": true,
                                "leaseTimeSeconds": 86400,
                                "options": [],
                                "prefixDelegation": {
                                    "enabled": true,
                                    "pdlist": []
                                },
                                "baseDhcpAddr": 1,
                                "numDhcpAddr": 10,
                                "staticReserved": 10,
                                "fixedIp": []
                            },
                            "ospf": {
                                "enabled": false,
                                "area": "",
                                "passiveInterface": true
                            },
                            "bindEdgeAddress": false
                        },
                        "interfaces": [
                            "GE2"
                        ],
                        "multicast": {
                            "igmp": {
                                "enabled": false,
                                "type": "IGMP_V2"
                            },
                            "pim": {
                                "enabled": false,
                                "type": "PIM_SM"
                            },
                            "pimHelloTimerSeconds": null,
                            "pimKeepAliveTimerSeconds": null,
                            "pimPruneIntervalSeconds": null,
                            "igmpHostQueryIntervalSeconds": null,
                            "igmpMaxQueryResponse": null
                        },
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "passiveInterface": true
                        },
                        "dnsProxy": true,
                        "radiusAuthentication": {
                            "enabled": false,
                            "macBypass": [],
                            "aclCheck": false
                        },
                        "bindEdgeAddress": false,
                        "vnfInsertion": null
                    },
                    {
                        "vlanId": 10,
                        "name": "Branch1-Host_VLAN10",
                        "segmentId": 0,
                        "advertise": true,
                        "pingResponse": true,
                        "cost": 10,
                        "cidrIp": "10.8.81.33",
                        "disableV4": false,
                        "disableV6": true,
                        "cidrPrefix": 28,
                        "netmask": "255.255.255.240",
                        "dhcp": {
                            "enabled": true,
                            "leaseTimeSeconds": 86400,
                            "options": [],
                            "override": true,
                            "dhcpRelay": {
                                "enabled": false,
                                "servers": [],
                                "sourceFromSecondaryIp": false
                            }
                        },
                        "staticReserved": 10,
                        "baseDhcpAddr": 9,
                        "multicast": {
                            "igmp": {
                                "enabled": false,
                                "type": "IGMP_V2"
                            },
                            "pim": {
                                "enabled": false,
                                "type": "PIM_SM"
                            },
                            "pimHelloTimerSeconds": null,
                            "pimKeepAliveTimerSeconds": null,
                            "pimPruneIntervalSeconds": null,
                            "igmpHostQueryIntervalSeconds": null,
                            "igmpMaxQueryResponse": null
                        },
                        "numDhcpAddr": 6,
                        "v6Detail": {
                            "override": true,
                            "advertise": true,
                            "addressing": {
                                "cidrIp": null,
                                "cidrPrefix": 64,
                                "netmask": "ffff:ffff:ffff:ffff:0000:0000:0000:0000"
                            },
                            "dhcpServer": {
                                "enabled": true,
                                "leaseTimeSeconds": 86400,
                                "options": [],
                                "prefixDelegation": {
                                    "enabled": true,
                                    "pdlist": []
                                },
                                "baseDhcpAddr": 1,
                                "numDhcpAddr": 10,
                                "staticReserved": 10,
                                "fixedIp": []
                            },
                            "ospf": {
                                "enabled": false,
                                "area": "",
                                "passiveInterface": true
                            },
                            "bindEdgeAddress": false
                        },
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "passiveInterface": true,
                            "override": true
                        },
                        "override": true,
                        "fixedIp": [],
                        "disabled": false,
                        "interfaces": [
                            "GE1"
                        ],
                        "dnsProxy": true,
                        "radiusAuthentication": {
                            "enabled": false,
                            "macBypass": [],
                            "aclCheck": false
                        },
                        "bindEdgeAddress": false,
                        "vnfInsertion": null
                    },
                    {
                        "vlanId": 20,
                        "name": "Branch1-Host_VLAN20",
                        "segmentId": 0,
                        "advertise": true,
                        "pingResponse": true,
                        "cost": 10,
                        "cidrIp": "10.8.81.49",
                        "disableV4": false,
                        "disableV6": true,
                        "cidrPrefix": 28,
                        "netmask": "255.255.255.240",
                        "dhcp": {
                            "enabled": true,
                            "leaseTimeSeconds": 86400,
                            "options": [],
                            "override": true,
                            "dhcpRelay": {
                                "enabled": false,
                                "servers": [],
                                "sourceFromSecondaryIp": false
                            }
                        },
                        "staticReserved": 10,
                        "baseDhcpAddr": 9,
                        "multicast": {
                            "igmp": {
                                "enabled": false,
                                "type": "IGMP_V2"
                            },
                            "pim": {
                                "enabled": false,
                                "type": "PIM_SM"
                            },
                            "pimHelloTimerSeconds": null,
                            "pimKeepAliveTimerSeconds": null,
                            "pimPruneIntervalSeconds": null,
                            "igmpHostQueryIntervalSeconds": null,
                            "igmpMaxQueryResponse": null
                        },
                        "numDhcpAddr": 6,
                        "v6Detail": {
                            "override": true,
                            "advertise": true,
                            "addressing": {
                                "cidrIp": null,
                                "cidrPrefix": 64,
                                "netmask": "ffff:ffff:ffff:ffff:0000:0000:0000:0000"
                            },
                            "dhcpServer": {
                                "enabled": true,
                                "leaseTimeSeconds": 86400,
                                "options": [],
                                "prefixDelegation": {
                                    "enabled": true,
                                    "pdlist": []
                                },
                                "baseDhcpAddr": 1,
                                "numDhcpAddr": 10,
                                "staticReserved": 10,
                                "fixedIp": []
                            },
                            "ospf": {
                                "enabled": false,
                                "area": "",
                                "passiveInterface": true
                            },
                            "bindEdgeAddress": false
                        },
                        "ospf": {
                            "enabled": false,
                            "area": "",
                            "passiveInterface": true,
                            "override": true
                        },
                        "override": true,
                        "fixedIp": [],
                        "disabled": false,
                        "interfaces": [
                            "GE1"
                        ],
                        "dnsProxy": true,
                        "radiusAuthentication": {
                            "enabled": false,
                            "macBypass": [],
                            "aclCheck": false
                        },
                        "bindEdgeAddress": false,
                        "vnfInsertion": null
                    }
                ],
                "visibility": {
                    "override": false,
                    "mode": "MAC"
                },
                "management": {
                    "cidrIp": "192.168.1.1",
                    "cidrPrefix": 32
                },
                "managementTraffic": {
                    "override": true,
                    "sourceInterface": ""
                }
            },
            "ha": {
                "vmacoverride": false,
                "enabled": false,
                "interface": "GE1"
            },
            "segments": [
                {
                    "segment": {
                        "segmentId": 0,
                        "name": "Global Segment",
                        "type": "REGULAR",
                        "segmentLogicalId": "2da3af62-748d-4d8e-a64c-2db579f3e974",
                        "serviceVlan": null
                    },
                    "routes": {
                        "static": [
                            {
                                "destination": "192.168.29.4",
                                "netmask": "255.255.255.255",
                                "sourceIp": null,
                                "gateway": "192.168.180.1",
                                "cost": 0,
                                "preferred": true,
                                "description": "",
                                "cidrPrefix": "32",
                                "wanInterface": "GE3",
                                "subinterfaceId": -1,
                                "icmpProbeLogicalId": null,
                                "vlanId": null,
                                "advertise": false
                            },
                            {
                                "destination": "192.168.32.17",
                                "netmask": "255.255.255.255",
                                "sourceIp": null,
                                "gateway": "192.168.180.1",
                                "cost": 0,
                                "preferred": true,
                                "description": "",
                                "cidrPrefix": "32",
                                "wanInterface": "GE3",
                                "subinterfaceId": -1,
                                "icmpProbeLogicalId": null,
                                "vlanId": null,
                                "advertise": false
                            }
                        ],
                        "staticV6": [],
                        "nsd": [],
                        "nsdV6": [],
                        "icmpResponders": [],
                        "icmpProbes": []
                    },
                    "analyticsSettings": {
                        "analyticsEnabled": false,
                        "sourceInterface": null
                    },
                    "secureAccess": {
                        "enabled": false,
                        "provider": {
                            "ref": "deviceSettings:secureAccess:provider",
                            "logicalId": ""
                        },
                        "override": false
                    },
                    "bgp": {
                        "enabled": true,
                        "ASN": "65502",
                        "routerId": "2.2.2.2",
                        "networks": [],
                        "holdtime": null,
                        "keepalive": null,
                        "enableGracefulRestart": false,
                        "connectedRoutes": true,
                        "overlayPrefix": true,
                        "propagateUplink": false,
                        "uplinkCommunity": null,
                        "disableASPathCarryOver": false,
                        "ospf": {
                            "enabled": false,
                            "metric": 20
                        },
                        "defaultRoute": {
                            "enabled": false,
                            "advertise": "CONDITIONAL"
                        },
                        "neighbors": [
                            {
                                "neighborIp": "21.21.20.2",
                                "neighborAS": "65503",
                                "inboundFilter": {
                                    "rules": [
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "10.8.81.0/28",
                                                "exactMatch": true
                                            },
                                            "action": {
                                                "type": "PERMIT",
                                                "values": [
                                                    {
                                                        "type": "NONE",
                                                        "value": ""
                                                    }
                                                ],
                                                "communityAdditive": false
                                            }
                                        },
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "10.8.81.16/28",
                                                "exactMatch": true
                                            },
                                            "action": {
                                                "type": "PERMIT",
                                                "values": [
                                                    {
                                                        "type": "NONE",
                                                        "value": ""
                                                    }
                                                ],
                                                "communityAdditive": false
                                            }
                                        },
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "10.8.81.80/28",
                                                "exactMatch": true
                                            },
                                            "action": {
                                                "type": "PERMIT",
                                                "values": [
                                                    {
                                                        "type": "NONE",
                                                        "value": ""
                                                    }
                                                ],
                                                "communityAdditive": false
                                            }
                                        },
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "0.0.0.0/0",
                                                "exactMatch": false
                                            },
                                            "action": {
                                                "type": "DENY",
                                                "values": [],
                                                "communityAdditive": false
                                            }
                                        }
                                    ],
                                    "filterNames": [
                                        "inbound"
                                    ],
                                    "filterNamesHash": "0b1276a9a74ea10002d3274de437f0a252b5a459"
                                },
                                "outboundFilter": {
                                    "rules": [
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "10.8.81.48/28",
                                                "exactMatch": true
                                            },
                                            "action": {
                                                "type": "PERMIT",
                                                "values": [
                                                    {
                                                        "type": "NONE",
                                                        "value": ""
                                                    }
                                                ],
                                                "communityAdditive": false
                                            }
                                        },
                                        {
                                            "match": {
                                                "type": "PREFIX",
                                                "value": "10.8.81.32/28",
                                                "exactMatch": true
                                            },
                                            "action": {
                                                "type": "DENY",
                                                "values": [],
                                                "communityAdditive": false
                                            }
                                        }
                                    ],
                                    "filterNames": [
                                        "outbound"
                                    ],
                                    "filterNamesHash": "e342b4b1cc12f5bb907bb1e854c3ee681e061c61"
                                },
                                "id": "d7179833-edfc-4bd6-9d21-bb695f82b0c4"
                            }
                        ],
                        "v6Detail": {
                            "networks": [],
                            "connectedRoutes": true,
                            "defaultRoute": {
                                "enabled": false,
                                "advertise": "CONDITIONAL"
                            },
                            "overlayPrefix": true,
                            "disableASPathCarryOver": false,
                            "propagateUplink": false,
                            "ospf": {
                                "enabled": false,
                                "metric": 20
                            },
                            "neighbors": [],
                            "aggregation": []
                        },
                        "aggregation": []
                    },
                    "authentication": {
                        "sourceInterface": ""
                    },
                    "netflow": {
                        "enabled": false,
                        "version": 10,
                        "collectors": [],
                        "intervals": {
                            "flowStats": 60,
                            "flowLinkStats": 60,
                            "tunnelStats": 60,
                            "vrfTable": 300,
                            "applicationTable": 300,
                            "interfaceTable": 300,
                            "linkTable": 300
                        }
                    },
                    "ospf": {
                        "enabled": true,
                        "aggregation": [],
                        "areas": [
                            {
                                "id": 0,
                                "name": "",
                                "type": "normal"
                            }
                        ],
                        "defaultRoutes": "NONE",
                        "defaultRouteAdvertise": "NONE",
                        "defaultPrefixes": true,
                        "bgp": {
                            "enabled": false,
                            "metric": 20,
                            "metricType": "E2"
                        },
                        "v6Detail": {
                            "enabled": false,
                            "aggregation": [],
                            "areas": [],
                            "defaultRoutes": "NONE",
                            "defaultRouteAdvertise": "NONE",
                            "defaultPrefixes": true,
                            "bgp": {
                                "enabled": false,
                                "metric": 20,
                                "metricType": "E2"
                            }
                        }
                    },
                    "natRules": [],
                    "dualNatRules": [],
                    "handOffGateways": {
                        "autoSelect": false,
                        "gatewayList": [],
                        "gateways": []
                    },
                    "handOffControllers": {
                        "autoSelect": false,
                        "gatewayList": [],
                        "gateways": []
                    },
                    "vqm": {
                        "enabled": false,
                        "protocol": "RFC6035",
                        "collectors": [
                            {
                                "address": "",
                                "port": 4739
                            }
                        ]
                    },
                    "dns": {
                        "primaryProvider": {
                            "primary": "8.8.8.8",
                            "secondary": "8.8.4.4",
                            "ipv4Servers": [
                                "8.8.8.8",
                                "8.8.4.4"
                            ],
                            "ipv6Servers": [
                                "2001:4860:4860::8888",
                                "2001:4860:4860::8844"
                            ],
                            "name": "Google"
                        },
                        "backupProvider": {},
                        "privateProviders": {},
                        "sourceInterface": "",
                        "localDNS": []
                    },
                    "snmp": {
                        "port": 161,
                        "snmpv2c": {
                            "enabled": false,
                            "community": "",
                            "allowedIp": []
                        },
                        "snmpv3": {
                            "enabled": false,
                            "users": [
                                {
                                    "name": "admin",
                                    "passphrase": "velocloud",
                                    "authAlg": "MD5",
                                    "privacy": false,
                                    "encrAlg": "DES"
                                }
                            ]
                        }
                    },
                    "ntp": {
                        "enabled": false,
                        "servers": []
                    },
                    "multicast": {
                        "enabled": false,
                        "rp": {
                            "type": "STATIC",
                            "staticGroups": []
                        },
                        "pimOnWanOverlay": {
                            "enabled": false,
                            "type": "SOURCE_IP",
                            "sourceCidrIp": null,
                            "sourceInterface": null
                        },
                        "pimKeepAliveTimerSeconds": null,
                        "pimPruneIntervalSeconds": null,
                        "igmpHostQueryIntervalSeconds": null,
                        "igmpMaxQueryResponse": null
                    },
                    "hubInterconnect": {
                        "enabled": false
                    },
                    "syslog": {
                        "enabled": false,
                        "collectors": [],
                        "facilityCode": "local0"
                    },
                    "bfd": {
                        "enabled": false,
                        "rules": [],
                        "rulesV6": []
                    }
                }
            ],
            "zscaler": {
                "config": {
                    "override": true,
                    "enabled": false,
                    "vendor": "zscaler",
                    "cloud": "",
                    "provider": {
                        "ref": null,
                        "logicalId": null
                    },
                    "location": {
                        "name": null
                    },
                    "subLocations": []
                },
                "deployment": {
                    "location": {},
                    "mtgreSite": {},
                    "subLocations": []
                }
            },
            "softwareUpdate": {
                "windowed": false,
                "window": {
                    "day": 6,
                    "beginHour": 17,
                    "endHour": 23
                }
            },
            "radioSettings": {
                "country": "auto",
                "radios": [
                    {
                        "radioId": 0,
                        "isEnabled": true,
                        "name": "Radio1",
                        "band": "2.4",
                        "channel": "auto",
                        "width": "auto",
                        "mode": "n"
                    }
                ]
            },
            "l2Settings": {
                "overrideARPTimeout": false,
                "arpStaleTimeoutMinutes": 2,
                "arpDeadTimeoutMinutes": 25,
                "arpCleanupTimeoutMinutes": 240
            },
            "globalIPv6Settings": {
                "advancedConfiguration": {
                    "disableAllIPv6Traffic": false,
                    "dropRoutingHeaderTypeZeroPackets": false,
                    "enforceExtensionHeaderValidation": false,
                    "enforceExtensionHeaderOrderCheck": false,
                    "dropnLogPacketsForRFCReservedFields": false
                },
                "icmpV6Messages": {
                    "disableDestinationUnreachable": false,
                    "disableTimeExceeded": false,
                    "disableParameterProblem": false
                }
            },
            "ntp": {
                "enabled": false,
                "sourceInterface": "",
                "servers": []
            },
            "ntpServer": {
                "enabled": false,
                "authentication": "NONE",
                "keys": []
            },
            "ccFirewall": {
                "enabled": false
            }
        }
    }
}