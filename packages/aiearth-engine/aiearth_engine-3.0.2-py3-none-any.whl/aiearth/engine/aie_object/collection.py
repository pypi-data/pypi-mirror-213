#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import abc
import inspect
from typing import Union

from aiearth import engine
from aiearth.engine.variable_node import VariableNode
from aiearth.engine.function_node import FunctionNode
from aiearth.engine.customfunction_node import CustomFunctionNode
from aiearth.engine.function_helper import FunctionHelper
from aiearth.core.error.aie_error import AIEError, AIEErrorCode


class Collection(FunctionNode):
    @abc.abstractmethod
    def elementType(self):
        pass

    def filter(self, filter: Union[str, engine.Filter]) -> engine.Collection:
        if filter is not None and not isinstance(filter, (str, engine.Filter)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"filter 只支持(str,engine.Filter)类型参数, 传入类型为{type(filter)}",
            )

        invoke_args = {
            "collection": self,
            "filter": filter,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "filter" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数filter不能为空")

        return FunctionHelper.apply(
            "Collection.filter", "engine.Collection", invoke_args
        )

    def filterBounds(
        self, geometry: Union[engine.Geometry, engine.Feature, engine.FeatureCollection]
    ) -> engine.Collection:
        if geometry is not None and not isinstance(
            geometry, (engine.Geometry, engine.Feature, engine.FeatureCollection)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometry 只支持(engine.Geometry,engine.Feature,engine.FeatureCollection)类型参数, 传入类型为{type(geometry)}",
            )

        invoke_args = {
            "collection": self,
            "geometry": geometry,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "geometry" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数geometry不能为空")

        return FunctionHelper.apply(
            "Collection.filterBounds", "engine.Collection", invoke_args
        )

    def first(self) -> object:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Collection.first", "object", invoke_args)

    def limit(
        self, limit: int, property: str = None, ascending: bool = True
    ) -> engine.Collection:
        if limit is not None and not isinstance(limit, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"limit 只支持int类型参数, 传入类型为{type(limit)}"
            )

        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        if ascending is not None and not isinstance(ascending, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"ascending 只支持bool类型参数, 传入类型为{type(ascending)}",
            )

        invoke_args = {
            "collection": self,
            "limit": limit,
            "property": property,
            "ascending": ascending,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "limit" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数limit不能为空")

        return FunctionHelper.apply(
            "Collection.limit", "engine.Collection", invoke_args
        )

    def size(self) -> object:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Collection.size", "object", invoke_args)

    def map(self, baseAlgorithm) -> engine.Collection:
        import types

        if baseAlgorithm is not None and not isinstance(
            baseAlgorithm, types.FunctionType
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"baseAlgorithm 只支持function类型参数, 传入类型为{type(baseAlgorithm)}",
            )

        args = inspect.getfullargspec(baseAlgorithm).args
        mapping_args = [
            "_MAPPING_VAR_#arg" + str(k) + "_" + v for k, v in enumerate(args)
        ]
        variables = [VariableNode(mapping_arg) for mapping_arg in mapping_args]

        element_type = self.elementType()

        def func_warp(e):
            return baseAlgorithm(element_type(e))

        body = func_warp(*variables)
        if body is None:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "自定义map函数必须有返回值")
        customfunc = CustomFunctionNode(mapping_args, body)

        invoke_args = {
            "collection": self,
            "baseAlgorithm": customfunc,
        }
        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "baseAlgorithm" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数baseAlgorithm不能为空")

        return FunctionHelper.apply("Collection.map", "engine.Collection", invoke_args)
