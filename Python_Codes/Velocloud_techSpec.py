#PYTHON:



import json
import re
import traceback
import sys
import time
from functools import wraps

from netbrain.common.models import RouteTable, NCTTable, NCTStatus
from netbrain.common.models import IP, IsIP
from netbrain.sysapi.datamodel import GetDeviceSetting, SetDeviceSetting, QueryNodeObjects
from netbrain.driver.common import function
from netbrain.techspec.models.base import TechSpecBase
from netbrain.techspec.common.enums import LOGICAL_TOPO_TYPE
from netbrain.techspec.common.lib import create_device_object
from netbrain.techspec.common.requestmgr import NBRequests
from netbrain.lib.datamodel import SetDeviceCredential
from netbrain.techspec.common.SimpleCache import SimpleCache
from netbrain.techspec.common.httputil import post as new_post
from netbrain.lib import datamodel
from netbrain.lib.datamodel import GetInterfacesByDevice, GetInterfaceProperty
from netbrain.techspec.common.utils import TableParams
from netbrain.lib.devicedata import GetCLIData
import copy


IS_WORKER_SIDE = False
try:
    import CDBHelper
    import PyDataModel
    IS_WORKER_SIDE = True
except ImportError:
    import pythonutil

# for testing only
DEVICE_FILTER = []

_is_debug = False   # set to True when enable debug.

def debug_print(*args, **kwargs):
    if _is_debug:
        print(*args, **kwargs)

def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_child_by_path(parent_obj, path):
    try:
        obj = parent_obj
        for sub_path in path.split('.'):
            if isinstance(obj, list):
                obj = obj[int(sub_path)]
            else:
                obj = obj[sub_path]
        return obj
    except:
        error_print(traceback.format_exc())
        return False

# A simple decorator
def debugthis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        debug_print('start run function:%s with args:%s, kwargs:%s' % (func.__name__, str(args), str(kwargs)))
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        debug_print('execute time is:%s' % str(end-start))
        debug_print('finish run function:%s with args:%s, kwargs:%s' % (func.__name__, str(args), str(kwargs)))
        return r
    return wrapper

root_schema = 'VELOCLOUD'
gateway_schema = 'VELOCLOUD.NetworkGateways.gateway'
gateway_port_schema = 'VELOCLOUD.NetworkGateways.gateway.port'
edge_schema = 'VELOCLOUD.WANEdges.edge'
edge_port_schema = 'VELOCLOUD.WANEdges.edge.links.interface'
vco_schema = 'VELOCLOUD.vco'
NAME_MAXIMUM_LENGTH = 60

SNMPv3_authPros = {
    'MD5': 1,
    'SHA': 2,
    'SHA224': 3,
    'SHA256': 4,
    'SHA384': 5,
    'SHA512': 6
    }

SNMPv3_encryptPros = {
    'DES': 1,
    'AES': 2,
    'AES192': 3,
    'AES256': 4
    }

class VCRequest:

    def __init__(self, endpoint_url, user, pwd, proxies=None, is_operator=False):

        self._cache_token = SimpleCache.getInstance()
        self._max_token_time = 600
        self.nb_request = NBRequests(endpoint_url)
        self.endpoint_url = endpoint_url
        self.user = user
        self.pwd = pwd
        self.is_operator = is_operator
        self.proxies = proxies
        if self.proxies:
            self.nb_request.set_request_params(**{'proxies': self.proxies})

    def get_authen_headers(self, msg=None):
        header = {}
        try_cache_cookie = self._cache_token.get(self.endpoint_url + self.user + self.pwd, None)
        if try_cache_cookie:
            header['Cookie'] = try_cache_cookie['value']
            return {'headers' : header}

        if self.is_operator:
            # operator login
            login_url = '/portal/rest/login/operatorLogin'
        else:
            # enterprise login
            login_url = '/portal/rest/login/enterpriseLogin'
        body = {
            "password": self.pwd,
            "username": self.user
        }
        if not msg:
            msg = []
        try:
            res = self.nb_request.post(self.endpoint_url + login_url, data=json.dumps(body))
            if res.status_code == 200 and not res.text.startswith('<html>') and 'Set-Cookie' in res.headers:
                header = {
                    'Cookie': res.headers['Set-Cookie']
                }
                _last_token_time = time.time()
                self._cache_token.set(self.endpoint_url + self.user + self.pwd, {
                    'value': res.headers['Set-Cookie'],
                    'time': _last_token_time,
                    'ttl': self._max_token_time - 30
                })
                return {'headers' : header}
        except Exception as e:
            error_log = 'Failed to get cookie headers, with error:%s'%str(e)
            error_log += traceback.format_exc()
            debug_print('error_log', error_log)
            msg.append(error_log)
        return {}

def get_normal_name(name):
    if not name:
        return ''
    lst = name.lstrip().rstrip().split(' ')
    name = '_'.join(lst)
    result = name
    len1 = len(name)
    if len1 > NAME_MAXIMUM_LENGTH:
        result = name[0:NAME_MAXIMUM_LENGTH].lstrip().rstrip()
    return result


# Define tech class inherited from TechSpecBase
class TechSpecVC(TechSpecBase):

    def __init__(self, endpoint_url, user, pwd, params):
        super().__init__(endpoint_url, user, pwd, params)
        self._technology = 'VELOCLOUD'
        self._tenant_db_name = params[1]
        self._domain_db_name = params[2]
        self._url = endpoint_url
        self._external_server_id = ''
        self._ap_id = ''
        self._tech_id = ''
        # proxy
        self._proxy_info = None
        self.proxies = {}
        self.is_operator = False
        self.has_cli = False
        self.prefer_private_wired_as_mgmt_ip = False
        self.autoset_snmp = False
        self.prefer_cli_for_ipsec = False
        self.prefer_loopback_as_mgmt_ip = False
        self.loopback_priority_sequence = ''
        self.lan_preferential_order = ''
        
        # use to adjust default discover behavior
        # by default,self.adjust_default_discover_behavior is set to False
        self.adjust_default_discover_behavior = False
        # only self.adjust_default_discover_behavior is set to True, the following 3 settings will take affect
        # the 3 settings could be combined together. 
        # in the scenarios that mutiple conditions are set, AND logic is used.
        self.solo_scan_edges = []
        self.solo_scan_enterprises = []
        self.discover_new_appliance_only = False
        self.existing_appliance_list = []
        
        # extra params
        self._extra_info = None
        if params is not None and len(params) == 8:
            proxy_param = params[4]
            # isEnabled,ip,port,username, password
            if proxy_param != "" and proxy_param != "{}":
                self._proxy_info = json.loads(proxy_param)
            extra_params = params[5]
            # {key:value,...}
            if extra_params != "" and extra_params != "{}":
                self._extra_info = json.loads(extra_params)
        if params:
            param = params
            if isinstance(param, str):
                param = json.loads(param)

            if 'apis' in param:
                apis = param['apis']
                for rootSchema in apis:
                    if rootSchema == 'VELOCLOUD':
                        tech_param = apis[rootSchema]
                        if 'extraParams' in tech_param:
                            if isinstance(tech_param['extraParams'], str):
                                self._extra_info = json.loads(tech_param['extraParams'])
                            else:
                                self._extra_info = tech_param['extraParams']
                        break
            else:
                if 'extraParams' in param:
                    if isinstance(param['extraParams'], str):
                        self._extra_info = json.loads(param['extraParams'])
                    else:
                        self._extra_info = param['extraParams']

        # update extra params
        if self._extra_info is not None:
            extra_paras = parse_extra_params(self._extra_info)
            self.proxies = extra_paras.get('proxies','')
            self.is_operator = extra_paras.get('is_operator') or False
            self.has_cli = extra_paras.get('has_cli') or False
            self.prefer_private_wired_as_mgmt_ip = extra_paras.get('prefer_private_wired_as_mgmt_ip') or False
            self.autoset_snmp = extra_paras.get('autoset_snmp') or False
            self.prefer_cli_for_ipsec = extra_paras.get('prefer_cli_for_ipsec') or False
            self.prefer_loopback_as_mgmt_ip = extra_paras.get('prefer_loopback_as_mgmt_ip') or False
            self.loopback_priority_sequence = extra_paras.get('loopback_priority_sequence','')
            self.lan_preferential_order = extra_paras.get('lan_preferential_order','')
            
            self.adjust_default_discover_behavior = extra_paras.get('adjust_default_discover_behavior') or False
            self.solo_scan_edges = extra_paras.get('solo_scan_edges') or []
            self.solo_scan_enterprises = extra_paras.get('solo_scan_enterprises') or []
            self.discover_new_appliance_only = extra_paras.get('discover_new_appliance_only') or False

        # print('self._extra_info', self._extra_info)
        # print('proxies from extra_info', self.proxies)
        # config proxy
        if self._proxy_info is not None and self._proxy_info['isEnabled']:
            proxy_url = ''
            if self._proxy_info['username'] == '':
                proxy_url = 'http://{0}:{1}'.format(self._proxy_info['ip'], self._proxy_info['port'])
            else:
                proxy_url = 'http://{0}:{1}@{2}:{3}'.format(
                    self._proxy_info['username'], self._proxy_info['password'],
                    self._proxy_info['ip'], self._proxy_info['port'])

            self.proxies = {'http': proxy_url, 'https': proxy_url.replace('http', 'https')}
            # print('proxies from proxy_info', self.proxies)

        ip = endpoint_url.rpartition('://')[2].partition('/')[0].partition(':')[0]
        query_condition = json.dumps({'ip': ip})
        server_res = PyDataModel.QueryDataFromDB(self._domain_db_name, 'ExternalAPIServer', query_condition)
        if server_res:
            try:
                server_res = self.normalize_json_string(server_res)
                server_res = json.loads(server_res)
                server = server_res[0]
            except:
                server_res = PyDataModel.QueryDataFromDB(self._tenant_db_name, 'ExternalAPIServer', query_condition)
                server_res = self.normalize_json_string(server_res)
                server_res = json.loads(server_res)
                server = server_res[0]
            if server:
                self._external_server_id = server['_id']
                self._ap_id = server['frontServerAndGroupId']
                self._tech_id = server['serverTypeId']

        #common_endpoint_url = endpoint_url
        # initial Request
        self.vc_request = VCRequest(endpoint_url, user, pwd, proxies=self.proxies, is_operator=self.is_operator)
        self.request = self.vc_request.nb_request
        self.request.set_ap_info(self._external_srv.fs_id, self._endpoint.ip)
        self.update_op_time()

    def normalize_json_string(self, res):
        temp = res.replace('\n', '').replace('\"', '"')
        return re.sub('ISODate\((.+?)\)', r'\g<1>', temp)

    def build_device_model(self):
        is_success = self.get_devices()
        return is_success


    def set_build_topo_profile(self):
        self.build_topo_profile = {
            LOGICAL_TOPO_TYPE:self.build_logic_topology
        }


    def update_op_time(self):
        if IS_WORKER_SIDE:
            query_condition = {'multiSources.nbPathSchema':{'$regex':'^VELOCLOUD'}}
            existing_objs = CDBHelper.QueryDeviceObjects(query_condition, cache_data = False)
            for i in existing_objs:
                if i['name'] not in self.existing_appliance_list:
                    self.existing_appliance_list.append(i['name'])
                if self.adjust_default_discover_behavior and (self.solo_scan_edges or self.solo_scan_enterprises or self.discover_new_appliance_only):   
                    CDBHelper.AddDeviceByObject(i)


    def buildNodeDeviceSetting(self, db_name, obj, is_dev_exist, default_ns_id):
        driver_id = obj['driverId']
        device_name = obj['name']
        subtype = obj['subType']
        management_ip = obj['mgmtIP']
        cli_front_server_id = self._ap_id
        api_server_id = self._external_server_id
        api_server_tech_id = self._tech_id
        device_id = obj['_id']
        result = CDBHelper.SetDeviceSettings(
                    device_name,
                    driver_id,
                    subtype,
                    management_ip,
                    cli_front_server_id,
                    api_server_id,
                    api_server_tech_id,
                    device_id = device_id
                    )

        # auto set ssh credential for VCE
        if subtype in [30105]:
            credential = ''
            if 'sn' in obj and obj['sn']:
                used_sn = obj['sn'].strip()[-3:]
                credential = 'VeloHello'+ used_sn.lower()
            if 'sn' in obj and obj['sn']:
                result = SetDeviceCredential(device_name, 'root', credential, '', '', 1, 22)
                if not result:
                    self.add_debug_log('error on save credential for device: ' + device_name)


    def get_devices(self):
        is_success = False

        def check_filter_result(enterprise_id, enterprise_name, edge_id, edge_name):
            if self.solo_scan_enterprises:
                for item in self.solo_scan_enterprises:
                    # item value is enterprise id
                    if item.isdigit():
                        if str(enterprise_id) == str(item):
                            break
                    # enterprise value is enterprise name
                    else:
                        if item.lower() in enterprise_name.lower():
                            break
                else:
                    return True
            if self.solo_scan_edges:
                for item in self.solo_scan_edges:
                    # item value is edge id
                    if item.isdigit():
                        if str(edge_id) == str(item):
                            break
                    # item value is edge name
                    else:
                        if item.lower() in edge_name.lower():
                            break
                else:
                    return True
            if self.discover_new_appliance_only:
                if self.existing_appliance_list:
                    if edge_name in self.existing_appliance_list:
                        return True
            return False
                      

        # merge legacy
        def _merge_legacy(node_obj):

            def _merge_vce_intf_properties(dev_name, new_intfs):
                # merge CLI only properties to API result
                old_intf_objs = GetInterfacesByDevice(dev_name, 'intfs')
                cli_only_properties = ['macAddr']
                for new_intf in new_intfs:
                    intf_name = new_intf.get('name')
                    for key in cli_only_properties:
                        value = new_intf.get(key)
                        old_value = GetInterfaceProperty(key, dev_name, intf_name,
                                 'intfs')
                        if (not value) and old_value:
                            new_intf[key] = old_value

            '''
            Simply use legacy first.
            '''
            if IS_WORKER_SIDE:
                dev_name = node_obj.get('name')
                node_obj['intfs'] = node_obj.get('intfs') or []
                legacy_objs = CDBHelper.QueryDeviceObjects(
                    {'name': dev_name})
                #old_intfs = QueryInterfaces({'name': node_obj.get('name')}, 'intfs')
                if len(legacy_objs) > 0:
                    legacy_obj = legacy_objs[0]
                    # may discovred from vcenter or other techspec.velo has highest priority
                    if 'VeloCloud ' not in legacy_obj['subTypeName']:
                        node_obj['_id'] = legacy_obj['_id']
                        legacy_obj = node_obj

                    # device properties
                    # common logic
                    legacy_source = {"nbPathSchema": "Legacy", "nbPathValue": legacy_obj['_id']}
                    has_legacy_source = False
                    velo_source = node_obj['multiSources'][0]
                    has_velo_source = False
                    dev_ms = legacy_obj['multiSources'] if 'multiSources' in legacy_obj else []
                    for s in dev_ms:
                        if s['nbPathSchema'] == 'Legacy':
                            has_legacy_source = True
                            s['nbPathValue'] = legacy_source['nbPathValue']
                        elif s['nbPathSchema'].startswith('VELOCLOUD'):
                            has_velo_source = True
                            s['nbPathValue'] = velo_source['nbPathValue']
                    if not has_legacy_source:
                        dev_ms.append(legacy_source)
                    if not has_velo_source:
                        dev_ms.append(velo_source)
                    legacy_obj['multiSources'] = dev_ms
                    legacy_obj['vendor'] = 'VMWARE'
                    if legacy_obj['subTypeName'] == 'VeloCloud Orchestrator':
                        legacy_obj['model'] = 'VeloCloud Orchestrator'

                    dev_device_setting = GetDeviceSetting(node_obj.get('name'))
                    locked_live_access = dev_device_setting.get('LockedLiveAccess', False)
                    locked_mgmt_ip = dev_device_setting.get('LockedMgmtIP', False)
                    # overwrite VCE mgmtIp/mfmtIntf if it is not locoked
                    if not locked_mgmt_ip and legacy_obj.get('subType') in [30105]:
                        legacy_obj['mgmtIP'] = node_obj.get('mgmtIP', '')
                        legacy_obj['mgmtIntf'] = node_obj.get('mgmtIntf', '')
                    # case 154210. update ver info or other gdrs which can be discovered by API only
                    dev_gdr_need_update_list = ['ver']
                    for item in dev_gdr_need_update_list:
                        if node_obj.get(item) and (node_obj.get(item) != legacy_obj.get(item)):
                            legacy_obj[item] = node_obj[item]

                    # update for interface properties
                    # update logic for VCE
                    new_intfs = node_obj.get('intfs') or []
                    if legacy_obj.get('subType') in [30105]:
                        _merge_vce_intf_properties(dev_name, new_intfs)
                        legacy_obj['intfs'] = new_intfs
                    # update logic for VCG or VCO, has_cli isn't set, use API result
                    elif not self.has_cli:
                        legacy_obj['intfs'] = new_intfs

                    return legacy_obj, locked_live_access

            # force 'Legacy' to be present in one of nbPathSchema
            # in case device is running over one VM (VM is discovered by other technology)
            _id = node_obj['_id']
            dev_ms = node_obj['multiSources']
            legacy_source = {"nbPathSchema": "Legacy", "nbPathValue": _id}
            dev_ms.append(legacy_source)
            return node_obj, False

        # get enterprise cookies
        is_operator = self.is_operator
        self.request.set_request_params(**self.vc_request.get_authen_headers(self.get_failed_log()))
        body = {}

        if is_operator:
            api_result = self.request.post(
                self._endpoint.url + '/portal/rest/network/getNetworkEnterprises',
                data=json.dumps(body))
        else:
            api_result = self.request.post(
                self._endpoint.url + '/portal/rest/enterprise/getEnterprise',
                data=json.dumps(body))
        if api_result.status_code != 200:
            self.add_failed_log('Retrieve enterprises list failed with state code:%s, error log:%s' % (
                api_result.status_code, api_result.error))
            return None

        if is_operator:
            enterprise_list = json.loads(api_result.text)
        else:
            enterprise_list = [json.loads(api_result.text)]


        retrieve_data = RetrieveDeviceData(self)
        for enterprise in enterprise_list:
            enterprise_id = enterprise.get('id', '')
            enterprise_name = enterprise.get('name', '')
            if not enterprise_id:
                continue
            for api_result in retrieve_data.retrieve_edge_data(
                self._endpoint.url, enterprise_id, self.add_discover_log):
                dev_name = api_result.get('edge',{}).get('name','')
                dev_id = api_result.get('edge',{}).get('id','')
                if DEVICE_FILTER and dev_name not in DEVICE_FILTER:
                    continue
                
                if self.adjust_default_discover_behavior:
                    filter_flag = check_filter_result(enterprise_id, enterprise_name, dev_id, dev_name)
                    if filter_flag:
                        continue
                
                mgmt_ip_setings = {
                    'prefer_private_wired_as_mgmt_ip': self.prefer_private_wired_as_mgmt_ip,
                    'prefer_loopback_as_mgmt_ip': self.prefer_loopback_as_mgmt_ip,
                    'loopback_priority_sequence': self.loopback_priority_sequence,
                    'lan_preferential_order': self.lan_preferential_order,
                }
                dev_object = ParseDeviceData.parsing_edge(api_result, self._framework.instance_id, mgmt_ip_setings)
                if dev_object:
                    dev_object_api = copy.deepcopy(dev_object)
                    dev_object, locked_live_access = _merge_legacy(dev_object)
                    is_success = True
                    if not dev_object.get('mgmtIP'):
                        dev_object['mgmtIP'] = self._endpoint.ip  # use endpoint ip if there is no mgmt ip.

                    self.legacy_device_objects.append(dev_object)
                    # if self.is_operator:
                    self.buildNodeDeviceSetting(self._domain_db_name, dev_object_api, True, self._ap_id)

                    # SNMP auto setting
                    dev_device_setting = GetDeviceSetting(dev_object['name'])
                    if dev_device_setting:
                        if not locked_live_access:
                            dev_device_setting['ManageIp'] = dev_object_api.get('mgmtIP', '')
                            dev_device_setting['SNMPSetting']['snmpTimeout'] = 20
                            # autoset SNMPv2 comnunity and SNMPv3 settings
                            if self.autoset_snmp:
                                if dev_object_api.get('snmpv2c_enabled'):
                                    dev_device_setting['SNMPSetting']['roString'] = dev_object_api.get('snmpv2c_community', '')
                                    dev_device_setting['SNMPSetting']['snmpVersion'] = 2
                                elif dev_object_api.get('snmpv3_enabled'):
                                    dev_device_setting['SNMPSetting']['snmpVersion'] = 3
                                    dev_device_setting['SNMPSetting']['v3']['authMode'] = dev_object_api.get('snmpv3_authMode', 0)
                                    dev_device_setting['SNMPSetting']['v3']['authPro'] = dev_object_api.get('snmpv3_authPro', 0)
                                    dev_device_setting['SNMPSetting']['v3']['authPassword'] = dev_object_api.get('snmpv3_authPassword', '')
                                    dev_device_setting['SNMPSetting']['v3']['userName'] = dev_object_api.get('snmpv3_userName', '')
                                    dev_device_setting['SNMPSetting']['v3']['encryptPassword'] = dev_object_api.get('snmpv3_encryptPassword', '')
                                    dev_device_setting['SNMPSetting']['v3']['encryptPro'] = dev_object_api.get('snmpv3_encryptPro', 0)
                            SetDeviceSetting(dev_device_setting)
                    del dev_object_api

                if not dev_object:
                    continue
                # save node data
                api_result = api_result['edge']
                if dev_object.get('multiSources'):
                    for nbpath in dev_object.get('multiSources'):
                        if nbpath['nbPathSchema'].lower().startswith('velocloud'):
                            api_result.update(nbpath)
                api_result['_id'] = dev_object['_id']
                api_result['dn'] = self._framework.instance_id
                api_result['nbId'] = self._framework.instance_id
                api_result['name'] = dev_object['name']
                self.sdn_node_objects.setdefault(api_result['nbPathSchema'], [])
                self.sdn_node_objects[api_result['nbPathSchema']].append(api_result)


        # get operator cookies
        #self.request.set_request_params(**self.vc_request.get_authen_headers(msg=self.get_failed_log()))
        has_data = False
        if is_operator:
            for api_result in retrieve_data.retrieve_gateway_data(
                self._endpoint.url, self.add_discover_log):
                dev_object = ParseDeviceData.parsing_gateway(api_result, self._framework.instance_id)
                if dev_object:
                    dev_object, _ = _merge_legacy(dev_object)
                    is_success = True
                    if not dev_object.get('mgmtIP'):
                        dev_object['mgmtIP'] = self._endpoint.ip  # use endpoint ip if there is no mgmt ip.
                    self.legacy_device_objects.append(dev_object)

                if not dev_object:
                    continue
                # save node data
                if dev_object.get('multiSources'):
                    for nbpath in dev_object.get('multiSources'):
                        if nbpath['nbPathSchema'].lower().startswith('velocloud'):
                            api_result.update(nbpath)
                api_result['_id'] = dev_object['_id']
                api_result['dn'] = self._framework.instance_id
                api_result['nbId'] = self._framework.instance_id
                api_result['name'] = dev_object['name']
                self.sdn_node_objects.setdefault(api_result['nbPathSchema'], [])
                self.sdn_node_objects[api_result['nbPathSchema']].append(api_result)

            # get orchastrator
            # check if standy_vco exists. need operator special privilege.
            try:
                standby_vco = []
                active_vco_ip = ''
                standby_vco_ip = ''
                body = {}

                api_result = self.request.post(
                self._endpoint.url + '/portal/rest/disasterRecovery/getReplicationStatus', data=json.dumps(body))
                if api_result.status_code != 200:
                    self.add_failed_log('Retrieve vco info by getReplicationStatus failed with state code:%s, error log:%s' % (
                        api_result.status_code, api_result.error))
                else:
                    vco_info = json.loads(api_result.text)
                    standby_vco = vco_info.get('standbyList',[])
                    active_address = vco_info.get('activeAddress','')
                    if standby_vco:
                        standby_vco = standby_vco[0]
                        standby_address = standby_vco.get('standbyAddress','')
                    if 'activeReplicationAddress' in vco_info and vco_info['activeReplicationAddress']:
                        active_vco_ip = vco_info['activeReplicationAddress']
                    if 'standbyReplicationAddress' in standby_vco and standby_vco['standbyReplicationAddress']:
                        standby_vco_ip = standby_vco['standbyReplicationAddress']
                    dev_object = ParseDeviceData.parsing_vco(
                        active_address, self._framework.instance_id, active_vco_ip, 'ACTIVE_VCO')
                    if dev_object:
                        dev_object, _ = _merge_legacy(dev_object)
                        if not dev_object.get('mgmtIP'):
                            dev_object['mgmtIP'] = self._endpoint.ip  # use endpoint ip if there is no mgmt ip.
                        self.legacy_device_objects.append(dev_object)
                    if standby_vco:
                        dev_object = ParseDeviceData.parsing_vco(
                            standby_address, self._framework.instance_id, standby_vco_ip, 'STANDBY_VCO')
                        if dev_object:
                            dev_object, _ = _merge_legacy(dev_object)
                            if not dev_object.get('mgmtIP'):
                                dev_object['mgmtIP'] = self._endpoint.ip  # use endpoint ip if there is no mgmt ip.
                            self.legacy_device_objects.append(dev_object)
                    has_data = True
            except:
                self.add_failed_log('current login account do not have priviledge to get API disasterRecovery info')

        if not has_data:
            mgmt_ip = ''
            body = {"enterpriseId": enterprise_id}
            api_result = self.request.post(
                self._endpoint.url + '/portal/rest/enterprise/getEnterpriseAddresses',
                body=json.dumps(body))
            if api_result.status_code != 200:
                self.add_failed_log('Retrieve vco info by getEnterpriseAddresses failed with state code:%s, error log:%s' % (
                    api_result.status_code, api_result.error))
            else:
                enterprise_addresses = json.loads(api_result.text)
                for entity in enterprise_addresses:
                    entity_role = entity.get('entity','')
                    if entity_role == 'ACTIVE_VCO':
                        mgmt_ip = entity.get('address','')
                        break
                dev_object = ParseDeviceData.parsing_vco(
                    self._endpoint.ip, self._framework.instance_id, mgmt_ip, 'ACTIVE_VCO')
                if dev_object:
                    dev_object, _ = _merge_legacy(dev_object)
                    if not dev_object.get('mgmtIP'):
                        dev_object['mgmtIP'] = self._endpoint.ip  # use endpoint ip if there is no mgmt ip.
                    self.legacy_device_objects.append(dev_object)

        ## add root node
        row = {}
        row['_id'] = self._framework.instance_id
        row['dn'] = self._framework.instance_id
        row['nbId'] = self._framework.instance_id
        row['name'] = self._endpoint.ip
        row['enterpriseIds'] = enterprise_list
        row['nbPathSchema'] = 'VELOCLOUD'
        row['nbPathValue'] = self._framework.instance_id
        self.sdn_node_objects['VELOCLOUD'] = [row]

        ## add vco node
        row = {}
        row['_id'] = self._framework.instance_id
        row['dn'] = self._framework.instance_id
        row['nbId'] = self._framework.instance_id
        row['name'] = self._endpoint.ip
        row['enterpriseIds'] = enterprise_list
        row['nbPathSchema'] = vco_schema
        row['nbPathValue'] = self._framework.instance_id + '\\' + self._endpoint.ip
        self.sdn_node_objects[vco_schema] = [row]
        if self.discover_new_appliance_only and not is_success:
            self.add_failed_log('Discover New Appliance Only is Set. Zero new appliance has been found!')
        return is_success


    def build_logic_topology(self):
        gateway_objs = CDBHelper.QueryNodes(gateway_schema, {'nbPathSchema':gateway_schema, 'nbId':self._framework.instance_id})
        gateway_names = [i['name'] for i in gateway_objs]
        edge_objs = CDBHelper.QueryNodes(gateway_schema, {'nbPathSchema':edge_schema, 'nbId':self._framework.instance_id})
        edge_names = [i['name'] for i in edge_objs]

        # build edge to gateway logical topology
        # if gateway_objs:
        #     for gateway_obj in gateway_objs:
        #         vcg_id = gateway_obj['_id']
        #         vcg_name = gateway_obj['name']
        #         for link in gateway_obj.get('connectedEdgeList', []):
        #             vceid = link['vceid'].lower()
        #             vces = CDBHelper.QueryDeviceObjects({'_id':vceid})
        #             print('vces', vces)
        #             vce_obj = vces[0]
        #             if vces:
        #                 CDBHelper.AddLinkToInterface(
        #                     self._framework.instance_id, vcg_id, vcg_name,
        #                     '', vceid, vce_obj['name'],
        #                     '', LOGICAL_TOPO_TYPE, self._technology)
        #                 print('logical link', self._framework.instance_id, vcg_id, vcg_name,
        #                     '', vceid, vce_obj['name'],
        #                     '', LOGICAL_TOPO_TYPE, self._technology)
        vco_object = CDBHelper.QueryDeviceObjects({'name':self._endpoint.ip})
        # build vco to edge/gateway logic topology
        if len(vco_object)>0:
            vco_name, vco_id = vco_object[0]['name'], vco_object[0]['_id']
            gateway_names.extend(edge_names)
            debug_print('gateway_names', gateway_names)
            for dev_name in gateway_names:
                dev_obj = CDBHelper.QueryDeviceObjects({'name':dev_name})
                if dev_obj:
                    dev_id = dev_obj[0]['_id']
                    CDBHelper.AddLinkToInterface(
                        self._framework.instance_id, vco_id, vco_name,
                        '', dev_id, dev_name, '', LOGICAL_TOPO_TYPE, self._technology)
                    debug_print('logical link', self._framework.instance_id, vco_id, vco_name,
                        '', dev_id, dev_name, '', LOGICAL_TOPO_TYPE, self._technology)


#define call function for framework

def check_license(endPoint, user, pwd, params):
    """
    Just hardcode return True, will be abandoned in future
    """
    return {'result': True}


def vc_discover_devices(endpoint_url, user, password, params):
    """
    Be Invoked by framework in discover/benchmark.
    Build device and topology model.
    """
    print('Start VeloCloud discovery')
    global common_endpoint_url
    common_endpoint_url = endpoint_url
    try:
        ap = TechSpecVC(endpoint_url, user, password, params)
        return ap.run()
    except Exception as e:
        msg = traceback.format_exc() + str(e)
        print('discover VeloCloud failed with error"%s' % msg)
        return {'result':False, 'msg':msg}


# define retrieve data function
class RetrieveDeviceData:

    def __init__(self, vc_inst):
        self.vc_inst = vc_inst

    def get_api_data(self, endpoint_url, api_url, body, add_log):
        api_result = self.vc_inst.request.post(
            endpoint_url + api_url,
            data=json.dumps(body))
        if api_result.status_code != 200:
            add_log(
                'Retrieve %s failed with state code:%s, error log:%s, body:%s' % (
                    api_url,
                    api_result.status_code,
                    api_result.error if hasattr(api_result, 'error') else api_result.text,
                    str(body)))
            rtn = None
        else:
            rtn = json.loads(api_result.text)
        return rtn


    def retrieve_edge_data(cls, endpoint_url, enterprise_id, add_log):
        # get edge list for specific enterprise
        # https://xxxx/portal/rest/enterprise/getEnterpriseEdges
        body = {
            "id": 0,
            "enterpriseId": enterprise_id,
            "with": [
                   "site", "links", "recentLinks", "configuration"
            ]
            }
    
        edge_list = cls.get_api_data(
            endpoint_url, '/portal/rest/enterprise/getEnterpriseEdges', body, add_log)

        for edge in edge_list:
            edge_id = edge['id']
            active_state = edge['activationState']
            if active_state.upper() != 'ACTIVATED':
                add_log('Skip edge %s since active state %s is not activated' % (edge['name'], active_state))
                continue

            off_state = edge.get('edgeState')
            if off_state == 'OFFLINE':
                add_log('Skip edge %s since edge state is OFFLINE' % (edge['name']))
                continue

            body = {
                "edgeId": edge_id,
                "enterpriseId": enterprise_id
            }
            edge_config = cls.get_api_data(
                endpoint_url, '/portal/rest/edge/getEdgeConfigurationStack', body, add_log)

            # get metrics
            endtime = int(time.time() * 1000)
            starttime = endtime - 3600 * 1000 * 24
            body = {
                "enterpriseId": enterprise_id,
                "edgeId": edge_id,
                "interval": {
                    "start": starttime ,
                    "end": endtime
                }
            }

            edge_metrix = cls.get_api_data(endpoint_url, '/portal/rest/metrics/getEdgeLinkMetrics', body, add_log)
            rtn = {
                'edge': edge,
                'edgeConfig': edge_config,
                'edgeMetrix': edge_metrix
            }
            yield rtn

    def retrieve_gateway_data(self, endpoint_url, add_log):
        # get gateway list
        # need use operate login
        # https://xxxx/portal/rest/?network?/getNetworkGateways
        api_result = self.get_api_data(endpoint_url, '/portal/rest/network/getNetworkGateways', {}, add_log)
        if not api_result:
            return None
        # gateway_list = json.loads(api_result.text)

        for gateway in api_result:
            yield gateway



# define data parsing function
class Interface:
    def __init__(self, ifname):
        self.ifname = ifname
        self.ipaddresses = [] # [1.1.1.1, 255.255.255.0]
        self.vrf = ''  # mplsVrf
        self.segment_name = '' # segmentName
        self.isp = '' # isp
        self.isshutdown = False # isShutdown
        self.l3vlan = None  # intfVlanId
        self.l2vlan = [] # vlan
        self.speed = None # speed
        self.duplex = None # duplex
        self.link_name = '' #linkName
        self.link_bd_rx = ''  # bpsOfBestPathRx
        self.link_bd_tx = ''  # bpsOfBestPathTx
        self.nbpath_schema = ''
        self.nbpath_value = ''
        self.multi_sources = []
        self.is_dhcp = False

    def to_dict(self):
        ips = []
        ip2mask = {}
        # remove duplicate IP, and for same ip, use the ip with mask
        for ipmask in set(self.ipaddresses):
            ip_addr, mask = ipmask
            ip2mask.setdefault(ip_addr, None)
            if mask:
                ip2mask[ip_addr] = mask

        for ip_addr, mask in ip2mask.items():
            if IsIP(ip_addr) != 4:
                continue
            mask_len = function.masktoint(mask) if IsIP(mask) == 4 else None
            if mask_len:
                ip_addr_withmask = ip_addr + '/' + str(mask_len)
            else:
                ip_addr_withmask = ip_addr

            ip_number = int(IP.IPToInt(ip_addr))
            ips_data = {
                'ip': ip_number,
                'ipLoc': ip_addr_withmask,
                'maskLen': mask_len
            }
            ips.append(ips_data)

        interface_obj = {
            'name': self.ifname,
            'shortName': self.ifname,
            'ips': ips,
            'mplsVrf': self.segment_name or str(self.vrf),
            'segmentName': self.segment_name,
            'segmentId': self.vrf,
            'isp': self.isp,
            'isShutdown': self.isshutdown,
            'intfVlanId': str(self.l3vlan) if isinstance(self.l3vlan, int) else '',
            'vlan': ','.join(self.l2vlan),
            'speed': self.speed,
            'duplex': self.duplex,
            'linkName': self.link_name,
            'bpsOfBestPathRx': self.link_bd_rx,
            'bpsOfBestPathTx': self.link_bd_tx,
            'multiSources': self.multi_sources or None
            }

        return interface_obj


class ParseDeviceData:

    @staticmethod
    def get_child_by_path(parent_obj, path, name_keys = [], repeat = False):
        def search(obj, sub_paths, name_keys = []):
            try:
                for sub_path in sub_paths:
                    if isinstance(obj, list):
                        found =  False
                        size = len(obj)
                        # for each sub_path which is indexed by an integer, check if it has a corresponding name key
                        # respect name keys first
                        if not name_keys:
                            obj = obj[int(sub_path)]
                            found  = True
                        elif size > 0:
                            key_dict  = name_keys[0]
                            for k, v in key_dict.items():
                                key = k
                                value = v
                                break
                            del name_keys[0]
                            for i in range(0, size):
                                if obj[i][key] == value:
                                    obj = obj[i]
                                    found  = True
                                    break
                        if not found:
                            return False
                    else:
                        obj = obj[sub_path]
                return obj
            except:
                error_print(traceback.format_exc())
                return False

        result =  False
        repeat_flag = True
        level1_obj_list = []
        sub_paths = path.split('.')
        temp_obj = copy.deepcopy(parent_obj)
        for obj in temp_obj:
            # it is observed the members of parent_obj may not be a dict
            if isinstance(obj, list):
                for i in obj:
                    level1_obj_list.append(i)
            elif isinstance(obj, dict):
                level1_obj_list.append(obj)
        # search all the levle 1 objects
        while repeat_flag and len(level1_obj_list) > 0:
            temp_name_keys = copy.deepcopy(name_keys)
            _result = search(level1_obj_list[0], sub_paths, temp_name_keys)
            if repeat and result and isinstance(result, list):
                result.extend(_result)
            else:
                result = _result
            if not repeat and result:
                repeat_flag =  False
            del level1_obj_list[0]
        return result


    @staticmethod
    @debugthis
    def _parse_lan_mgmt_ip(edge_config):
        name_keys = [{'name' : 'deviceSettings'}]
        obj = ParseDeviceData.get_child_by_path(edge_config, "modules.1.data.lan.management", name_keys = name_keys)
        if not obj:
            return False
        return obj.get('cidrIp')

    @staticmethod
    @debugthis
    def _parse_wan_private_wired_ip(edge_config):
        name_keys = [{'name' : 'WAN'}]
        wan_links = ParseDeviceData.get_child_by_path(edge_config, "modules.3.data.links", name_keys = name_keys)
        wired_mgmt_ip = ''
        wired_intf = ''
        if wan_links:
            for link in wan_links:
                mode = link['mode'] if 'mode' in link else ''
                type = link['type'] if 'type' in link else ''
                intf = link['interfaces'][0] if 'interfaces' in link and link['interfaces'] else ''
                if mode == 'PRIVATE' and type == 'WIRED':
                    wired_mgmt_ip = link['publicIpAddress'] if 'publicIpAddress' in link else ''
                    wired_intf = intf
        return wired_mgmt_ip, wired_intf

    @staticmethod
    @debugthis
    def _parse_snmp_strings(edge_config, device_property):
        name_keys = [{'name' : 'deviceSettings'}]
        snmp_configs = ParseDeviceData.get_child_by_path(edge_config, "modules.1.data.snmp", name_keys = name_keys)
        if not snmp_configs:
            return
        snmpv2c = snmp_configs.get('snmpv2c', {})
        snmpv3 = snmp_configs.get('snmpv3', {})
        if snmpv2c:
            device_property['snmpv2c_enabled'] = snmpv2c.get('enabled', False)
            device_property['snmpv2c_community'] = snmpv2c.get('community', '')
        if snmpv3:
            users = snmpv3.get('users',[])
            enabled = snmpv3.get('enabled',False)
            device_property['snmpv3_enabled'] = enabled
            if users:
                config = users[0]
                privacy = config.get('privacy',False)
                v3mode = 0
                if enabled:
                    if privacy:
                        v3mode = 3
                    else:
                        v3mode = 2
                else:
                    v3mode = 1
                device_property['snmpv3_authMode'] = v3mode
                if v3mode > 1 :
                    device_property['snmpv3_authPassword'] = config.get('passphrase','')
                if v3mode  == 3:
                    device_property['snmpv3_encryptPassword'] = config.get('passphrase','')
                device_property['snmpv3_userName'] = config.get('name','')
                device_property['snmpv3_authPro'] = SNMPv3_authPros.get(config.get('authAlg',''),0)
                device_property['snmpv3_encryptPro'] = SNMPv3_encryptPros.get(config.get('encrAlg',''), 0)


    @staticmethod
    @debugthis
    def _parse_lan_networks(edge_config, interfaces, lan_preferential_order):
        name_keys = [{'name' : 'deviceSettings'}]
        # may get extra networks from 0.modules.xxx or 1.modules.x
        objs = ParseDeviceData.get_child_by_path(edge_config, "modules.1.data.lan.networks", name_keys = name_keys) or []
        # edge_config has been changed/reduced in the first call
        name_keys = [{'name' : 'deviceSettings'}]
        objs.extend(ParseDeviceData.get_child_by_path(edge_config, "modules.1.data.lan.networks", name_keys = name_keys) or [])
        lan_intfs = {}
        lan_preferential_order = lan_preferential_order.split(';')
        for obj in objs:
            intf_name = obj.get('name')
            if not intf_name:
                continue
            intf_obj = interfaces.setdefault(intf_name, Interface(intf_name))
            ip, mask = obj.get('cidrIp'), obj.get('netmask')
            if ip and mask:
                intf_obj.ipaddresses.append((ip, mask))
                lan_intfs[intf_name] = ip
            else:
                intf_obj.is_dhcp = obj.get('dhcp', {}).get('enabled')
            intf_obj.isshutdown = obj.get('disabled')
            intf_obj.vrf = obj.get('segmentId')
            intf_obj.l3vlan = obj.get('vlanId')
        for name in lan_preferential_order:
            for k, v in lan_intfs.items():
                if name.lower() == k.lower():
                    return v, k
        return '', ''


    # @staticmethod
    # @debugthis
    # def _parse_mgmt_intf(edge_config, interfaces):
    #     schema = "1.modules.1.data.lan.management"
    #     obj = ParseDeviceData.get_child_by_path(edge_config, schema)
    #     ip = obj.get('cidrIp')
    #     if ip:
    #         mgmt_intf = interfaces.setdefault('mgmt', Interface('mgmt'))
    #         mask = function.getmaskaddressbylen(obj.get('cidrPrefix')) if obj.get('cidrPrefix') else ''
    #         mgmt_intf.ipaddresses.append((ip, mask))

    @staticmethod
    @debugthis
    def _parse_routed_intfs(edge_config, interfaces):
        schema = 'modules.1.data.routedInterfaces'
        name_keys = [{'name' : 'deviceSettings'}]

        def _parse_rt_intf(intf_obj, obj):
            addressing = obj.get('addressing') or {}
            ip, mask = addressing.get('cidrIp'), addressing.get('netmask')
            if ip and mask:
                intf_obj.ipaddresses.append((ip, mask))
            else:
                if addressing.get('type') == 'DHCP':
                    intf_obj.is_dhcp = True
            intf_obj.isshutdown = obj.get('disabled')
            intf_obj.vrf = obj.get('segmentId')
            intf_obj.l3vlan = obj.get('vlanId')
            l2 = obj.get('l2') or {}
            intf_obj.speed, intf_obj.duplex = l2.get('speed'), l2.get('duplex')

        objs = ParseDeviceData.get_child_by_path(edge_config, schema, name_keys = name_keys) or []
        for obj in objs:
            intf_name = obj.get('name')
            if not intf_name:
                continue
            intf_obj = interfaces.setdefault(intf_name, Interface(intf_name))
            _parse_rt_intf(intf_obj, obj)
            sub_intfs = obj.get('subinterfaces') or []
            for sub_intf in sub_intfs:
                intf_id = sub_intf.get('subinterfaceId')
                if not intf_id:
                    continue
                sub_intf_name = intf_name + '.' + str(intf_id)
                sub_intf_obj = interfaces.setdefault(sub_intf_name, Interface(sub_intf_name))
                _parse_rt_intf(sub_intf_obj, sub_intf)

    @staticmethod
    @debugthis
    def _parse_ha_intfs(edge_config, interfaces):
        pass

    @staticmethod
    @debugthis
    def _parse_loop_intfs(edge_config, interfaces, device_property, prefer_loopback_as_mgmt_ip, loopback_priority_sequence):
        schema = 'modules.1.data.loopbackInterfaces'
        name_keys = [{'name' : 'deviceSettings'}]
        objs = ParseDeviceData.get_child_by_path(edge_config, schema, name_keys = name_keys) or {}
        lo_dict = {}
        for intf_name, value in objs.items():
            intf_obj = interfaces.setdefault(intf_name, Interface(intf_name))
            ip, mask_len = value.get('cidrIp'), value.get('cidrPrefix')
            mask = function.getmaskaddressbylen(mask_len) if isinstance(mask_len, int) else ''
            if ip:
                intf_obj.ipaddresses.append((ip, mask))
                lo_dict[intf_name.lower()] = ip
                # if intf_name.lower() == 'lo1':
                #     device_property['mgmtIP'] = ip
                #     device_property['mgmtIntf'] = intf_name
            intf_obj.vrf = value.get('segmentId')

        # in case self-defined loop back intf is defined.
        # check the priority defined by customer.
        # the first loop back intf defined in list is used as mgmt_ip
        if prefer_loopback_as_mgmt_ip and loopback_priority_sequence:
            for intf_name in loopback_priority_sequence:
                if intf_name.lower() in lo_dict:
                    return lo_dict[intf_name.lower()], intf_name
                    break
        return '', ''

    @staticmethod
    @debugthis
    def _parse_l2_intfs(edge_config, interfaces):
        schema = "modules.1.data.models"
        name_keys = [{'name' : 'deviceSettings'}]
        objs = ParseDeviceData.get_child_by_path(edge_config, schema, name_keys = name_keys) or {}
        for value in objs.values():
            lan_intfs = value.get('lan', {}).get('interfaces') or []
            for lan_intf in lan_intfs:
                intf_name = lan_intf.get('name')
                if not intf_name:
                    continue
                intf_obj = interfaces.setdefault(intf_name, Interface(intf_name))
                intf_obj.l2_mode = lan_intf.get('portMode') or ''
                intf_obj.l2_vlans = lan_intf.get('vlanIds') or []
                l2 = lan_intf.get('l2') or {}
                intf_obj.speed =  l2.get('speed')
                intf_obj.duplex =  l2.get('duplex')
                intf_obj.isshutdown =  l2.get('disabled')


    @staticmethod
    @debugthis
    def _parse_link_bps_bestpath(edge_metrix, interfaces):
        for link_obj in edge_metrix:
            link = link_obj.get('link',{})
            intf_name = link.get('interface', '')
            if not intf_name:
                continue
            intf_obj = interfaces.setdefault(intf_name, Interface(intf_name))
            intf_obj.link_name =  link.get('displayName','')
            intf_obj.isp = link.get('isp','')
            ip_addr = link.get('ipAddress','')
            mask = link.get('netmask', '')
            intf_obj.link_bd_rx = link_obj.get('bpsOfBestPathRx', '')
            intf_obj.link_bd_tx = link_obj.get('bpsOfBestPathTx', '')
            if IsIP(ip_addr):
                intf_obj.ipaddresses.append((ip_addr, mask))


    @staticmethod
    @debugthis
    def _parse_bgp(edge_config):
        bgp_schema = "modules.1.data.segments"
        name_keys = [{'name' : 'deviceSettings'}]
        objs = ParseDeviceData.get_child_by_path(edge_config, bgp_schema, name_keys = name_keys) or []
        bgp_info = []
        has_bgp = False
        for obj in objs:
            if 'bgp' not in obj:
                continue
            segment_id = obj['segment']['segmentId']
            bgp_enable = obj['bgp']['enabled']
            if bgp_enable:
                has_bgp = True
            # asn = obj['bgp']['ASN']
            asn = obj['bgp'].get('ASN', '')
            if not asn:
                continue
            for nbr in obj['bgp']['neighbors']:
                nbr_as = nbr['neighborAS']
                nbr_ip = nbr['neighborIp']
                row = {
                    "localAsNum": asn,
                    "neighborIp": nbr_ip,
                    "remoteAsNum": nbr_as,
                    "vrfName": str(segment_id)
                }
                bgp_info.append(row)
        return has_bgp, bgp_info

    # modules.1.data.segments segment.name
    def _parse_segments(edge_config, interfaces):
        schema = "modules.1.data.segments"
        name_keys = [{'name' : 'deviceSettings'}]
        objs = ParseDeviceData.get_child_by_path(edge_config, schema, name_keys = name_keys) or []
        id2name = {-1: 'Underlay'}
        for obj in objs:
            segment_obj = obj['segment']
            segment_id = segment_obj['segmentId']
            segment_name = segment_obj['name']
            id2name[segment_id] = segment_name

        for intf in interfaces.values():
            intf.segment_name = id2name.get(intf.vrf)

    @staticmethod
    @debugthis
    def _add_nbpaths(interfaces, sub_path):
        for name, intf_obj in interfaces.items():
            intf_obj.multi_sources = [{
                'nbPathSchema': edge_port_schema,
                'nbPathValue': '/'.join([sub_path, name])
                }]

    @staticmethod
    @debugthis
    def _parse_edge_devinfo(edge, instance_id):
       # device
        device_type = 30105
        device_type_name = 'VeloCloud Edge'
        driver_id = 'ca965acf-2852-4410-b692-1f96225b7e02'
        driver_name = 'VeloCloud Edge'
        main_type_name = 'Router'
        main_type_id = 1000
        assign_tag = []
        host_name = get_normal_name(edge['name'])

        mgmt_ip = ''

        # parse edge device
        device_property = {
            'ver':edge.get('softwareVersion', ''),
            'sn':edge.get('serialNumber', ''),
            'model':edge.get('modelNumber', ''),
            'name':host_name,
            '_id':edge['logicalId'].lower(),
            'mgmtIP': mgmt_ip,
            'isHA': edge.get('haState') == 'READY',
            'haSerialNumber': edge.get('haSerialNumber') or '',
            'edgeID': edge['id'],
            'enterpriseID': edge['enterpriseId'],
            'mainType': main_type_id,
            'mainTypeName': main_type_name,
            'subType': device_type,
            'subTypeName': device_type_name,
            'driverName': driver_name,
            'driverId': driver_id,
            'assignTags': assign_tag,
            'vendor': 'VMWARE',
            'multiSources': [{
                'nbPathValue': '/'.join([instance_id, edge['logicalId'], str(edge['enterpriseId']), str(edge['id'])]),
                'nbPathSchema': edge_schema
            }]
        }

        return device_property

    @classmethod
    @debugthis
    def parsing_edge(cls, edge_data, instance_id, mgmt_ip_settings):
        if not edge_data:
            return None
        # debug_print('edge_data is:', edge_data)
        edge = edge_data['edge']
        edge_config = edge_data['edgeConfig']
        edge_metrix = edge_data['edgeMetrix']

        # parse edge device info
        device_property = cls._parse_edge_devinfo(edge, instance_id)
        has_bgp, bgp_infos = cls._parse_bgp(edge_config)
        if has_bgp:
            device_property['hasBGPConfig'] = True
        if bgp_infos:
            device_property['bgpNeighbor'] = bgp_infos

        # parse edge interface info
        interfaces = {}
        # parse interface from config
        if edge_config:
            # in case of customized mgmt ip
            api_mgmt_ip = cls._parse_lan_mgmt_ip(edge_config)

            prefer_private_wired_as_mgmt_ip = mgmt_ip_settings.get('prefer_private_wired_as_mgmt_ip') or False
            if prefer_private_wired_as_mgmt_ip:
                private_wired_mgmt_ip, wired_intf = cls._parse_wan_private_wired_ip(edge_config)

            lan_preferential_order = mgmt_ip_settings.get('lan_preferential_order') or ''
            lan_mgmt_ip, lan_mgmt_intf = cls._parse_lan_networks(edge_config, interfaces, lan_preferential_order)

            cls._parse_routed_intfs(edge_config, interfaces)
            cls._parse_ha_intfs(edge_config, interfaces)

            prefer_loopback_as_mgmt_ip = mgmt_ip_settings.get('prefer_loopback_as_mgmt_ip') or False
            loopback_priority_sequence = mgmt_ip_settings.get('loopback_priority_sequence') or ''
            if loopback_priority_sequence:
                loopback_priority_sequence = loopback_priority_sequence.split(';')
            else:
                loopback_priority_sequence = []
            lb_mgmt_ip, lb_mgmt_intf = cls._parse_loop_intfs(edge_config, interfaces, device_property, prefer_loopback_as_mgmt_ip, loopback_priority_sequence)

            cls._parse_l2_intfs(edge_config, interfaces)
            # parse segment name and id mapping
            cls._parse_segments(edge_config, interfaces)
            cls._parse_snmp_strings(edge_config, device_property)

        # parse interface edge metrix
        if edge_metrix:
            cls._parse_link_bps_bestpath(edge_metrix, interfaces)
        cls._add_nbpaths(interfaces, '/'.join([instance_id, edge['logicalId']]))

        # merge DHCP interface from driver interface info
        exist_dev_obj = CDBHelper.QueryDeviceObjects({'name': device_property['name']}, False)
        if exist_dev_obj:
            exist_dev_intfs = exist_dev_obj[0].get('intfs', [])
            exist_dev_intfs_dict = {i['name']: i for i in exist_dev_intfs}
            for intf_name, intf_obj in interfaces.items():
                if intf_obj.is_dhcp and intf_name in exist_dev_intfs_dict:
                    for old_ip in exist_dev_intfs_dict[intf_name].get('ips') or []:
                        iploc = old_ip.get('ipLoc') or ''
                        if IsIP(iploc) == 4:
                            old_ip_obj = IP(iploc)
                            intf_obj.ipaddresses.append((old_ip_obj.Address(), old_ip_obj.Mask()))

        device_property['intfs'] = [i.to_dict() for i in interfaces.values()]

        # sources of mgmt_ip:
        # prefer_loopback_as_mgmt_ip, if defined - top priority
        # prefer_private_wired_mgmt_ip, if defined - second high priority
        # lan_preferential_order, if defined - third priority
        # api_mgmt_ip, used as default mgmt_ip, lowest priority
        # if all above are None, randonly choose one intf ip as mgmt_ip
        if prefer_loopback_as_mgmt_ip:
            if lb_mgmt_ip and lb_mgmt_intf:
                device_property['mgmtIP'] = lb_mgmt_ip
                device_property['mgmtIntf'] = lb_mgmt_intf
        # designed for COCC. prefer private wired IP first
        if not device_property.get('mgmtIP') and prefer_private_wired_as_mgmt_ip:
            if private_wired_mgmt_ip and wired_intf:
                device_property['mgmtIP'] = private_wired_mgmt_ip
                device_property['mgmtIntf'] = wired_intf
        if  not device_property.get('mgmtIP') and lan_preferential_order:
            if lan_mgmt_ip and lan_mgmt_intf:
                device_property['mgmtIP'] = lan_mgmt_ip
                device_property['mgmtIntf'] = lan_mgmt_intf
        if not device_property.get('mgmtIP') and api_mgmt_ip:
            # api_mgmt_ip may not have an corresponding intf
            device_property['mgmtIP'] = api_mgmt_ip

        # mgmt_dict = {
        #     'prefer_private_wired_as_mgmt_ip': prefer_private_wired_as_mgmt_ip,
        #     'prefer_loopback_as_mgmt_ip': prefer_loopback_as_mgmt_ip,
        #     'lb_mgmt_ip': lb_mgmt_ip if prefer_loopback_as_mgmt_ip else '',
        #     'lb_mgmt_intf': lb_mgmt_intf if prefer_loopback_as_mgmt_ip else '',
        #     'private_wired_mgmt_ip': private_wired_mgmt_ip if prefer_loopback_as_mgmt_ip else '',
        #     'wired_intf': wired_intf if prefer_loopback_as_mgmt_ip else '',
        #     'lan_mgmt_ip': lan_mgmt_ip,
        #     'lan_mgmt_intf': lan_mgmt_intf,
        #     'api_mgmt_ip': api_mgmt_ip,
        #     'mgmtIP': device_property.get('mgmtIP', ''),
        #     'mgmtIntf': device_property.get('mgmtIntf', '')
        # }
        # raise ValueError(mgmt_dict)

        # select one ip as mgmt IP if mgmtIP is empty
        if not device_property.get('mgmtIP', ''):
            for intf in interfaces.values():
                if intf.ipaddresses:
                    for ips in intf.ipaddresses:
                        device_property['mgmtIP'] = ips[0]
                        device_property['mgmtIntf'] = intf.ifname
                        break
                if device_property['mgmtIP']:
                    break

        # get mgmt intf if mgmtIntf is empty
        mgmt_ip = device_property.get('mgmtIP', '')
        if mgmt_ip and not device_property.get('mgmtIntf', ''):
            for intf in interfaces.values():
                if intf.ipaddresses:
                    for ips in intf.ipaddresses:
                        if mgmt_ip == ips[0]:
                            device_property['mgmtIntf'] = intf.ifname
                            break
                if device_property.get('mgmtIntf', ''):
                    break
        rtn = create_device_object(device_property)
        return rtn

    @staticmethod
    def parsing_gateway(gateway, instance_id):
        if not gateway:
            return None
        device_type = 30107
        device_type_name = 'VeloCloud Gateway'
        driver_id = '92498440-76c4-40ba-a3b8-427609cbb841'
        driver_name = 'VeloCloud Gateway'
        main_type_name = 'Router'
        main_type_id = 1000
        assign_tag = ['esg']
        gateway_id = str(gateway['id'])
        gateway_logical_id = gateway['logicalId']
        vc_gateway_property = {
            'ver':gateway.get('softwareVersion', ''),
            'name':gateway['name'],
            '_id':gateway['logicalId'].lower().replace('gateway', ''),
            'mgmtIP':gateway['ipAddress']
        }

        nb_property = {
            'mainType': main_type_id,
            'mainTypeName': main_type_name,
            'subType': device_type,
            'subTypeName': device_type_name,
            'driverName': driver_name,
            'driverId': driver_id,
            'vendor': 'VMWARE',
            'assignTags': assign_tag,
            'multiSources': [{
                'nbPathValue': '/'.join([instance_id, gateway_logical_id, gateway_id]),
                'nbPathSchema': gateway_schema
            }]
        }
        interfaces = []
        # intfs_data = edge_dict.get('links', [])
        intfs_data = {'ipAddress':gateway.get('ipAddress'), 'privateIpAddress':gateway.get('privateIpAddress')}
        for intf_name in intfs_data:
            ip_addr = intfs_data[intf_name]
            if ip_addr:
                ip_number = int(IP.IPToInt(ip_addr))
                ips_data = {
                    'ip': ip_number,
                    'ipLoc': ip_addr,
                    'maskLen': 0
                }
                ips = [ips_data]
            else:
                ips = []
            interface_obj = {
                    'name': intf_name,
                    'shortName': intf_name,
                    'multiSources': [{
                        'nbPathSchema': gateway_port_schema,
                        'nbPathValue': '/'.join([instance_id, gateway['logicalId'].lower(), intf_name])
                        }],
                    'ips':ips
                    }
            interfaces.append(interface_obj)
        nb_property['intfs'] = interfaces
        nb_property.update(vc_gateway_property)
        rtn = create_device_object(nb_property)
        return rtn

    @staticmethod
    def parsing_vco(instance_name, instance_id, mgmt_ip, vco_role):
        device_type = 30113
        device_type_name = 'VeloCloud Orchestrator'
        driver_id = '3e53e76a-ca24-4561-9b28-efee33b83d59'
        driver_name = 'VeloCloud Orchestrator'
        main_type_name = 'End System'
        main_type_id = 1004
        assign_tag = ['vm']
        vco_name = instance_name.split('.')[0]
        if not vco_name:
            vco_name = 'VCO:' + str(mgmt_ip)
        vco_property = {
            'ver': '',
            'name': vco_name,
            '_id': '',
            'mgmtIP': mgmt_ip
        }

        nb_property = {
            'mainType': main_type_id,
            'mainTypeName': main_type_name,
            'subType': device_type,
            'subTypeName': device_type_name,
            'driverName': driver_name,
            'driverId': driver_id,
            'assignTags': assign_tag,
            'model': 'VeloCloud Orchestrator',
            'vendor': 'VMWARE',
            'multiSources': [{
                'nbPathValue': '/'.join([instance_id, instance_name, vco_role]),
                'nbPathSchema': vco_schema
            }]
        }
        # intfs_data = edge_dict.get('links', [])
        nb_property.update(vco_property)
        rtn = create_device_object(nb_property)
        return rtn


def velocloud_get_config_file(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    nbpathvalue =  tp.nbpathvalue
    dev_name = tp.dev_name

    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request
    enterprise_id = nbpathvalue.rpartition('/')[0].rpartition('/')[2]
    edge_id = nbpathvalue.rpartition('/')[2]

    try:
        body = {
            'enterpriseId': int(enterprise_id),
            'edgeId': int(edge_id)
        }
        api_result = rq.post(endpoint_url + '/portal/rest/edge/getEdgeConfigurationStack', data=json.dumps(body), proxies=proxies)
        if api_result.status_code != 200:
            debug_print('Retrieve configuration stack failed for device %s with state code:%s, error log:%s' % (dev_name,
                api_result.status_code, api_result.text))
            return None
        if api_result.text:
            contents = ['!\r\n!\r\n!\r\n! This config file is generated via API\r\n!\r\n']
            # content += '!\r\n!\r\n! It is observed the full configuration could consume 2M or even larger space\r\n!\r\n'
            # content += '!\r\n!\r\n! the config content here only refer to devicesetting modules\r\n!\r\n'
            # modules = json.loads(api_result.text)[0].get('modules',[])
            # include_list = ['deviceSettings']
            # for module in modules:
            #     name = module.get('name','')
            #     if name not in include_list:
            #         continue
            #     content += '!\r\n!\r\n! module ' + name + '\r\n!\r\n'
            #     content += json.dumps(module, indent=4)
            contents.append(json.dumps(json.loads(api_result.text), indent=4))

            # get link metrics.
            days = 1
            # set to_retrieve_metrics to True. for debug only
            to_retrieve_metrics = True
            if to_retrieve_metrics:
                endtime = int(time.time() * 1000)
                starttime = endtime - 3600 * 1000 * 24 * days
                # enterpriseId(from db) need to convert to integer for this API
                body = {
                'enterpriseId': int(enterprise_id),
                'edgeId': int(edge_id),
                    "interval": {
                        "start": starttime ,
                        "end": endtime
                    }
                }
                edge_metrix = rq.post(endpoint_url + '/portal/rest/metrics/getEdgeLinkMetrics', data=json.dumps(body), proxies=proxies, verify=False)
                if edge_metrix and edge_metrix.text:
                    contents.append(f'\r\n\r\nAPI Result of {endpoint_url}/portal/rest/metrics/getEdgeLinkMetrics')
                    contents.append(f'enterpriseId:{enterprise_id},  edgeId:{edge_id}')
                    contents.append(json.dumps(json.loads(edge_metrix.text), indent=4))

            content = '\r\n'.join(contents)
            node_result = {'data': content, 'original':content, 'log': '', 'status': 1}
        else:
            node_result = {'data': '', 'original':'', 'log': '', 'status': 0}
        return node_result
    except Exception as e:
        msg = traceback.format_exc() + '\r\n' + str(e)
        debug_print('Exception: retrieve configuration msg is:', msg)
        return {'data': '', 'original':'', 'log': '', 'status': 0}


def vco_get_config_file(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request

    original_datas = []
    body = {}
    node_result = {'data': '', 'original':'', 'log': '', 'status': 0}
    try:
        if is_operator:
            api_url = endpoint_url + '/portal/rest/network/getNetworkEnterprises'
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
        else:
            api_url = endpoint_url + '/portal/rest/enterprise/getEnterprise'
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
        if api_result.status_code != 200:
            debug_print('Retrieve enterprise list failed with state code:%s, error log:%s' % (api_result.status_code, api_result.text))
            return node_result
        if api_result.text:
            api_data = json.dumps(json.loads(api_result.text, strict=False), indent=4)
            if api_data:
                original_datas.append(api_url)
                original_datas.append(api_data)
                original_datas.append('\r\n')

        if is_operator:
            enterprise_list = json.loads(api_result.text)
        else:
            enterprise_list = [json.loads(api_result.text)]

        for enterprise in enterprise_list:
            enterprise_id = enterprise.get('id', '')
            if not enterprise_id:
                continue
            # to get the content of enterprise list and edge list only.
            if not is_operator:
                body = {}
            else:
                body = {"enterpriseId": int(enterprise_id)}
            api_url = endpoint_url + '/portal/rest/enterprise/getEnterpriseEdges'
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)

            if api_result.status_code != 200:
                msg  = f'Retrieve enterprise list failed for enterprise id {enterprise_id} with state code:{api_result.status_code}, error log:{api_result.text}'
                debug_print(msg)
                api_name = api_url + f' (for enterprise id {enterprise_id})'
                original_datas.append(api_name)
                original_datas.append(msg)                
            elif api_result.text:
                api_data = json.dumps(json.loads(api_result.text, strict=False), indent=4)
                if api_data:
                    api_name = api_url + f' (for enterprise id {enterprise_id})'
                    original_datas.append(api_name)
                    original_datas.append(api_data)
                    original_datas.append('\r\n')

        if original_datas:
            contents = ['!\r\n!\r\n!\r\n! This config file is generated via API\r\n!\r\n']
            contents.extend(original_datas)
            contents = '\r\n'.join(contents)
            node_result = {'data': contents, 'original':contents, 'log': '', 'status': 1}
        return node_result
    except Exception as e:
        msg = traceback.format_exc() + '\r\n' + str(e)
        debug_print('Exception: retrieve vco configuration failed', msg)
        return {'data': '', 'original':'', 'log': '', 'status': 0}


def get_vco_route_table(input_param):
    
    def parse_one_row(prefer_exit, cidr_ip):
        edge_name = prefer_exit.get('edgeName') or prefer_exit.get('gatewayName') or ''
        if not edge_name:
            return None
        type = prefer_exit.get('type') or ''
        exit_type = prefer_exit.get('exitType') or ''
        protocol = prefer_exit.get('protocol') or ''
        # cidr_ip = prefer_exit['cidrIp']
        # cidr_prefix = prefer_exit['cidrPrefix']
        cost = prefer_exit.get('cost')
        metric = prefer_exit.get('metric')
        # route_type = prefer_exit['routeType']
        # is_advertised = prefer_exit['advertise']
        out_intf = prefer_exit.get('interface') or ''
        nexthop_ip = prefer_exit.get('nextHopIp') or ''
        neighbor_ip = prefer_exit.get('neighborIp') or ''
        state = prefer_exit.get('state') or ''
        algs_list = [exit_type, type]
        alg = ':'.join(algs_list)
        # BGP Attri
        #   "attributes": {
        #   "bgpAttributes": {
        #     "asPathLength": 3,
        #     "localPreference": 100,
        #     "multiExitDiscriminator": 0
        #   }
        bgp_aspath = ''
        bgp_local_pre = ''
        bgp_med = ''
        bgp_attr = (prefer_exit.get('attributes') or {}).get('bgpAttributes')
        if bgp_attr:
            bgp_aspath = bgp_attr.get('asPathLength')
            bgp_local_pre = bgp_attr.get('localPreference')
            bgp_med = bgp_attr.get('multiExitDiscriminator')
        one_row = {
            'DestIp':cidr_ip,
            'DestMask': function.getmaskaddressbylen(int(cidr_mask)),
            'Protocol': protocol,
            'NextHop': nexthop_ip,
            'Metric': metric,
            'Cost': cost,
            'Alg': alg,
            'OutIf': out_intf,
            'Neighbor IP': neighbor_ip,
            'NextDevice': edge_name,
            'State': state,
            'OriginalAlg': alg,
            'AS Path Length': bgp_aspath,
            'Local Preference': bgp_local_pre,
            'Multi Exit Discriminator':bgp_med     
        }
        return one_row
        # if is_advertised:
        #   return one_row
        # else:
        #     debug_print('Skip none-advised rt:' + str(prefer_exit))
        #    return None
                                
        
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    dev_name = tp.dev_name

    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request
    body = {}
    msg = []
    table_name = 'Enterprise Route Table'
    msg.append('Begain to retrieve %s' % table_name)
    nct_table = NCTTable(dev_name, table_name)
    if is_operator:
            api_result = rq.post(
                endpoint_url + '/portal/rest/network/getNetworkEnterprises',
                data=json.dumps(body),
                verify=False)
    else:
        api_result = rq.post(
            endpoint_url + '/portal/rest/enterprise/getEnterprise',
            data=json.dumps(body),
            verify=False)
    msg = []
    if api_result.status_code != 200:
        error_msg = 'Retrieve enterprises list failed with state code:%s, error log:%s' % (
            api_result.status_code, api_result.error)
        debug_print(error_msg)
        msg.append(error_msg)
        nct_table.SetStatus(NCTStatus.Failed)
        nct_table.AddLog('\r\n'.join(msg))
        return nct_table.SaveResult()

    if is_operator:
        enterprise_list = json.loads(api_result.text)
    else:
        enterprise_list = [ json.loads(api_result.text) ]

    rts = {} # key is vrf, value is entries
    for enterprise in enterprise_list:
        enterprise_id = enterprise.get('id', '')
        body = {
            'enterpriseId': enterprise_id
        }
        # get enterprise segments
        segment_id2name = {-1: 'Underlay'}
        segment_text = {}
        segments_api_result = rq.post(endpoint_url + '/portal/rest/enterprise/getEnterpriseNetworkSegments', data=json.dumps(body), proxies=proxies, verify=False)
        if segments_api_result.status_code != 200:
            debug_print('Retrieve getEnterpriseNetworkSegments failed for device %s with state code:%s, error log:%s' % (dev_name,
                segments_api_result.status_code, segments_api_result.text))
        else:
            segments_api_obj = json.loads(segments_api_result.text)
            for i in segments_api_obj or []:
                s_id = i['data']['segmentId']
                s_name = i['name']
                segment_id2name[s_id] = s_name
                segment_text[s_id] = i
        api_result = rq.post(endpoint_url + '/portal/rest/enterprise/getEnterpriseRouteTable', data=json.dumps(body), proxies=proxies, verify=False)
        if api_result.status_code != 200:
            debug_print('Retrieve getEnterpriseRouteTable stack failed for device %s with state code:%s, error log:%s' % (dev_name,
                api_result.status_code, api_result.text))
            return None
        if api_result.text:
            api_result_obj = json.loads(api_result.text)
            for i in api_result_obj.get('subnets') or []:
                subnet = i['subnet'].split(':')
                if len(subnet) >1:
                    cidr_ip_mask, segment_id = subnet[0], subnet[1]
                else:
                    cidr_ip_mask, segment_id = subnet[0], ''
                cidr_ip = cidr_ip_mask.split('/')[0]
                cidr_mask = cidr_ip_mask.split('/')[1]
                # segment_key = segment_id2name.get(int(segment_id)) or segment_id
                try:
                    segment_id = int(segment_id)
                except:
                    pass
                segment_key = segment_id2name.get(segment_id) or segment_id
                segment_api_text = segment_text.get(segment_id) or ''
                if not segment_key:
                    segment_key = 'Underlay'
                key = ':'.join([str(enterprise_id), str(segment_key)])
                if key not in rts:
                    rts[key] = [NCTTable(dev_name, table_name, key), [segment_api_text] if segment_api_text else []]
                    rts[key][0].SetStatus(NCTStatus.Success)
                    rts[key][0].SetColumns([
                        'DestIp', 'DestMask', 'NextHop', 'OutIf',
                        'Neighbor IP','NextDevice', 'Metric','Cost','AS Path Length', 'Local Preference',
                        'Multi Exit Discriminator','Alg', 'Protocol', 'State'
                    ])
                    rts[key][0].SetKeys(['DestIp', 'DestMask', 'NextDevice', 'OutIf'])
                rts[key][1].append(i)
                for prefer_exit in i['preferredExits']:
                    if isinstance(prefer_exit, dict):
                        one_row = parse_one_row(prefer_exit, cidr_ip)
                        if one_row:
                            rts[key][0].AddOneRow(one_row)
                    elif isinstance(prefer_exit, list):
                        for item in prefer_exit:
                            one_row = parse_one_row(item, cidr_ip)
                            if one_row:
                                rts[key][0].AddOneRow(one_row)

    for k, v in rts.items():
        v[0].SetOriginalText(json.dumps(v[1], indent=4))
    new_rts = {}
    for key, value in rts.items():
        if len(value[0]) > 0:
            new_rts[key] = value[0].SaveResult()
    return new_rts        
    #return {key: value[0].SaveResult() for key, value in rts.items()}


def get_edge_route_table(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    nbpathvalue =  tp.nbpathvalue
    dev_name = tp.dev_name

    extra_paras = parse_extra_params(extra_params)
    enterprise_id = nbpathvalue.rpartition('/')[0].rpartition('/')[2]
    edge_id = nbpathvalue.rpartition('/')[2]
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    has_cli = extra_paras.get('has_cli', '')

    # get routing table by CLI if advanced setting of Has CLI Access is true
    ssh_recheable = check_cli_reachability(dev_name)
    if has_cli and ssh_recheable:
        message = 'Has CLI Access is set to True, use CLI to pull data..'
        return 400, {'data': '', 'original': '', 'log': message, 'status': 0}

    body = {}
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    if IS_WORKER_SIDE:
        vc_request.nb_request.set_ap_info(tp._external_srv.fs_id, tp.endpoint_ip)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request

    body = {
        'enterpriseId': enterprise_id,
        'edgeId': edge_id
    }
    api_result = rq.post(endpoint_url + '/portal/rest/edge/getEdgeConfigurationStack', data=json.dumps(body), proxies=proxies)
    if api_result.status_code != 200:
        debug_print('Retrieve configuration stack failed for device %s with state code:%s, error log:%s' % (dev_name,
            api_result.status_code, api_result.text))
        return None
    empty_row = {
        'Index': '',
        'DestIp': '',
        'DestMask': '',
        'NextHop': '',
        'TimeStamp': '',
        'Metric': '',
        'Distance': '',
        'Alg': '',
        'OutIf': '',
        'NextDevice': '',
        'OriginalAlg': ''
    }
    rts = {} # key is vrf, value is entries
    segment_id2name = {-1: 'Underlay'}
    if api_result.text:
        index = 0
        api_result_obj = json.loads(api_result.text)

        # find device_setting module
        # default one
        device_setting_obj = get_child_by_path(api_result_obj, "0.modules.1") or {}
        for root in api_result_obj:
            if root.get('name', '').lower() == 'edge specific profile':
                for module in root.get('modules', []):
                    if module.get('name', '').lower() == 'devicesettings' and module.get('type', '').lower() == 'ENTERPRISE'.lower():
                        device_setting_obj = module
                        break
                break
        # static route
        static_rt_schema = "data.segments"
        sub_static_rt_schema = "routes.static"
        segments = get_child_by_path(device_setting_obj, static_rt_schema)
        for segment in segments or []:
            vrf = segment['segment']['segmentId']
            segment_name = segment['segment']['name']
            segment_id2name[vrf] = segment_name
            st_rt = get_child_by_path(segment, sub_static_rt_schema)
            key = segment_name or str(vrf)
            if key not in rts:
                rts[key] = [RouteTable(dev_name, key), []]
                rts[key][0].SetStatus(NCTStatus.Success)
                rts[key][0].AddOneRow(empty_row)
                rts[key][1].append(segment)
            for i in st_rt or []:
                one_row = {
                    'Index': index + 1,
                    'DestIp': i['destination'],
                    'DestMask': i['netmask'],
                    'NextHop': i['gateway'],
                    'TimeStamp': '',
                    'Metric': i['cost'],
                    'Distance': '',
                    'Alg': 'Static',
                    'OutIf': i['wanInterface'],
                    'NextDevice': '',
                    'OriginalAlg': 'Static'
                }
                if i['advertise']:
                    rts[key][0].AddOneRow(one_row)
                else:
                    debug_print('Skip none-advised rt:' + str(i))
        # routed interface route
        # rtd_intf_schema = "0.modules.1.data.routedInterfaces"
        rtd_intf_schema = "data.routedInterfaces"
        rtd_intfs = get_child_by_path(device_setting_obj, rtd_intf_schema)

        # for sub interface
        sub_intfs = []
        for rtd_intf in rtd_intfs or []:
            sub_intfs.extend(rtd_intf.get('subinterfaces') or [])

        rtd_intfs.extend(sub_intfs)
        for rtd_intf in rtd_intfs:
            addressing = rtd_intf['addressing']
            gateway = addressing['gateway']
            if not gateway:
                continue
            cidr_ip = addressing['cidrIp']
            mask = addressing['netmask']
            if not (cidr_ip and mask):
                continue
            network_address = IP(' '.join([cidr_ip, mask])).NetworkAddress()
            one_row = {
                'Index': index + 1,
                'DestIp': network_address,
                'DestMask': mask,
                'NextHop': gateway,
                'TimeStamp': '',
                'Metric': '',
                'Distance': '',
                'Alg': 'Static',
                'OutIf': '',
                'NextDevice': '',
                'OriginalAlg': 'Static'
            }
            vrf = rtd_intf['segmentId']
            segment_name = segment_id2name.get(vrf) or ''
            key = segment_name or str(vrf)
            if key not in rts:
                rts[key] = [RouteTable(dev_name, key), []]
                rts[key][0].SetStatus(NCTStatus.Success)
                rts[key][0].AddOneRow(empty_row)
            rts[key][0].AddOneRow(one_row)
            rts[key][1].append(rtd_intf)

    for v in rts.values():
        v[0].SetOriginalText(json.dumps(v[1], indent=4))
    return {key: value[0].SaveResult() for key, value in rts.items()}


@debugthis
def check_cli_reachability(dev_name):
    try:
        cli_data = GetCLIData(dev_name, "debug.py --interfaces")
        if cli_data.data:
            return True
    except:
        pass
    return False


def get_edge_ipsec_table(input_param):
    def parse_tunnel_info(dev_name, link_logical_id):
        dev_obj = datamodel.GetDevice(dev_name)
        ms = dev_obj.GetProperty('multiSources') if dev_obj else None
        if ms:
            nbpathvalue, nbPathSchema = '' , ''
            for item in ms:
                if item['nbPathSchema'].lower().startswith('velocloud'):
                    nbpathvalue = item['nbPathValue']
                    nbPathSchema = item['nbPathSchema']
                    break
            else:
                return '', ''
            node_query = {
                "nbPathValue": nbpathvalue,
                "nbPathSchema": nbPathSchema
            }
            nodes = QueryNodeObjects('VELOCLOUD', node_query)
            if not nodes:
                debug_print('can not find data in VELOCLOUD_Node for device:', dev_name)
            else:
                node = nodes[0]
                links = node.get('links', [])
                if links:
                    for link in links:
                        link_internal_id = link.get('internalId', '')
                        local_public_ip, intf = '', ''
                        if link_internal_id == link_logical_id:
                            local_public_ip = link.get('ipAddress', '')
                            intf = link.get('interface', '')
                        if local_public_ip and intf:
                            return intf, local_public_ip
        return '', ''

    def get_one_row(metric_obj, parsed_list):
        one_row = {
                'Interface': '',
                'Link Name': '',
                'Crypto Map': '',
                'VRF Name': '',
                'IPsec VPN Local IP':'',
                'IPsec VPN Local Public IP': '',
                'IPsec VPN Remote IP': '',
                'Peer Name': '',
                'Source Traffic IP':'',
                'Source Traffic Mask':'',
                'Destination Traffic IP': '',
                'Destination Traffic Mask': '',
                'Remote Link Name': '',
                'RX State': '',
                'TX State': '',
                'Status': ''
            }
        source = metric_obj.get('source', {})
        destination = metric_obj.get('destination', {})
        status = metric_obj.get('status', '')
        #to save calculation, use parsed_list to store the parsed link info
        # parsed_list = {}
        local_intf = ''
        link_name = ''
        local_public_ip = ''
        remote_public_ip = ''
        peer_name = ''
        remote_link_name = ''
        if source:
            link_name = source.get('linkName', '')
            link_logical_id = source.get('linkLogicalId', '')
            dev_name = source.get('deviceName', '')
            if link_logical_id in parsed_list:
                local_intf = parsed_list[link_logical_id]['intf']
                local_public_ip = parsed_list[link_logical_id]['local_ip']
            else:
                local_intf, local_public_ip = parse_tunnel_info(dev_name, link_logical_id)
                if local_intf and local_public_ip:
                    parsed_list[link_logical_id] = {'intf':local_intf, 'local_ip':local_public_ip}
        if destination:
            remote_link_name = destination.get('linkName', '')
            link_logical_id = destination.get('linkLogicalId', '')
            peer_name = destination.get('deviceName', '')
            if link_logical_id in parsed_list:
                remote_intf = parsed_list[link_logical_id]['intf']
                remote_public_ip = parsed_list[link_logical_id]['local_ip']
            else:
                remote_intf, remote_public_ip = parse_tunnel_info(peer_name,link_logical_id)
                if remote_intf and remote_public_ip:
                    parsed_list[link_logical_id] = {'intf':remote_intf, 'local_ip':remote_public_ip}

        if local_intf and local_public_ip and remote_public_ip:
            one_row['Interface'] = local_intf
            one_row['Link Name'] = link_name
            one_row['IPsec VPN Local IP'] = local_public_ip
            # one_row['IPsec VPN Local Public IP'] = local_public_ip
            one_row['IPsec VPN Remote IP'] = remote_public_ip
            one_row['Peer Name'] = peer_name
            one_row['Remote Link Name'] = remote_link_name
            one_row['Status'] = status
            return one_row
        else:
            # debug_print('invalid tunnel info', local_intf , local_public_ip , remote_public_ip)
            return None

    tp = TableParams(input_param, root_schema)
    extra_paras = parse_extra_params(tp.extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    has_cli = extra_paras.get('has_cli', '')
    prefer_cli_for_ipsec = extra_paras.get('prefer_cli_for_ipsec', '')
    if len(tp.nbpathvalue.split('/')) == 4:
        enterprise_id = int(tp.nbpathvalue.split('/')[2])
        edge_id = int(tp.nbpathvalue.split('/')[3])
    else:
        return ''

    # check CLI preference setting
    if has_cli and prefer_cli_for_ipsec:
        is_ssh_recheable = False
        is_ssh_recheable = check_cli_reachability(tp.dev_name)
        if is_ssh_recheable:
            message = 'prefer CLI for ipsec data is set, SSH is recheable. use CLI to pull data..'
            return 400, {'data': '', 'original': '', 'log': message, 'status': 0}
        else:
            debug_print('has_cli and prefer_cli_for_ipsec are set, how ever CLI is not recheable.')

    vc_request = VCRequest(tp.endpoint, tp.username, tp.password, proxies, is_operator)
    tp = TableParams(input_param, 'VELOCLOUD')
    if IS_WORKER_SIDE:
        vc_request.nb_request.set_ap_info(tp._external_srv.fs_id, tp.endpoint_ip)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request

    body = {
        'enterpriseId': enterprise_id,
        'edgeId': edge_id
    }

    table_name = "IPsec VPN Table[Real-time]"
    sub_name = ''
    ipsec_table = NCTTable(tp.dev_name, table_name, sub_name)
    ipsec_table.SetColumns(
        ['Interface', 'Link Name', 'Crypto Map', 'VRF Name', 'IPsec VPN Local IP', 'IPsec VPN Local Public IP',
         'IPsec VPN Remote IP', 'Peer Name', 'Source Traffic IP', 'Source Traffic Mask', 'Destination Traffic IP',
         'Destination Traffic Mask', 'Remote Link Name', 'RX State', 'TX State', 'Status'])
    ipsec_table.SetKeys(['Interface', 'Link Name', 'IPsec VPN Local IP', 'IPsec VPN Remote IP'])
    has_data = False

    try:
        save_original_data = True
        original_datas = []
        # get SD-WAN peers info
        # some customer environments don't have a result
        api_url = tp.endpoint + "/portal/rest/edge/getEdgeSDWANPeers"
        sdwan_peer_api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
        if sdwan_peer_api_result.status_code != 200:
            debug_print('Retrieving sd-wan peer status failed for device %s with state code:%s, error log:%s' % (tp.dev_name,
                sdwan_peer_api_result.status_code, sdwan_peer_api_result.text))
            return None
        if sdwan_peer_api_result.text:
            sdwan_peers = json.loads(sdwan_peer_api_result.text, strict=False)
            if save_original_data:
                original_datas.append({api_url: sdwan_peers})
            peer_device_logical_id_list = []
            for peer in sdwan_peers:
                device_logical_id = peer.get('deviceLogicalId', '')
                if device_logical_id and device_logical_id not in peer_device_logical_id_list:
                    peer_device_logical_id_list.append(device_logical_id)

            # get VPN metrics info to each peer
            parsed_list = {}
            if peer_device_logical_id_list:
                for device_logcial_id in peer_device_logical_id_list:
                    metric_body = {
                    'enterpriseId': enterprise_id,
                    'edgeId': edge_id,
                    'peerLogicalId': str(device_logcial_id)
                    }
                    api_url = tp.endpoint + "/portal/rest/metrics/getEdgeSDWANPeerPathMetrics"
                    metric_api_result = rq.post(api_url, data=json.dumps(metric_body), proxies=proxies)
                    if metric_api_result.status_code != 200:
                        debug_print('Retrieve sd-wan metric failed for peer with id %s with state code:%s, error log:%s' % (device_logcial_id,
                            metric_api_result.status_code, metric_api_result.text))
                        continue
                    if metric_api_result.text:
                        metric_obj_list = json.loads(metric_api_result.text, strict=False)
                        if save_original_data:
                            original_datas.append({api_url: metric_obj_list})
                        for metric_obj in metric_obj_list:
                            one_row = get_one_row(metric_obj, parsed_list)
                            if one_row:
                                ipsec_table.AddOneRow(one_row)
                                has_data = True

        if has_data:  # successful
            ipsec_table.SetStatus(NCTStatus.Success)
            msg = 'Retrieve ipsec table successfully.'
            ipsec_table.AddLog(msg)
        else:  # failed
            ipsec_table.SetStatus(NCTStatus.NA)
            msg = 'No ipsec data.'
            ipsec_table.AddLog(msg)
        debug_print('End getting ipsec table for device {0}'.format(tp.dev_name))
        ipsec_table.SetOriginalText(json.dumps(original_datas, indent=4))
        return ipsec_table.SaveResult()
    except Exception as e:
        msg = traceback.format_exc() + '\r\n' + str(e)
        debug_print('Exception: retrieve ipsec table experienced with exception:', msg)
        return ''


def velocloud_get_handoff_table(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    nbpathvalue =  tp.nbpathvalue
    dev_name = tp.dev_name
    gateway_logical_id = nbpathvalue.split('/')[1]
    gateway_id = nbpathvalue.split('/')[2]

    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request

    debug_print(f'Start to get handoff assignments table for gateway {dev_name}')
    table_name = 'Handoff Assignments Table'
    sub_name = ''
    handoff_table = NCTTable(dev_name, table_name, sub_name)
    handoff_table.SetColumns(
        ['Enterprise ID', 'Enterprise Name', 'Handoff cTag', 'Segment ID', 'Segment Name', 'Local IP', 'BGP Peer IP', 'Edge List'])
    handoff_table.SetKeys(['Enterprise ID', 'Segment ID'])
    has_data = False

    original_datas = []
    try:
        # get all edges and its enterprises
        body = {
            'gatewayId': gateway_id
        }
        api_url = endpoint_url + '/portal/rest/gateway/getGatewayEdgeAssignments'
        api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
        if api_result.status_code != 200:
            debug_print('Retrieve handoff assignments table failed for gateway %s with state code:%s, error log:%s' % (dev_name,
                api_result.status_code, api_result.text))
            return None
        debug_print('API output:', api_result.text)
        edge_assignment_api_result = json.loads(api_result.text, strict=False)
        # debug_print('API output in json format:', edge_assignment_api_result)
        original_datas.append({api_url: edge_assignment_api_result})
        enterprise_dict = {}
        edge_list_dict = {}
        for item in edge_assignment_api_result:
            enterprise_id = item['enterpriseId'] if 'enterpriseId' in item else ''
            enterprise_name = item['enterpriseName'] if 'enterpriseName' in item else ''
            edge_name = item['name'] if 'name' in item else ''
            if enterprise_id not in enterprise_dict and enterprise_id and enterprise_name and edge_name:
                enterprise_dict[enterprise_id] = enterprise_name
                edge_list_dict[enterprise_id] = []
                edge_list_dict[enterprise_id].append(edge_name)
            elif enterprise_id in edge_list_dict and edge_name:
                edge_list_dict[enterprise_id].append(edge_name)
        for enterprise_id in enterprise_dict:
            body = {
                'enterpriseId': enterprise_id
            }
            api_url = endpoint_url + '/portal/rest/enterprise/getEnterpriseGatewayHandoff'
            debug_print('calling getEnterpriseGatewayHandoff API')
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
            if api_result.status_code != 200:
                debug_print('Retrieve handoff assignments table failed for enterprise %s with state code:%s, error log:%s' % (enterprise_dict[enterprise_id],
                    api_result.status_code, api_result.text))
                return None
            debug_print('API output:', api_result.text)
            enterprise_assignment_api_result = json.loads(api_result.text, strict=False).get('value',{}).get('segments',[])
            # debug_print('API output in json format:', enterprise_assignment_api_result)
            original_datas.append({api_url: enterprise_assignment_api_result})
            if enterprise_assignment_api_result:
                vlan_info = enterprise_assignment_api_result[0].get('overrides',{}).get('VLAN',{})
                address_info = enterprise_assignment_api_result[0].get('overrides',{}).get('localAddress',{})
                bgp_info = enterprise_assignment_api_result[0].get('overrides',{}).get('bgp',{})
                segment_id = enterprise_assignment_api_result[0].get('segment',{}).get('segmentId','')
                segment_name = enterprise_assignment_api_result[0].get('segment',{}).get('name','')
                # debug_print('vlan_info:', vlan_info)
                # debug_print('address_info:', address_info)
                if vlan_info and address_info:
                    handoff_ctag = 0
                    for logical_id in vlan_info:
                        info = vlan_info[logical_id]
                        if logical_id == gateway_logical_id and info['type'] in ['802.1Q', 'QinQ (0x8100)']:
                            handoff_ctag = info['cTag']
                            break
                    local_ip = ''
                    for logical_id in address_info:
                        info = address_info[logical_id]
                        if logical_id == gateway_logical_id and info['cidrIp']:
                            local_ip= info['cidrIp']
                            break
                    peer_ip = ''
                    for logical_id in bgp_info:
                        info = bgp_info[logical_id]
                        if logical_id == gateway_logical_id and info['neighborIp']:
                            peer_ip= info['neighborIp']
                            break
                    debug_print('handoff_ctag:', handoff_ctag)
                    if handoff_ctag != 0:
                        one_row = {
                            'Enterprise ID': enterprise_id,
                            'Enterprise Name': enterprise_dict[enterprise_id],
                            'Handoff cTag': handoff_ctag,
                            'Segment ID': segment_id,
                            'Segment Name': segment_name,
                            'Local IP': local_ip,
                            'BGP Peer IP': peer_ip,
                            'Edge List': ';'.join(edge_list_dict[enterprise_id]),
                        }
                        handoff_table.AddOneRow(one_row)
                        has_data = True

        if has_data:  # successful
            handoff_table.SetStatus(NCTStatus.Success)
            msg = 'Retrieve handoff assignments table successfully.'
            handoff_table.AddLog(msg)
        else:  # failed
            handoff_table.SetStatus(NCTStatus.NA)
            msg = 'No handoff assignments table found.'
            handoff_table.AddLog(msg)
        debug_print('End getting handoff assignments table {0}'.format(dev_name))
        handoff_table.SetOriginalText(json.dumps(original_datas, indent=4))
        return handoff_table.SaveResult()
    except Exception as e:
        msg = traceback.format_exc() + '\r\n' + str(e)
        debug_print('Exception: retrieve handoff assignments table experienced with exception:', msg)
        return ''


def velocloud_get_bgp_neighbor_table(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params
    nbpathvalue =  tp.nbpathvalue
    dev_name = tp.dev_name
    gateway_logical_id = nbpathvalue.split('/')[1]
    gateway_id = nbpathvalue.split('/')[2]

    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request

    debug_print(f'Start to get vcg bgp neighbor table for gateway {dev_name}')
    table_name = 'VCG BGP Neighbor Table'
    sub_name = ''
    vcg_bgp_table = NCTTable(dev_name, table_name, sub_name)
    vcg_bgp_table.SetColumns(['Enterprise ID', 'Enterprise Name', 'Segment ID', 'Segment Name', 'Local AS',  'Neighbor AS', 'Local IP', 'Neighbor IP', 'Up Time', 'Msg Received', 'Msg Send', 'Pfx Received'])
    vcg_bgp_table.SetKeys(['Enterprise ID', 'Segment ID', 'Local IP', 'Neighbor IP'])
    has_data = False

    original_datas = []
    try:
        # get all enterprises
        body = {
            'gatewayId': gateway_id
        }
        api_url = endpoint_url + '/portal/rest/gateway/getGatewayEdgeAssignments'
        api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
        if api_result.status_code != 200:
            debug_print('Retrieve getGatewayEdgeAssignments failed for gateway %s with state code:%s, error log:%s' % (dev_name,
                api_result.status_code, api_result.text))
            return None
        debug_print('API output:', api_result.text)
        edge_assignment_api_result = json.loads(api_result.text, strict=False)
        # debug_print('API output in json format:', edge_assignment_api_result)
        original_datas.append({api_url: edge_assignment_api_result})
        enterprise_dict = {}
        for item in edge_assignment_api_result:
            enterprise_id = item['enterpriseId'] if 'enterpriseId' in item else ''
            enterprise_name = item['enterpriseName'] if 'enterpriseName' in item else ''
            if enterprise_id not in enterprise_dict and enterprise_id and enterprise_name:
                enterprise_dict[enterprise_id] = enterprise_name

        for enterprise_id in enterprise_dict:
            body = {
                'enterpriseId': enterprise_id
            }
            api_url = endpoint_url + '/portal/rest/enterprise/getEnterpriseGatewayHandoff'
            debug_print('calling API getEnterpriseGatewayHandoff')
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
            if api_result.status_code != 200:
                debug_print('Retrieve getEnterpriseGatewayHandoff failed for enterprise %s with state code:%s, error log:%s' % (enterprise_dict[enterprise_id],
                    api_result.status_code, api_result.text))
                return None
            debug_print('API output:', api_result.text)
            enterprise_assignment_api_result = json.loads(api_result.text, strict=False).get('value',{}).get('segments',[])
            # debug_print('API output in json format:', enterprise_assignment_api_result)
            original_datas.append({api_url: enterprise_assignment_api_result})

            api_url = endpoint_url + '/portal/rest/monitoring/getEnterpriseBgpPeerStatus'
            debug_print('calling API getEnterpriseBgpPeerStatus')
            api_result = rq.post(api_url, data=json.dumps(body), proxies=proxies)
            if api_result.status_code != 200:
                debug_print('Retrieve getEnterpriseBgpPeerStatus failed for enterprise %s with state code:%s, error log:%s' % (enterprise_dict[enterprise_id],
                    api_result.status_code, api_result.text))
                return None
            # debug_print('API output:', api_result.text)
            bgp_status_api_result = json.loads(api_result.text, strict=False)
            # debug_print('API output in json format:', bgp_status_api_result)
            # original_datas.append({api_url: bgp_status_api_result})
            # multiple msg records for one gateway found, only use the most recent record
            bgp_status = {}
            for item in bgp_status_api_result:
                if gateway_logical_id in item['gatewayLogicalId']:
                    bgp_status = item['data']
                    break

            if enterprise_assignment_api_result:
                for segment in enterprise_assignment_api_result:
                    address_info = segment.get('overrides',{}).get('localAddress',{})
                    bgp_info = segment.get('overrides',{}).get('bgp',{})
                    segment_id = segment.get('segment',{}).get('segmentId','')
                    segment_name = segment.get('segment',{}).get('name','')
                    local_ip = ''
                    for key in address_info:
                        if gateway_logical_id in key:
                            local_ip = address_info[key]['cidrIp']
                            break
                    local_as = ''
                    for key in bgp_info:
                        if gateway_logical_id in key:
                            local_as = bgp_info[key]['ASN']
                            break
                    if local_ip and local_as and bgp_status:
                        one_row = {
                            'Enterprise ID': enterprise_id,
                            'Enterprise Name': enterprise_dict[enterprise_id],
                            'Segment ID': segment_id,
                            'Segment Name': segment_name,
                            'Local AS': local_as,
                            'Neighbor AS':bgp_status['neighborAS'] if 'neighborAS' in bgp_status else '',
                            'Local IP': local_ip,
                            'Neighbor IP': bgp_status['neighborIp'] if 'neighborIp' in bgp_status else '',
                            'Up Time':bgp_status['upDownTime'] if 'upDownTime' in bgp_status else '',
                            'Msg Received': bgp_status['msgRcvd'] if 'msgRcvd' in bgp_status else '',
                            'Msg Send': bgp_status['msgSent'] if 'msgSent' in bgp_status else '',
                            'Pfx Received':bgp_status['pfxRcvd'] if 'pfxRcvd' in bgp_status else '',
                        }
                        vcg_bgp_table.AddOneRow(one_row)
                        has_data = True

        if has_data:  # successful
            vcg_bgp_table.SetStatus(NCTStatus.Success)
            msg = 'Retrieve VeloCloud VCG BGP Neighbor table successfully.'
            vcg_bgp_table.AddLog(msg)
        else:  # failed
            vcg_bgp_table.SetStatus(NCTStatus.NA)
            msg = 'No VeloCloud VCG BGP Neighbor table found.'
            vcg_bgp_table.AddLog(msg)
        debug_print('End Retrieving VeloCloud VCG BGP Neighbor table {0}'.format(dev_name))
        vcg_bgp_table.SetOriginalText(json.dumps(original_datas, indent=4))
        return vcg_bgp_table.SaveResult()
    except Exception as e:
        msg = traceback.format_exc() + '\r\n' + str(e)
        debug_print('Exception: retrieve VeloCloud VCG BGP Neighbor table experienced with exception:', msg)
        return ''


def _test(param):
    try:
        param = json.loads(param)
        #print('param:', param)
        url = param['endpoint'] if 'endpoint' in param else ''
        user = param['username'] if 'username' in param else ''
        pwd = param['password'] if 'password' in param else ''
        _extra_info = param['extraParams'] if 'extraParams' in param else None
        extra_paras = parse_extra_params(_extra_info)
        proxies = extra_paras.get('proxies', '')
        is_operator = extra_paras.get('is_operator', '')

        # raise ValueError('is_operator:', is_operator, proxies)
        test_rtn = {'isFailed': False}
        err_msg = ''
        if is_operator:
            # operator login
            login_url = '/portal/rest/login/operatorLogin'
        else:
            # enterprise login
            login_url = '/portal/rest/login/enterpriseLogin'
        body = {
            "password": pwd,
            "username": user
        }

        test_rtn['msg'] = ''
        success = False
        try:
            res = new_post(url + login_url, json.dumps(body), proxies=proxies, verify=False)
            err_msg += '\r\n API test result as following:'
            err_msg += '\r\n status_code:' + str(res.status_code)
            if _is_debug:
                err_msg += '\r\n headers:' + str(res.headers)
            err_msg += '\r\n text:' + str(res.text)

            if res.status_code == 200 and not res.text.startswith('<html>'):
                if 'Set-Cookie' in res.headers:
                    success = True
                else:
                    err_msg += '\r\n ' + 'API RETURNS WITH STATUS CODE 200. HOWEVER NO COOKIE COULD BE FOUND IN HEADER'
                    err_msg += '\r\n ' + 'PLEASE CHECK IF THE VCO ACCOUNT IS GRANT RIGHT PRIVILEGES OR IF SSO RESTRICTION'
        except Exception as e:
            error_log = 'Failed to get cookie headers, with error:%s'%str(e)
            error_log += traceback.format_exc()
            #msg.append(error_log)
            err_msg += '\r\n' + error_log

        if success:
            test_rtn['msg'] = err_msg
            return 200, json.dumps(test_rtn)
        else:
            err_msg += '\r\n ' + 'Authentication failed to VCO'
            test_rtn['isFailed'] = True
            test_rtn['msg'] = err_msg
            return 400, json.dumps(test_rtn)
    except Exception as e:
        debug_print(traceback.format_exc())
        return 400, json.dumps({'isFailed': True, 'msg': 'Exception' + str(e)})


def parse_extra_params(_extra_info):
    proxies = {}
    is_operator = False
    has_cli = False
    prefer_private_wired_as_mgmt_ip = False
    autoset_snmp = False
    prefer_cli_for_ipsec = False
    prefer_loopback_as_mgmt_ip = False
    loopback_priority_sequence = ''
    lan_preferential_order = ''
    
    adjust_default_discover_behavior = False
    solo_scan_edges = []
    solo_scan_enterprices = []
    discover_new_appliance_only = False
    
    if _extra_info is not None:
        if isinstance(_extra_info, list):
            for item in _extra_info:
                if 'key' in item and 'proxy' == item['key']:
                    proxies.update({'http': item['value'], 'https': item['value']})
                if 'key' in item and 'is_operator' == item['key']:
                    is_operator = True if (item['value'].lower() and item['value'].lower() != 'false') else False
                if 'key' in item and 'has_cli' == item['key']:
                    has_cli = True if (item['value'].lower() and item['value'].lower() == 'true') else False
                if 'key' in item and 'prefer_private_wired_as_mgmt_ip' == item['key']:
                    prefer_private_wired_as_mgmt_ip = True if (item['value'].lower() and item['value'].lower() == 'true') else False
                if 'key' in item and 'autoset_snmp' == item['key']:
                    autoset_snmp = True if (item['value'].lower() and item['value'].lower() == 'true') else False
                if 'key' in item and 'prefer_cli_for_ipsec' == item['key']:
                    prefer_cli_for_ipsec = True if (item['value'].lower() and item['value'].lower() == 'true') else False
                if 'key' in item and 'prefer_loopback_as_mgmt_ip' == item['key']:
                    prefer_loopback_as_mgmt_ip = True if (item['value'].lower() and item['value'].lower() == 'true') else False
                if 'key' in item and 'loopback_priority_sequence' == item['key']:
                    loopback_priority_sequence = item['value']
                if 'key' in item and 'lan_preferential_order' == item['key']:
                    lan_preferential_order = item['value']
                if 'key' in item and 'adjust_default_discover_behavior' == item['key']:
                    adjust_default_discover_behavior = True if (item['value'].lower() and item['value'].lower() == 'true') else False                    
                if 'key' in item and 'solo_scan_edges' == item['key']:
                    solo_scan_edges = item['value'].split(';')
                if 'key' in item and 'solo_scan_enterprices' == item['key']:
                    solo_scan_enterprices = item['value'].split(';')
                if 'key' in item and 'discover_new_appliance_only' == item['key']:
                    discover_new_appliance_only = True if (item['value'].lower() and item['value'].lower() == 'true') else False                                                               
        else:
            if 'proxy' in _extra_info:
                proxies.update({'http': _extra_info['proxy'], 'https': _extra_info['proxy']})
            if (_extra_info.get('is_operator', '').lower() and _extra_info.get('is_operator', '').lower() != 'false'):
                is_operator = True
            if (_extra_info.get('has_cli', '').lower() and _extra_info.get('has_cli', '').lower() == 'true'):
                has_cli = True
            if (_extra_info.get('prefer_private_wired_as_mgmt_ip', '').lower() and _extra_info.get('prefer_private_wired_as_mgmt_ip', '').lower() == 'true'):
                prefer_private_wired_as_mgmt_ip = True
            if (_extra_info.get('autoset_snmp', '').lower() and _extra_info.get('autoset_snmp', '').lower() == 'true'):
                autoset_snmp = True
            if (_extra_info.get('prefer_cli_for_ipsec', '').lower() and _extra_info.get('prefer_cli_for_ipsec', '').lower() == 'true'):
                prefer_cli_for_ipsec = True
            if (_extra_info.get('prefer_loopback_as_mgmt_ip', '').lower() and _extra_info.get('prefer_loopback_as_mgmt_ip', '').lower() == 'true'):
                prefer_loopback_as_mgmt_ip = True
            if _extra_info.get('loopback_priority_sequence', ''):
                loopback_priority_sequence = _extra_info.get('loopback_priority_sequence')
            if _extra_info.get('lan_preferential_order', ''):
                lan_preferential_order = _extra_info.get('lan_preferential_order')
            if (_extra_info.get('adjust_default_discover_behavior', '').lower() and _extra_info.get('adjust_default_discover_behavior', '').lower() == 'true'):
                adjust_default_discover_behavior = True
            if _extra_info.get('solo_scan_edges', ''):
                solo_scan_edges = _extra_info.get('solo_scan_edges').split(';')
            if _extra_info.get('solo_scan_enterprices', ''):
                solo_scan_enterprices = _extra_info.get('solo_scan_enterprices').split(';')
            if (_extra_info.get('discover_new_appliance_only', '').lower() and _extra_info.get('discover_new_appliance_only', '').lower() == 'true'):
                discover_new_appliance_only = True                                                                     

    return {
        'proxies': proxies,
        'is_operator': is_operator,
        'has_cli': has_cli,
        'prefer_private_wired_as_mgmt_ip': prefer_private_wired_as_mgmt_ip,
        'autoset_snmp': autoset_snmp,
        'prefer_cli_for_ipsec': prefer_cli_for_ipsec,
        'prefer_loopback_as_mgmt_ip': prefer_loopback_as_mgmt_ip,
        'loopback_priority_sequence': loopback_priority_sequence,
        'lan_preferential_order': lan_preferential_order,
        'adjust_default_discover_behavior': adjust_default_discover_behavior,
        'solo_scan_edges': solo_scan_edges,
        'solo_scan_enterprices': solo_scan_enterprices,
        'discover_new_appliance_only': discover_new_appliance_only
        }


def getData(input_param):
    tp = TableParams(input_param, root_schema)
    endpoint_url = tp.endpoint
    username = tp.username
    password = tp.password
    extra_params = tp.extra_params

    sub_url = input_param.get('url', '')
    body = input_param.get('body', '')
    full_url = '/'.join([endpoint_url, sub_url])
    extra_paras = parse_extra_params(extra_params)
    proxies = extra_paras.get('proxies', '')
    is_operator = extra_paras.get('is_operator', '')
    # get edge list for specific enterprise
    # https://xxxx/portal/rest/enterprise/getEnterpriseEdges
    # data params must be a json str for this url post
    vc_request = VCRequest(endpoint_url, username, password, proxies, is_operator)
    vc_request.nb_request.set_request_params(**vc_request.get_authen_headers())
    rq = vc_request.nb_request
    api_result = rq.post(full_url, data=json.dumps(body))
    if api_result.status_code != 200:
        error_print('Retrieve edges list failed with state code:%s, error log:%s' % (
            api_result.status_code, api_result.error))
        return None
    return api_result.text
