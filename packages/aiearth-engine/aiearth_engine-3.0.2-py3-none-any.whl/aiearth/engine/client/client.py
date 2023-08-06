#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from aiearth.core.error import AIEError, AIEErrorCode
from aiearth.core.client.client import BaseClient

from aiearth.engine import aie_env

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client(BaseClient):
    class ResponseCode(object):
        OK = 0
        ERROR = -1

    @staticmethod
    def __append_extra_body(data):
        options = {}
        if "options" in data:
            options = json.loads(data["options"])

        options["sessionId"] = aie_env.AIEEnv.getCurrentUserInteractiveSession()
        options["projectId"] = aie_env.AIEEnv.getCurrentUserProjectId()
        data["options"] = json.dumps(options)
        return data

    @staticmethod
    def post(url, data):
        headers = {"Content-Type": "application/json"}
        data = Client.__append_extra_body(data)
        resp = super(Client, Client).post(url, headers, data)
        response_data = resp.json()
        if "object" in response_data:
            value = json.loads(response_data["object"])
            if value["code"] != Client.ResponseCode.OK:
                extrainfo = {}
                if "requestId" in value:
                    extrainfo["requestId"] = value["requestId"]
                raise AIEError(
                    value["code"], value["message"], json.dumps(extrainfo))
            return value
        else:
            raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                           "", json.dumps(response_data))

    @staticmethod
    def get(url):
        headers = {"Content-Type": "application/json"}
        resp = super(Client, Client).get(url, headers)
        response_data = resp.json()
        if "object" in response_data:
            value = json.loads(response_data["object"])
            if value["code"] != Client.ResponseCode.OK:
                extrainfo = {}
                if "requestId" in value:
                    extrainfo["requestId"] = value["requestId"]
                raise AIEError(
                    value["code"], value["message"], json.dumps(extrainfo))
            return value
        else:
            raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                           "", json.dumps(response_data))

    @staticmethod
    def delete(url):
        headers = {"Content-Type": "application/json"}
        resp = super(Client, Client).delete(url, headers)
        response_data = resp.json()
        if "object" in response_data:
            value = json.loads(response_data["object"])
            if value["code"] != Client.ResponseCode.OK:
                extrainfo = {}
                if "requestId" in value:
                    extrainfo["requestId"] = value["requestId"]
                raise AIEError(
                    value["code"], value["message"], json.dumps(extrainfo))
            return value
        else:
            raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                           "", json.dumps(response_data))
