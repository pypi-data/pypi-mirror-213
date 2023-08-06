#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .function_node import FunctionNode
from . import aie_object
from aiearth.core.error import AIEError, AIEErrorCode
from aiearth import engine


class FunctionHelper(object):
    @classmethod
    def cast(cls, node, kclass):
        if kclass == "engine.Image":
            node.__class__ = engine.Image
        elif kclass == "engine.Collection":
            node.__class__ = engine.Collection
        elif kclass == "engine.ImageCollection":
            node.__class__ = engine.ImageCollection
        elif kclass == "engine.Geometry":
            node.__class__ = engine.Geometry
        elif kclass == "engine.Feature":
            node.__class__ = engine.Feature
        elif kclass == "engine.FeatureCollection":
            node.__class__ = engine.FeatureCollection
        elif kclass == "engine.Filter":
            node.__class__ = engine.Filter
        elif kclass == "engine.Reducer":
            node.__class__ = engine.Reducer
        elif kclass == "engine.Terrain":
            node.__class__ = engine.Terrain
        elif kclass == "engine.Kernel":
            node.__class__ = engine.Kernel
        elif kclass == "engine.Classifier":
            node.__class__ = engine.Classifier
        elif kclass == "engine.ConfusionMatrix":
            node.__class__ = engine.ConfusionMatrix
        elif kclass in ("int", "float", "bool", "str", "list", "tuple", "dict", "object"):
            pass
        else:
            raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR,
                           "", "FunctionHelper::cast kclass " + kclass + " not support")
        return node

    @classmethod
    def apply(cls, name, returns, args):
        node = FunctionNode(name, args)
        return cls.cast(node, returns)
