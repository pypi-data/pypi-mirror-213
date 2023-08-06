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


class Image(FunctionNode):
    def __init__(self, args=None) -> engine.Image:
        if isinstance(args, (int, float, complex)):
            invoke_args = {"value": args}
            super(Image, self).__init__("Image.constant", invoke_args)
        elif isinstance(args, str):
            invoke_args = {"id": args}
            super(Image, self).__init__("Image.load", invoke_args)
        elif isinstance(args, (list, tuple)):
            images = [Image(i) for i in args]
            result = images[0]
            for image in images[1:]:
                invoke_args = {"srcImg": image, "dstImg": result}
                result = FunctionHelper.apply(
                    "Image.addBands", "engine.Image", invoke_args
                )
            super(Image, self).__init__(
                result.func_name, result.invoke_args, result.var_name
            )
        elif args is None:
            image = Image(0)
            invoke_args = {"input": image, "mask": image}
            super(Image, self).__init__("Image.mask", invoke_args)
        elif isinstance(args, engine.variable_node.VariableNode):
            super(Image, self).__init__(args.func_name, args.invoke_args, args.var_name)
        elif isinstance(args, engine.function_node.FunctionNode):
            super(Image, self).__init__(args.func_name, args.invoke_args, args.var_name)
        else:
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"args 只支持number|str|list类型参数, 传入类型为{type(args)}",
            )

    def select(self, bandSelectors: Union[str, list]) -> engine.Image:
        if bandSelectors is not None and not isinstance(bandSelectors, (str, list)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"bandSelectors 只支持(str,list)类型参数, 传入类型为{type(bandSelectors)}",
            )

        if isinstance(bandSelectors, str):
            bandSelectors = [bandSelectors]

        invoke_args = {
            "input": self,
            "bandSelectors": bandSelectors,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "bandSelectors" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数bandSelectors不能为空")

        return FunctionHelper.apply("Image.select", "engine.Image", invoke_args)

    def rename(self, names: list) -> engine.Image:
        if names is not None and not isinstance(names, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"names 只支持list类型参数, 传入类型为{type(names)}"
            )

        invoke_args = {
            "input": self,
            "names": names,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "names" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数names不能为空")

        return FunctionHelper.apply("Image.rename", "engine.Image", invoke_args)

    def normalizedDifference(self, bandNames: list) -> engine.Image:
        if bandNames is not None and not isinstance(bandNames, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"bandNames 只支持list类型参数, 传入类型为{type(bandNames)}",
            )

        invoke_args = {
            "input": self,
            "bandNames": bandNames,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "bandNames" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数bandNames不能为空")

        return FunctionHelper.apply(
            "Image.normalizedDifference", "engine.Image", invoke_args
        )

    def expression(self, expression: str, map: dict = None) -> engine.Image:
        if expression is not None and not isinstance(expression, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"expression 只支持str类型参数, 传入类型为{type(expression)}",
            )

        if map is not None and not isinstance(map, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"map 只支持dict类型参数, 传入类型为{type(map)}"
            )

        invoke_args = {
            "input": self,
            "expression": expression,
            "map": map,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "expression" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数expression不能为空")

        return FunctionHelper.apply("Image.expression", "engine.Image", invoke_args)

    def getMapId(self, vis_params):
        if vis_params is not None and not isinstance(vis_params, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"vis_params 只支持dict类型参数, 传入类型为{type(vis_params)}",
            )
        return engine.client.Maps.getMapId(self, vis_params)

    def getCenter(self) -> tuple:
        bbox = engine.client.InteractiveSession.getBounds(self)
        if bbox is not None and isinstance(bbox, list):
            center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            return center
        raise AIEError(AIEErrorCode.ARGS_ERROR, f"获取Center失败. bbox: {bbox}")

    def getBounds(self) -> list:
        bbox = engine.client.InteractiveSession.getBounds(self)
        if bbox is not None and isinstance(bbox, list):
            bounds = [bbox[0], bbox[1], bbox[2], bbox[3]]
            return bounds
        raise AIEError(AIEErrorCode.ARGS_ERROR, f"获取Bounds失败. bbox: {bbox}")

    def where(self, test: engine.Image, value: engine.Image) -> engine.Image:
        if test is not None and not isinstance(test, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"test 只支持engine.Image类型参数, 传入类型为{type(test)}"
            )

        if value is not None and not isinstance(value, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"value 只支持engine.Image类型参数, 传入类型为{type(value)}",
            )

        invoke_args = {
            "input": self,
            "test": test,
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "test" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数test不能为空")

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Image.where", "engine.Image", invoke_args)

    def abs(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.abs", "engine.Image", invoke_args)

    def acos(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.acos", "engine.Image", invoke_args)

    def add(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.add", "engine.Image", invoke_args)

    def asin(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.asin", "engine.Image", invoke_args)

    def atan(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.atan", "engine.Image", invoke_args)

    def ceil(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.ceil", "engine.Image", invoke_args)

    def clamp(self, low: [int, float], high: [int, float]) -> engine.Image:
        if low is not None and not isinstance(low, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"low 只支持(int,float)类型参数, 传入类型为{type(low)}"
            )

        if high is not None and not isinstance(high, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"high 只支持(int,float)类型参数, 传入类型为{type(high)}"
            )

        invoke_args = {
            "input": self,
            "low": low,
            "high": high,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "low" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数low不能为空")

        if "high" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数high不能为空")

        return FunctionHelper.apply("Image.clamp", "engine.Image", invoke_args)

    def cos(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.cos", "engine.Image", invoke_args)

    def divide(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.divide", "engine.Image", invoke_args)

    def exp(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.exp", "engine.Image", invoke_args)

    def floor(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.floor", "engine.Image", invoke_args)

    def log(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.log", "engine.Image", invoke_args)

    def log10(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.log10", "engine.Image", invoke_args)

    def max(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.max", "engine.Image", invoke_args)

    def min(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.min", "engine.Image", invoke_args)

    def mod(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.mod", "engine.Image", invoke_args)

    def multiply(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.multiply", "engine.Image", invoke_args)

    def pow(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.pow", "engine.Image", invoke_args)

    def round(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.round", "engine.Image", invoke_args)

    def signum(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.signum", "engine.Image", invoke_args)

    def sin(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.sin", "engine.Image", invoke_args)

    def sqrt(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.sqrt", "engine.Image", invoke_args)

    def subtract(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.subtract", "engine.Image", invoke_args)

    def tan(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.tan", "engine.Image", invoke_args)

    def eq(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.eq", "engine.Image", invoke_args)

    def gt(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.gt", "engine.Image", invoke_args)

    def gte(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.gte", "engine.Image", invoke_args)

    def lt(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.lt", "engine.Image", invoke_args)

    def lte(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.lte", "engine.Image", invoke_args)

    def neq(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.neq", "engine.Image", invoke_args)

    def And(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.and", "engine.Image", invoke_args)

    def Not(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.not", "engine.Image", invoke_args)

    def Or(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.or", "engine.Image", invoke_args)

    def bitwiseAnd(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.bitwiseAnd", "engine.Image", invoke_args)

    def bitwiseNot(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.bitwiseNot", "engine.Image", invoke_args)

    def bitwiseOr(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.bitwiseOr", "engine.Image", invoke_args)

    def bitwiseXor(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.bitwiseXor", "engine.Image", invoke_args)

    def leftShift(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.leftShift", "engine.Image", invoke_args)

    def rightShift(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.rightShift", "engine.Image", invoke_args)

    def mask(self, mask: engine.Image = None) -> engine.Image:
        if mask is not None and not isinstance(mask, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"mask 只支持engine.Image类型参数, 传入类型为{type(mask)}"
            )

        invoke_args = {
            "input": self,
            "mask": mask,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.mask", "engine.Image", invoke_args)

    def unmask(
        self, value: engine.Image = None, sameFootprint: bool = True
    ) -> engine.Image:
        if value is not None and not isinstance(value, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"value 只支持engine.Image类型参数, 传入类型为{type(value)}",
            )

        if sameFootprint is not None and not isinstance(sameFootprint, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"sameFootprint 只支持bool类型参数, 传入类型为{type(sameFootprint)}",
            )

        invoke_args = {
            "input": self,
            "value": value,
            "sameFootprint": sameFootprint,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.unmask", "engine.Image", invoke_args)

    def updateMask(self, mask: engine.Image) -> engine.Image:
        if mask is not None and not isinstance(mask, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"mask 只支持engine.Image类型参数, 传入类型为{type(mask)}"
            )

        invoke_args = {
            "image": self,
            "mask": mask,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "mask" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数mask不能为空")

        return FunctionHelper.apply("Image.updateMask", "engine.Image", invoke_args)

    def focalMax(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalMax", "engine.Image", invoke_args)

    def focalMean(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalMean", "engine.Image", invoke_args)

    def focalMedian(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalMedian", "engine.Image", invoke_args)

    def focalMin(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalMin", "engine.Image", invoke_args)

    def focalMode(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalMode", "engine.Image", invoke_args)

    def focalSum(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalSum", "engine.Image", invoke_args)

    def focalStandardDeviation(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Image.focalStandardDeviation", "engine.Image", invoke_args
        )

    def focalConway(
        self,
        radius: [int, float] = 1.0,
        kernelType: str = "square",
        units: str = "pixels",
        iterations: int = 1,
    ) -> engine.Image:
        if radius is not None and not isinstance(radius, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"radius 只支持(int,float)类型参数, 传入类型为{type(radius)}",
            )

        if kernelType is not None and not isinstance(kernelType, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernelType 只支持str类型参数, 传入类型为{type(kernelType)}",
            )

        if units is not None and not isinstance(units, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"units 只支持str类型参数, 传入类型为{type(units)}"
            )

        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        invoke_args = {
            "input": self,
            "radius": radius,
            "kernelType": kernelType,
            "units": units,
            "iterations": iterations,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.focalConway", "engine.Image", invoke_args)

    def reduce(self, reducer: engine.Reducer) -> engine.Image:
        if reducer is not None and not isinstance(reducer, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer 只支持engine.Reducer类型参数, 传入类型为{type(reducer)}",
            )

        invoke_args = {
            "image": self,
            "reducer": reducer,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "reducer" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer不能为空")

        return FunctionHelper.apply("Image.reduce", "engine.Image", invoke_args)

    def reduceRegion(
        self,
        reducer: engine.Reducer,
        geometry: engine.Geometry = None,
        scale: [int, float] = None,
    ) -> object:
        if reducer is not None and not isinstance(reducer, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer 只支持engine.Reducer类型参数, 传入类型为{type(reducer)}",
            )

        if geometry is not None and not isinstance(geometry, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometry 只支持engine.Geometry类型参数, 传入类型为{type(geometry)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        invoke_args = {
            "image": self,
            "reducer": reducer,
            "geometry": geometry,
            "scale": scale,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "reducer" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer不能为空")

        return FunctionHelper.apply("Image.reduceRegion", "object", invoke_args)

    def reduceRegions(
        self,
        collection: engine.FeatureCollection,
        reducer: engine.Reducer,
        scale: [int, float] = None,
    ) -> engine.FeatureCollection:
        if collection is not None and not isinstance(
            collection, engine.FeatureCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection 只支持engine.FeatureCollection类型参数, 传入类型为{type(collection)}",
            )

        if reducer is not None and not isinstance(reducer, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer 只支持engine.Reducer类型参数, 传入类型为{type(reducer)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        invoke_args = {
            "image": self,
            "collection": collection,
            "reducer": reducer,
            "scale": scale,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection不能为空")

        if "reducer" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer不能为空")

        return FunctionHelper.apply(
            "Image.reduceRegions", "engine.FeatureCollection", invoke_args
        )

    def clip(self, geometry: Union[engine.Geometry, engine.Feature]) -> engine.Image:
        if geometry is not None and not isinstance(
            geometry, (engine.Geometry, engine.Feature)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometry 只支持(engine.Geometry,engine.Feature)类型参数, 传入类型为{type(geometry)}",
            )

        invoke_args = {
            "image": self,
            "geometry": geometry,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "geometry" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数geometry不能为空")

        return FunctionHelper.apply("Image.clip", "engine.Image", invoke_args)

    def addBands(
        self, srcImg: engine.Image, names: list = None, overwrite: bool = False
    ) -> engine.Image:
        if srcImg is not None and not isinstance(srcImg, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"srcImg 只支持engine.Image类型参数, 传入类型为{type(srcImg)}",
            )

        if names is not None and not isinstance(names, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"names 只支持list类型参数, 传入类型为{type(names)}"
            )

        if overwrite is not None and not isinstance(overwrite, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"overwrite 只支持bool类型参数, 传入类型为{type(overwrite)}",
            )

        invoke_args = {
            "dstImg": self,
            "srcImg": srcImg,
            "names": names,
            "overwrite": overwrite,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "srcImg" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数srcImg不能为空")

        return FunctionHelper.apply("Image.addBands", "engine.Image", invoke_args)

    @staticmethod
    def constant(value: Union[int, float, list]) -> engine.Image:
        if value is not None and not isinstance(value, (int, float, list)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"value 只支持(int,float,list)类型参数, 传入类型为{type(value)}",
            )

        invoke_args = {
            "value": value,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "value" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数value不能为空")

        return FunctionHelper.apply("Image.constant", "engine.Image", invoke_args)

    def bandNames(self) -> object:
        invoke_args = {
            "image": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.bandNames", "object", invoke_args)

    def bandTypes(self) -> object:
        invoke_args = {
            "image": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.bandTypes", "object", invoke_args)

    def date(self) -> object:
        invoke_args = {
            "image": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.date", "object", invoke_args)

    def get(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "input": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply("Image.get", "object", invoke_args)

    @staticmethod
    def rgb(r: engine.Image, g: engine.Image, b: engine.Image) -> engine.Image:
        if r is not None and not isinstance(r, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"r 只支持engine.Image类型参数, 传入类型为{type(r)}"
            )

        if g is not None and not isinstance(g, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"g 只支持engine.Image类型参数, 传入类型为{type(g)}"
            )

        if b is not None and not isinstance(b, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"b 只支持engine.Image类型参数, 传入类型为{type(b)}"
            )

        invoke_args = {
            "r": r,
            "g": g,
            "b": b,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "r" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数r不能为空")

        if "g" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数g不能为空")

        if "b" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数b不能为空")

        return FunctionHelper.apply("Image.rgb", "engine.Image", invoke_args)

    def rgbToHsv(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.rgbToHsv", "engine.Image", invoke_args)

    def hsvToRgb(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.hsvToRgb", "engine.Image", invoke_args)

    def unitScale(self, low: [int, float], high: [int, float]) -> engine.Image:
        if low is not None and not isinstance(low, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"low 只支持(int,float)类型参数, 传入类型为{type(low)}"
            )

        if high is not None and not isinstance(high, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"high 只支持(int,float)类型参数, 传入类型为{type(high)}"
            )

        invoke_args = {
            "input": self,
            "low": low,
            "high": high,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "low" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数low不能为空")

        if "high" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数high不能为空")

        return FunctionHelper.apply("Image.unitScale", "engine.Image", invoke_args)

    def sinh(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.sinh", "engine.Image", invoke_args)

    def cosh(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.cosh", "engine.Image", invoke_args)

    def tanh(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.tanh", "engine.Image", invoke_args)

    def atan2(self, right: engine.Image) -> engine.Image:
        if right is not None and not isinstance(right, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Image类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Image.atan2", "engine.Image", invoke_args)

    def fastAtan2(self, right: engine.Image) -> engine.Image:
        if right is not None and not isinstance(right, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Image类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Image.fastAtan2", "engine.Image", invoke_args)

    def convolve(self, kernel: engine.Kernel) -> engine.Image:
        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        invoke_args = {
            "image": self,
            "kernel": kernel,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "kernel" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数kernel不能为空")

        return FunctionHelper.apply("Image.convolve", "engine.Image", invoke_args)

    def toByte(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toByte", "engine.Image", invoke_args)

    def toInt16(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toInt16", "engine.Image", invoke_args)

    def toUint16(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toUint16", "engine.Image", invoke_args)

    def toInt32(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toInt32", "engine.Image", invoke_args)

    def toUint32(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toUint32", "engine.Image", invoke_args)

    def toFloat(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toFloat", "engine.Image", invoke_args)

    def toDouble(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.toDouble", "engine.Image", invoke_args)

    def selfMask(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.selfMask", "engine.Image", invoke_args)

    def polynomial(self, coeffs: list) -> engine.Image:
        if coeffs is not None and not isinstance(coeffs, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"coeffs 只支持list类型参数, 传入类型为{type(coeffs)}"
            )

        invoke_args = {
            "input": self,
            "coeffs": coeffs,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coeffs" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coeffs不能为空")

        return FunctionHelper.apply("Image.polynomial", "engine.Image", invoke_args)

    def gamma(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.gamma", "engine.Image", invoke_args)

    def digamma(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.digamma", "engine.Image", invoke_args)

    def remap(
        self,
        fromValue: list,
        toValue: list,
        defaultValue: [int, float] = None,
        bandName: str = None,
    ) -> engine.Image:
        if fromValue is not None and not isinstance(fromValue, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"fromValue 只支持list类型参数, 传入类型为{type(fromValue)}",
            )

        if toValue is not None and not isinstance(toValue, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"toValue 只支持list类型参数, 传入类型为{type(toValue)}"
            )

        if defaultValue is not None and not isinstance(defaultValue, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"defaultValue 只支持(int,float)类型参数, 传入类型为{type(defaultValue)}",
            )

        if bandName is not None and not isinstance(bandName, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"bandName 只支持str类型参数, 传入类型为{type(bandName)}"
            )

        invoke_args = {
            "input": self,
            "fromValue": fromValue,
            "toValue": toValue,
            "defaultValue": defaultValue,
            "bandName": bandName,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "fromValue" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数fromValue不能为空")

        if "toValue" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数toValue不能为空")

        return FunctionHelper.apply("Image.remap", "engine.Image", invoke_args)

    def erf(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.erf", "engine.Image", invoke_args)

    def erfc(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.erfc", "engine.Image", invoke_args)

    def erfInv(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.erfInv", "engine.Image", invoke_args)

    def erfcInv(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.erfcInv", "engine.Image", invoke_args)

    def pixelArea(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.pixelArea", "engine.Image", invoke_args)

    def derivative(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.derivative", "engine.Image", invoke_args)

    def entropy(self, kernel: engine.Kernel) -> engine.Image:
        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        invoke_args = {
            "input": self,
            "kernel": kernel,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "kernel" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数kernel不能为空")

        return FunctionHelper.apply("Image.entropy", "engine.Image", invoke_args)

    def distance(self, kernel: engine.Kernel, skipMasked: bool = True) -> engine.Image:
        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        if skipMasked is not None and not isinstance(skipMasked, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"skipMasked 只支持bool类型参数, 传入类型为{type(skipMasked)}",
            )

        invoke_args = {
            "input": self,
            "kernel": kernel,
            "skipMasked": skipMasked,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "kernel" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数kernel不能为空")

        return FunctionHelper.apply("Image.distance", "engine.Image", invoke_args)

    def spectralDilation(
        self,
        metric: str = "sam",
        kernel: engine.Kernel = None,
        useCentroid: bool = False,
    ) -> engine.Image:
        if metric is not None and not isinstance(metric, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"metric 只支持str类型参数, 传入类型为{type(metric)}"
            )

        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        if useCentroid is not None and not isinstance(useCentroid, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"useCentroid 只支持bool类型参数, 传入类型为{type(useCentroid)}",
            )

        invoke_args = {
            "image": self,
            "metric": metric,
            "kernel": kernel,
            "useCentroid": useCentroid,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Image.spectralDilation", "engine.Image", invoke_args
        )

    def spectralErosion(
        self,
        metric: str = "sam",
        kernel: engine.Kernel = None,
        useCentroid: bool = False,
    ) -> engine.Image:
        if metric is not None and not isinstance(metric, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"metric 只支持str类型参数, 传入类型为{type(metric)}"
            )

        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        if useCentroid is not None and not isinstance(useCentroid, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"useCentroid 只支持bool类型参数, 传入类型为{type(useCentroid)}",
            )

        invoke_args = {
            "image": self,
            "metric": metric,
            "kernel": kernel,
            "useCentroid": useCentroid,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Image.spectralErosion", "engine.Image", invoke_args
        )

    def spectralGradient(
        self,
        metric: str = "sam",
        kernel: engine.Kernel = None,
        useCentroid: bool = False,
    ) -> engine.Image:
        if metric is not None and not isinstance(metric, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"metric 只支持str类型参数, 传入类型为{type(metric)}"
            )

        if kernel is not None and not isinstance(kernel, engine.Kernel):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"kernel 只支持engine.Kernel类型参数, 传入类型为{type(kernel)}",
            )

        if useCentroid is not None and not isinstance(useCentroid, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"useCentroid 只支持bool类型参数, 传入类型为{type(useCentroid)}",
            )

        invoke_args = {
            "image": self,
            "metric": metric,
            "kernel": kernel,
            "useCentroid": useCentroid,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Image.spectralGradient", "engine.Image", invoke_args
        )

    def spectralDistance(
        self, image2: engine.Image, metric: str = "sam"
    ) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        if metric is not None and not isinstance(metric, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"metric 只支持str类型参数, 传入类型为{type(metric)}"
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
            "metric": metric,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply(
            "Image.spectralDistance", "engine.Image", invoke_args
        )

    def lanczos(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.lanczos", "engine.Image", invoke_args)

    def pixelCoordinates(self, projection: str) -> engine.Image:
        if projection is not None and not isinstance(projection, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"projection 只支持str类型参数, 传入类型为{type(projection)}",
            )

        invoke_args = {
            "value": self,
            "projection": projection,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "projection" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数projection不能为空")

        return FunctionHelper.apply(
            "Image.pixelCoordinates", "engine.Image", invoke_args
        )

    def pixelLonLat(self) -> engine.Image:
        invoke_args = {
            "value": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.pixelLonLat", "engine.Image", invoke_args)

    def unmix(self, endmembers: list) -> engine.Image:
        if endmembers is not None and not isinstance(endmembers, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"endmembers 只支持list类型参数, 传入类型为{type(endmembers)}",
            )

        invoke_args = {
            "image": self,
            "endmembers": endmembers,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "endmembers" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数endmembers不能为空")

        return FunctionHelper.apply("Image.unmix", "engine.Image", invoke_args)

    def clipToCollection(self, collection: engine.FeatureCollection) -> engine.Image:
        if collection is not None and not isinstance(
            collection, engine.FeatureCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection 只支持engine.FeatureCollection类型参数, 传入类型为{type(collection)}",
            )

        invoke_args = {
            "input": self,
            "collection": collection,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection不能为空")

        return FunctionHelper.apply(
            "Image.clipToCollection", "engine.Image", invoke_args
        )

    def propertyNames(self) -> object:
        invoke_args = {
            "element": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.propertyNames", "object", invoke_args)

    def copyProperties(self, image2: engine.Image) -> engine.Image:
        if image2 is not None and not isinstance(image2, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"image2 只支持engine.Image类型参数, 传入类型为{type(image2)}",
            )

        invoke_args = {
            "image1": self,
            "image2": image2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "image2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数image2不能为空")

        return FunctionHelper.apply("Image.copyProperties", "engine.Image", invoke_args)

    def classify(
        self, classifier: engine.Classifier, outputName: str = "classification"
    ) -> engine.Image:
        if classifier is not None and not isinstance(classifier, engine.Classifier):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"classifier 只支持engine.Classifier类型参数, 传入类型为{type(classifier)}",
            )

        if outputName is not None and not isinstance(outputName, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"outputName 只支持str类型参数, 传入类型为{type(outputName)}",
            )

        invoke_args = {
            "input": self,
            "classifier": classifier,
            "outputName": outputName,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "classifier" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数classifier不能为空")

        return FunctionHelper.apply("Image.classify", "engine.Image", invoke_args)

    def sample(
        self,
        region: engine.Geometry,
        scale: [int, float],
        numPixels: int,
        seed: int = 0,
        geometries: bool = False,
    ) -> engine.FeatureCollection:
        if region is not None and not isinstance(region, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"region 只支持engine.Geometry类型参数, 传入类型为{type(region)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        if numPixels is not None and not isinstance(numPixels, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"numPixels 只支持int类型参数, 传入类型为{type(numPixels)}"
            )

        if seed is not None and not isinstance(seed, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"seed 只支持int类型参数, 传入类型为{type(seed)}"
            )

        if geometries is not None and not isinstance(geometries, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometries 只支持bool类型参数, 传入类型为{type(geometries)}",
            )

        invoke_args = {
            "input": self,
            "region": region,
            "scale": scale,
            "numPixels": numPixels,
            "seed": seed,
            "geometries": geometries,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "region" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数region不能为空")

        if "scale" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数scale不能为空")

        if "numPixels" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数numPixels不能为空")

        return FunctionHelper.apply(
            "Image.sample", "engine.FeatureCollection", invoke_args
        )

    def mask(self) -> engine.Image:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.mask", "engine.Image", invoke_args)

    def id(self) -> object:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.id", "object", invoke_args)

    def getNumber(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "input": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply("Image.getNumber", "object", invoke_args)

    def getString(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "input": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply("Image.getString", "object", invoke_args)

    def random(self, seed: int = 0, distribution: str = "uniform") -> engine.Image:
        if seed is not None and not isinstance(seed, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"seed 只支持int类型参数, 传入类型为{type(seed)}"
            )

        if distribution is not None and not isinstance(distribution, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"distribution 只支持str类型参数, 传入类型为{type(distribution)}",
            )

        invoke_args = {
            "input": self,
            "seed": seed,
            "distribution": distribution,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Image.random", "engine.Image", invoke_args)

    def sampleRegion(
        self, region: engine.Geometry, scale: [int, float], geometries: bool = False
    ) -> engine.FeatureCollection:
        if region is not None and not isinstance(region, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"region 只支持engine.Geometry类型参数, 传入类型为{type(region)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        if geometries is not None and not isinstance(geometries, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometries 只支持bool类型参数, 传入类型为{type(geometries)}",
            )

        invoke_args = {
            "input": self,
            "region": region,
            "scale": scale,
            "geometries": geometries,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "region" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数region不能为空")

        if "scale" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数scale不能为空")

        return FunctionHelper.apply(
            "Image.sampleRegion", "engine.FeatureCollection", invoke_args
        )

    def sampleRegions(
        self,
        collection: engine.FeatureCollection,
        scale: [int, float],
        properties: list = None,
        geometries: bool = False,
    ) -> engine.FeatureCollection:
        if collection is not None and not isinstance(
            collection, engine.FeatureCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection 只支持engine.FeatureCollection类型参数, 传入类型为{type(collection)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        if properties is not None and not isinstance(properties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"properties 只支持list类型参数, 传入类型为{type(properties)}",
            )

        if geometries is not None and not isinstance(geometries, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometries 只支持bool类型参数, 传入类型为{type(geometries)}",
            )

        invoke_args = {
            "input": self,
            "collection": collection,
            "scale": scale,
            "properties": properties,
            "geometries": geometries,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection不能为空")

        if "scale" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数scale不能为空")

        return FunctionHelper.apply(
            "Image.sampleRegions", "engine.FeatureCollection", invoke_args
        )

    def samplePoints(
        self,
        collection: engine.FeatureCollection,
        scale: [int, float],
        properties: list = None,
        geometries: bool = False,
    ) -> engine.FeatureCollection:
        if collection is not None and not isinstance(
            collection, engine.FeatureCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection 只支持engine.FeatureCollection类型参数, 传入类型为{type(collection)}",
            )

        if scale is not None and not isinstance(scale, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"scale 只支持(int,float)类型参数, 传入类型为{type(scale)}"
            )

        if properties is not None and not isinstance(properties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"properties 只支持list类型参数, 传入类型为{type(properties)}",
            )

        if geometries is not None and not isinstance(geometries, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"geometries 只支持bool类型参数, 传入类型为{type(geometries)}",
            )

        invoke_args = {
            "input": self,
            "collection": collection,
            "scale": scale,
            "properties": properties,
            "geometries": geometries,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection不能为空")

        if "scale" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数scale不能为空")

        return FunctionHelper.apply(
            "Image.samplePoints", "engine.FeatureCollection", invoke_args
        )

    def cast(self, bandTypes: dict) -> engine.Image:
        if bandTypes is not None and not isinstance(bandTypes, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"bandTypes 只支持dict类型参数, 传入类型为{type(bandTypes)}",
            )

        invoke_args = {
            "input": self,
            "bandTypes": bandTypes,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "bandTypes" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数bandTypes不能为空")

        return FunctionHelper.apply("Image.cast", "engine.Image", invoke_args)

    def set(self, var_args: dict) -> engine.Image:
        if var_args is not None and not isinstance(var_args, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"var_args 只支持dict类型参数, 传入类型为{type(var_args)}"
            )

        invoke_args = {
            "input": self,
            "var_args": var_args,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "var_args" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数var_args不能为空")

        return FunctionHelper.apply("Image.set", "engine.Image", invoke_args)
