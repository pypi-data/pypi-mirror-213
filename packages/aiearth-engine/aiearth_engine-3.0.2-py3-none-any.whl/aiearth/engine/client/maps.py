#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from aiearth.core.client.endpoints import newUUID, Endpoints, SdkGatewayResource
from .client import Client
from aiearth import engine
from aiearth.core.error.aie_error import *
from aiearth.engine.serialize import serializer


class Maps(object):
    class AddLayerType:
        Image = "Image"
        Feature = "Feature"

    @staticmethod
    def getMapId(obj, vis_params=None):
        request_id = newUUID()

        add_layer_type = None
        if isinstance(obj, engine.Image):
            add_layer_type = Maps.AddLayerType.Image
        elif isinstance(obj, engine.ImageCollection):
            obj = obj.mosaic()
            add_layer_type = Maps.AddLayerType.Image
        elif isinstance(obj, engine.Geometry):
            add_layer_type = Maps.AddLayerType.Feature
        elif isinstance(obj, engine.Feature):
            add_layer_type = Maps.AddLayerType.Feature
        elif isinstance(obj, engine.FeatureCollection):
            add_layer_type = Maps.AddLayerType.Feature

        expr = serializer.encode(obj)

        options = {
            "mapId": newUUID(),
            "taskType": "addLayer",
            "addLayerType": add_layer_type,
            "visParams": vis_params
        }

        options_serialize = ""
        try: 
            options_serialize = json.dumps(options, ensure_ascii=False, allow_nan=False)
        except Exception as e:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "请检查visParams参数", str(e))
        data = {"requestId": request_id,
                "expr": expr,
                "options": options_serialize}

        url = Endpoints.SDK_GATEWAY + SdkGatewayResource.Maps.GET_MAP_ID
        return Client.post(url, data)
