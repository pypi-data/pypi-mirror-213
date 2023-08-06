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


class Filter(FunctionNode):
    @staticmethod
    def date(start: str, end: str = None) -> engine.Filter:
        if start is not None and not isinstance(start, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"start 只支持str类型参数, 传入类型为{type(start)}"
            )

        if end is not None and not isinstance(end, str):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"end 只支持str类型参数, 传入类型为{type(end)}")

        invoke_args = {
            "start": start,
            "end": end,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "start" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数start不能为空")

        return FunctionHelper.apply("Filter.date", "engine.Filter", invoke_args)

    @staticmethod
    def bounds(
        geometry: Union[engine.Geometry, engine.Feature, engine.FeatureCollection]
    ) -> engine.Filter:
        if geometry is not None and not isinstance(
            geometry, (engine.Geometry, engine.Feature, engine.FeatureCollection)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometry 只支持(engine.Geometry,engine.Feature,engine.FeatureCollection)类型参数, 传入类型为{type(geometry)}",
            )

        invoke_args = {
            "geometry": geometry,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "geometry" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数geometry不能为空")

        return FunctionHelper.apply("Filter.bounds", "engine.Filter", invoke_args)

    @staticmethod
    def eq(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.eq", "engine.Filter", invoke_args)

    @staticmethod
    def gt(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.gt", "engine.Filter", invoke_args)

    @staticmethod
    def gte(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.gte", "engine.Filter", invoke_args)

    @staticmethod
    def lt(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.lt", "engine.Filter", invoke_args)

    @staticmethod
    def lte(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.lte", "engine.Filter", invoke_args)

    @staticmethod
    def neq(name: str, value: object) -> engine.Filter:
        if name is not None and not isinstance(name, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"name 只支持str类型参数, 传入类型为{type(name)}"
            )

        if value is not None and not isinstance(value, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"value 只支持object类型参数, 传入类型为{type(value)}"
            )

        invoke_args = {
            "name": name,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "name" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数name不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Filter.neq", "engine.Filter", invoke_args)

    @staticmethod
    def And(filters: list) -> engine.Filter:
        if filters is not None and not isinstance(filters, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"filters 只支持list类型参数, 传入类型为{type(filters)}"
            )

        invoke_args = {
            "filters": filters,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "filters" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数filters不能为空")

        return FunctionHelper.apply("Filter.and", "engine.Filter", invoke_args)

    @staticmethod
    def Or(filters: list) -> engine.Filter:
        if filters is not None and not isinstance(filters, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"filters 只支持list类型参数, 传入类型为{type(filters)}"
            )

        invoke_args = {
            "filters": filters,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "filters" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数filters不能为空")

        return FunctionHelper.apply("Filter.or", "engine.Filter", invoke_args)

    @staticmethod
    def Not() -> engine.Filter:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Filter.not", "engine.Filter", invoke_args)

    @staticmethod
    def calendarRange(
        start: int, end: int = None, field: str = "day_of_year"
    ) -> engine.Filter:
        if start is not None and not isinstance(start, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"start 只支持int类型参数, 传入类型为{type(start)}"
            )

        if end is not None and not isinstance(end, int):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"end 只支持int类型参数, 传入类型为{type(end)}")

        if field is not None and not isinstance(field, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"field 只支持str类型参数, 传入类型为{type(field)}"
            )

        invoke_args = {
            "start": start,
            "end": end,
            "field": field,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "start" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数start不能为空")

        return FunctionHelper.apply(
            "Filter.calendarRange", "engine.Filter", invoke_args
        )

    @staticmethod
    def dateRangeContains(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Filter.dateRangeContains", "engine.Filter", invoke_args
        )

    @staticmethod
    def dayOfYear(start: int, end: int) -> engine.Filter:
        if start is not None and not isinstance(start, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"start 只支持int类型参数, 传入类型为{type(start)}"
            )

        if end is not None and not isinstance(end, int):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"end 只支持int类型参数, 传入类型为{type(end)}")

        invoke_args = {
            "start": start,
            "end": end,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "start" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数start不能为空")

        if "end" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数end不能为空")

        return FunctionHelper.apply("Filter.dayOfYear", "engine.Filter", invoke_args)

    @staticmethod
    def equals(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Filter.equals", "engine.Filter", invoke_args)

    @staticmethod
    def greaterThan(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Filter.greaterThan", "engine.Filter", invoke_args)

    @staticmethod
    def greaterThanOrEquals(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Filter.greaterThanOrEquals", "engine.Filter", invoke_args
        )

    @staticmethod
    def lessThan(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Filter.lessThan", "engine.Filter", invoke_args)

    @staticmethod
    def lessThanOrEquals(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Filter.lessThanOrEquals", "engine.Filter", invoke_args
        )

    @staticmethod
    def notEquals(
        leftField: str = None,
        rightValue: object = None,
        rightField: str = None,
        leftValue: object = None,
    ) -> engine.Filter:
        if leftField is not None and not isinstance(leftField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"leftField 只支持str类型参数, 传入类型为{type(leftField)}"
            )

        if rightValue is not None and not isinstance(rightValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightValue 只支持object类型参数, 传入类型为{type(rightValue)}",
            )

        if rightField is not None and not isinstance(rightField, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"rightField 只支持str类型参数, 传入类型为{type(rightField)}",
            )

        if leftValue is not None and not isinstance(leftValue, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"leftValue 只支持object类型参数, 传入类型为{type(leftValue)}",
            )

        invoke_args = {
            "leftField": leftField,
            "rightValue": rightValue,
            "rightField": rightField,
            "leftValue": leftValue,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Filter.notEquals", "engine.Filter", invoke_args)

    @staticmethod
    def notNull(properties: list) -> engine.Filter:
        if properties is not None and not isinstance(properties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"properties 只支持list类型参数, 传入类型为{type(properties)}",
            )

        invoke_args = {
            "properties": properties,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "properties" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数properties不能为空")

        return FunctionHelper.apply("Filter.notNull", "engine.Filter", invoke_args)
