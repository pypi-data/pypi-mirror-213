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


class Terrain(FunctionNode):
    @staticmethod
    def aspect(input: engine.Image) -> engine.Image:
        if input is not None and not isinstance(input, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"input 只支持engine.Image类型参数, 传入类型为{type(input)}",
            )

        invoke_args = {
            "input": input,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "input" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数input不能为空")

        return FunctionHelper.apply("Terrain.aspect", "engine.Image", invoke_args)

    @staticmethod
    def slope(input: engine.Image) -> engine.Image:
        if input is not None and not isinstance(input, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"input 只支持engine.Image类型参数, 传入类型为{type(input)}",
            )

        invoke_args = {
            "input": input,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "input" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数input不能为空")

        return FunctionHelper.apply("Terrain.slope", "engine.Image", invoke_args)

    @staticmethod
    def hillshade(
        input: engine.Image, azimuth: [int, float] = 270, elevation: [int, float] = 45
    ) -> engine.Image:
        if input is not None and not isinstance(input, engine.Image):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"input 只支持engine.Image类型参数, 传入类型为{type(input)}",
            )

        if azimuth is not None and not isinstance(azimuth, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"azimuth 只支持(int,float)类型参数, 传入类型为{type(azimuth)}",
            )

        if elevation is not None and not isinstance(elevation, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"elevation 只支持(int,float)类型参数, 传入类型为{type(elevation)}",
            )

        invoke_args = {
            "input": input,
            "azimuth": azimuth,
            "elevation": elevation,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "input" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数input不能为空")

        return FunctionHelper.apply("Terrain.hillshade", "engine.Image", invoke_args)
