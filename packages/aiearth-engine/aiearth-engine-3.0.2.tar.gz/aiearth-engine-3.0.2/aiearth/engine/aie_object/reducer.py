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


class Reducer(FunctionNode):
    def combine(
        self,
        reducer2: engine.Reducer,
        outputPrefix: str = "",
        sharedInputs: bool = False,
    ) -> engine.Reducer:
        if reducer2 is not None and not isinstance(reducer2, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer2 只支持engine.Reducer类型参数, 传入类型为{type(reducer2)}",
            )

        if outputPrefix is not None and not isinstance(outputPrefix, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"outputPrefix 只支持str类型参数, 传入类型为{type(outputPrefix)}",
            )

        if sharedInputs is not None and not isinstance(sharedInputs, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"sharedInputs 只支持bool类型参数, 传入类型为{type(sharedInputs)}",
            )

        invoke_args = {
            "reducer1": self,
            "reducer2": reducer2,
            "outputPrefix": outputPrefix,
            "sharedInputs": sharedInputs,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "reducer2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer2不能为空")

        return FunctionHelper.apply("Reducer.combine", "engine.Reducer", invoke_args)

    @staticmethod
    def histogram(
        maxBuckets: int = None, minBucketWidth: [int, float] = None, maxRaw: int = None
    ) -> engine.Reducer:
        if maxBuckets is not None and not isinstance(maxBuckets, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"maxBuckets 只支持int类型参数, 传入类型为{type(maxBuckets)}",
            )

        if minBucketWidth is not None and not isinstance(minBucketWidth, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"minBucketWidth 只支持(int,float)类型参数, 传入类型为{type(minBucketWidth)}",
            )

        if maxRaw is not None and not isinstance(maxRaw, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"maxRaw 只支持int类型参数, 传入类型为{type(maxRaw)}"
            )

        invoke_args = {
            "maxBuckets": maxBuckets,
            "minBucketWidth": minBucketWidth,
            "maxRaw": maxRaw,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.histogram", "engine.Reducer", invoke_args)

    @staticmethod
    def count() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.count", "engine.Reducer", invoke_args)

    @staticmethod
    def max(numInputs: int = 1) -> engine.Reducer:
        if numInputs is not None and not isinstance(numInputs, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"numInputs 只支持int类型参数, 传入类型为{type(numInputs)}"
            )

        invoke_args = {
            "numInputs": numInputs,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.max", "engine.Reducer", invoke_args)

    @staticmethod
    def mean() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.mean", "engine.Reducer", invoke_args)

    @staticmethod
    def median(
        maxBuckets: int = None, minBucketWidth: [int, float] = None, maxRaw: int = None
    ) -> engine.Reducer:
        if maxBuckets is not None and not isinstance(maxBuckets, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"maxBuckets 只支持int类型参数, 传入类型为{type(maxBuckets)}",
            )

        if minBucketWidth is not None and not isinstance(minBucketWidth, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"minBucketWidth 只支持(int,float)类型参数, 传入类型为{type(minBucketWidth)}",
            )

        if maxRaw is not None and not isinstance(maxRaw, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"maxRaw 只支持int类型参数, 传入类型为{type(maxRaw)}"
            )

        invoke_args = {
            "maxBuckets": maxBuckets,
            "minBucketWidth": minBucketWidth,
            "maxRaw": maxRaw,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.median", "engine.Reducer", invoke_args)

    @staticmethod
    def min(numInputs: int = 1) -> engine.Reducer:
        if numInputs is not None and not isinstance(numInputs, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"numInputs 只支持int类型参数, 传入类型为{type(numInputs)}"
            )

        invoke_args = {
            "numInputs": numInputs,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.min", "engine.Reducer", invoke_args)

    @staticmethod
    def minMax() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.minMax", "engine.Reducer", invoke_args)

    @staticmethod
    def mode(
        maxBuckets: int = None, minBucketWidth: [int, float] = None, maxRaw: int = None
    ) -> engine.Reducer:
        if maxBuckets is not None and not isinstance(maxBuckets, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"maxBuckets 只支持int类型参数, 传入类型为{type(maxBuckets)}",
            )

        if minBucketWidth is not None and not isinstance(minBucketWidth, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"minBucketWidth 只支持(int,float)类型参数, 传入类型为{type(minBucketWidth)}",
            )

        if maxRaw is not None and not isinstance(maxRaw, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"maxRaw 只支持int类型参数, 传入类型为{type(maxRaw)}"
            )

        invoke_args = {
            "maxBuckets": maxBuckets,
            "minBucketWidth": minBucketWidth,
            "maxRaw": maxRaw,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.mode", "engine.Reducer", invoke_args)

    @staticmethod
    def product() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.product", "engine.Reducer", invoke_args)

    @staticmethod
    def stdDev() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.stdDev", "engine.Reducer", invoke_args)

    @staticmethod
    def sum() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.sum", "engine.Reducer", invoke_args)

    @staticmethod
    def variance() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.variance", "engine.Reducer", invoke_args)

    @staticmethod
    def allNonZero() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.allNonZero", "engine.Reducer", invoke_args)

    @staticmethod
    def anyNonZero() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.anyNonZero", "engine.Reducer", invoke_args)

    @staticmethod
    def bitwiseAnd() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.bitwiseAnd", "engine.Reducer", invoke_args)

    @staticmethod
    def bitwiseOr() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.bitwiseOr", "engine.Reducer", invoke_args)

    @staticmethod
    def sampleStdDev() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.sampleStdDev", "engine.Reducer", invoke_args
        )

    @staticmethod
    def sampleVariance() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.sampleVariance", "engine.Reducer", invoke_args
        )

    @staticmethod
    def histogram(buckets: int) -> engine.Reducer:
        if buckets is not None and not isinstance(buckets, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"buckets 只支持int类型参数, 传入类型为{type(buckets)}"
            )

        invoke_args = {
            "buckets": buckets,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "buckets" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数buckets不能为空")

        return FunctionHelper.apply("Reducer.histogram", "engine.Reducer", invoke_args)

    @staticmethod
    def fixedHistogram(
        min: [int, float], max: [int, float], buckets: int
    ) -> engine.Reducer:
        if min is not None and not isinstance(min, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"min 只支持(int,float)类型参数, 传入类型为{type(min)}"
            )

        if max is not None and not isinstance(max, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"max 只支持(int,float)类型参数, 传入类型为{type(max)}"
            )

        if buckets is not None and not isinstance(buckets, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"buckets 只支持int类型参数, 传入类型为{type(buckets)}"
            )

        invoke_args = {
            "min": min,
            "max": max,
            "buckets": buckets,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "min" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数min不能为空")

        if "max" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数max不能为空")

        if "buckets" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数buckets不能为空")

        return FunctionHelper.apply(
            "Reducer.fixedHistogram", "engine.Reducer", invoke_args
        )

    @staticmethod
    def linearFit() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Reducer.linearFit", "engine.Reducer", invoke_args)

    @staticmethod
    def linearRegression() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.linearRegression", "engine.Reducer", invoke_args
        )

    @staticmethod
    def pearsonsCorrelation() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.pearsonsCorrelation", "engine.Reducer", invoke_args
        )

    @staticmethod
    def spearmansCorrelation() -> engine.Reducer:
        invoke_args = {}

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.spearmansCorrelation", "engine.Reducer", invoke_args
        )

    @staticmethod
    def ridgeRegression(regParam: [int, float] = 0.1) -> engine.Reducer:
        if regParam is not None and not isinstance(regParam, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"regParam 只支持(int,float)类型参数, 传入类型为{type(regParam)}",
            )

        invoke_args = {
            "regParam": regParam,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.ridgeRegression", "engine.Reducer", invoke_args
        )

    @staticmethod
    def lassoRegression(regParam: [int, float] = 0.1) -> engine.Reducer:
        if regParam is not None and not isinstance(regParam, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"regParam 只支持(int,float)类型参数, 传入类型为{type(regParam)}",
            )

        invoke_args = {
            "regParam": regParam,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Reducer.lassoRegression", "engine.Reducer", invoke_args
        )
