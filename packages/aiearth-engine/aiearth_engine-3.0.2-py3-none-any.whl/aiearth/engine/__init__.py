#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "3.0.2"

import aiearth.core

from aiearth.engine.aie_env import AIEEnv
from aiearth.core import g_var
from aiearth.engine import serialize
from aiearth.core import auth
from aiearth.engine import client
from aiearth.core import error
from aiearth.engine.map.aie_map import Map


from aiearth.engine.aie_object.image import Image

from aiearth.engine.aie_object.collection import Collection

from aiearth.engine.aie_object.image_collection import ImageCollection

from aiearth.engine.aie_object.geometry import Geometry

from aiearth.engine.aie_object.feature import Feature

from aiearth.engine.aie_object.feature_collection import FeatureCollection

from aiearth.engine.aie_object.filter import Filter

from aiearth.engine.aie_object.reducer import Reducer

from aiearth.engine.aie_object.terrain import Terrain

from aiearth.engine.aie_object.kernel import Kernel

from aiearth.engine.aie_object.classifier import Classifier

from aiearth.engine.aie_object.confusion_matrix import ConfusionMatrix

from aiearth.engine.aie_object.model import Model


Authenticate = aiearth.core.Authenticate


def Initialize(debug_level=g_var.LogLevel.INFO_LEVEL, debug=False):
    if debug:
        debug_level = g_var.LogLevel.DEBUG_LEVEL
    AIEEnv.init(debug_level)


def se(obj):
    return serialize.serializer.encode(obj)
