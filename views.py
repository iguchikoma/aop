import json
import logging
import csv
import re
import socket
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from lib.smartemttelnetlib import SmartemtTelnetlib

#TODO(takashi.iguchi@ntt.com)  logger configuration should change dict_configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

NE_IP_ADDR = "192.168.10.228"
NE_LOGIN_ID = "somebody\n"
NE_PASS = "\n"

sample_data = {"username":"vifip99", "interface":"vif2", "src-ip":"2.2.2.2/24", "route":"0.0.0.0/0", "gateway":"2.2.2.1"}

@csrf_exempt
def cfgs_crud(request):
    if request.method == "GET":
        output = get_config()
        response = HttpResponse(json.dumps(output))
        response["Access-Control-Allow-Origin"] = "*"
        return response

@csrf_exempt
def vrfs_crud(request):
    if request.method == "GET":
        output = []
        output = get_config()
        response = HttpResponse(json.dumps(output))
        response["Access-Control-Allow-Origin"] = "*"
        return response
    elif request.method == "POST":
        # logger.debug("raw_body = %s , type = %s", request.body, type(request.body))
        json_body = json.loads(request.body)
        logger.debug("json_body = %s , type = %s", json_body, type(json_body))
        config_vrf(json_body)
#        for ne_type in json_body:
#            insert_ne_type(ne_type)
        return HttpResponse(status=204)
    elif request.method =="DELETE":
        json_body = json.loads(request.body)
#        for ne_type in json_body:
#            delete_ne_type(ne_type)
        response = HttpResponse(status=204)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    elif request.method == "OPTIONS":
        return preflight_response()

@csrf_exempt
def targets_crud(request):
    if request.method == "GET":
        output = []
        output = get_config()
        response = HttpResponse(json.dumps(output))
        response["Access-Control-Allow-Origin"] = "*"
        return response
    elif request.method == "POST":
        # logger.debug("raw_body = %s , type = %s", request.body, type(request.body))
        json_body = json.loads(request.body)
        logger.debug("json_body = %s , type = %s", json_body, type(json_body))
        config_target(json_body)
#        for ne_type in json_body:
#            insert_ne_type(ne_type)
        return HttpResponse(status=204)

def preflight_response():
    response = HttpResponse("")
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Methods'] = "DELETE, OPTIONS"
    #response['Access-Control-Allow-Headers'] = "X-Requested-With"
    response['Access-Control-Max-Age'] = "1800"
    return response

def config_vrf(input_json):
    username = input_json["username"]
    interface = input_json["interface"]
    src_ip = input_json["src-ip"]
    route = input_json["route"]
    gw = input_json["gateway"]
    create_ip_instance = u"create ip instance %s interface %s %s\n" %(username, interface, src_ip)
    create_ip_route = u"create ip route %s gateway %s in %s\n" %(route, gw, username)
    # logger.debug("%s", create_ip_instance)
    # logger.debug("%s", create_ip_route)
    client = SmartemtTelnetlib(ne_ip_addr = NE_IP_ADDR, login_id = NE_LOGIN_ID, password = NE_PASS)
    try:
        client.telnet_connect()
    except:
        raise
    else:
        try:
            client.exec_cmd(create_ip_instance)
            client.exec_cmd(create_ip_route)
        finally:
            client.telnet_disconnect()

def config_target(input_json):
    targetname = input_json["targetname"]
    mode = input_json["mode"]
    targetip = input_json["targetip"]
    ip = input_json["ip"]
    index = input_json["index"]
    upcount = input_json["upcount"]
    downcount = input_json["downcount"]
    normaltxinterval = input_json["normaltxinterval"]
    checktxinterval = input_json["checktxinterval"]
    normalrxtimeout = input_json["normalrxtimeout"]
    checkrxtimeout = input_json["checkrxtimeout"]
    statsaverage = input_json["statsaverage"]
    delaythreshold = input_json["delaythreshold"]
    framelength = input_json["framelength"]
    ttl = input_json["ttl"]

    create_icmpmng = u"create icmpmng %s mode %s target %s ip %s index %s\n" %(targetname, mode, targetip, ip, index)
    set_icmpmng_txframe = u"set icmpmng %s txframe length %s ttl %s\n" %(targetname, framelength, ttl)
    set_icmpmng_state = u"set icmpmng %s state count %s %s interval %s %s timeout %s %s\n" %(targetname, upcount, downcount, normaltxinterval, checktxinterval, normalrxtimeout, checkrxtimeout)
    set_icmpmng_stats = u"set icmpmng %s stats average %s delay %s\n" %(targetname, statsaverage, delaythreshold)
    set_icmpmng_on = u"set icmpmng %s mnglog on\n" %(targetname)
    enable_icmpmng = u"enable icmpmng %s\n" %(targetname)

    client = SmartemtTelnetlib(ne_ip_addr = NE_IP_ADDR, login_id = NE_LOGIN_ID, password = NE_PASS)
    try:
        client.telnet_connect()
    except:
        raise
    else:
        try:
            client.exec_cmd(create_icmpmng)
            client.exec_cmd(set_icmpmng_txframe)
            client.exec_cmd(set_icmpmng_state)
            client.exec_cmd(set_icmpmng_stats)
            client.exec_cmd(set_icmpmng_on)
            client.exec_cmd(enable_icmpmng)
        finally:
            client.telnet_disconnect()

def get_config():
    gl_res = {"config":[]}
    client = SmartemtTelnetlib(ne_ip_addr = NE_IP_ADDR, login_id = NE_LOGIN_ID, password = NE_PASS)
    try:
        client.telnet_connect()
    except:
        raise
    else:
        try:
            gl_res["config"] = client.exec_cmd("show config\n")
        finally:
            client.telnet_disconnect()
    return gl_res

