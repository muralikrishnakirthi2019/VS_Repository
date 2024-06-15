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




################################################################################################
##########################    Expected Output on vedges   ##############################################
################################################################################################



{
    "timeseries": [
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718373780000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718375509000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718377238000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718378967000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718380696000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718382425000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718384154000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718385883000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718387612000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718389341000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718391070000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718392799000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718394528000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718396257000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718397986000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718399715000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718401444000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718403173000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718404902000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718406631000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718408360000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718410089000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718411818000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718413547000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718415276000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718417005000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718418734000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718420463000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718422192000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718423921000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718425650000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718427379000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718429108000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718430837000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718432566000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718434295000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718436024000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718437753000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718439482000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718441211000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718442940000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718444669000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718446398000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718448127000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718449856000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718451585000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718453314000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718455043000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718456772000
        },
        {
            "after": {
                "0": 4,
                "1": 4,
                "2": 4
            },
            "metadata": {
                "stateMap": {
                    "0": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "1": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    },
                    "2": {
                        "0": {
                            "after": 4
                        },
                        "1": {
                            "after": 4
                        },
                        "2": {
                            "after": 4
                        },
                        "3": {
                            "after": 4
                        },
                        "4": {
                            "after": 4
                        },
                        "5": {
                            "after": 4
                        }
                    }
                }
            },
            "timestamp": 1718458501000
        }
    ],
    "distribution": {
        "0": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 1
        },
        "1": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 1
        },
        "2": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 1
        }
    },
    "score": {
        "0": 10,
        "1": 10,
        "2": 10
    },
    "totalScore": 10,
    "sampleLength": 1729000,
    "sampleCount": 50
}