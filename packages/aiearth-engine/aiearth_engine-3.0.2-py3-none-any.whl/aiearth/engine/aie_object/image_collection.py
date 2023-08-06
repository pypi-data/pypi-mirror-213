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


class ImageCollection(engine.Collection):
    def __init__(self, args) -> engine.ImageCollection:
        if isinstance(args, str):
            invoke_args = {"id": args}
            super(ImageCollection, self).__init__("ImageCollection.load", invoke_args)
        elif isinstance(args, engine.Image):
            args = [args]
            invoke_args = {"images": args}
            super(ImageCollection, self).__init__(
                "ImageCollection.fromImages", invoke_args
            )
        elif isinstance(args, (list, tuple)):
            images = [engine.Image(i) for i in args]
            invoke_args = {"images": images}
            super(ImageCollection, self).__init__(
                "ImageCollection.fromImages", invoke_args
            )
        else:
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"args 只支持str|engine.Image|list类型参数, 传入类型为{type(args)}",
            )

    def elementType(self):
        return engine.Image

    def getMapId(self, vis_params):
        if vis_params is not None and not isinstance(vis_params, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"vis_params 只支持dict类型参数, 传入类型为{type(vis_params)}",
            )
        return engine.client.Maps.getMapId(self, vis_params)

    def mosaic(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "ImageCollection.mosaic", "engine.Image", invoke_args
        )

    def qualityMosaic(self, qualityBand: str) -> engine.Image:
        if qualityBand is not None and not isinstance(qualityBand, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"qualityBand 只支持str类型参数, 传入类型为{type(qualityBand)}",
            )

        invoke_args = {
            "collection": self,
            "qualityBand": qualityBand,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "qualityBand" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数qualityBand不能为空")

        return FunctionHelper.apply(
            "ImageCollection.qualityMosaic", "engine.Image", invoke_args
        )

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

    def toList(self, count: int, offset: int = 0) -> object:
        if count is not None and not isinstance(count, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"count 只支持int类型参数, 传入类型为{type(count)}"
            )

        if offset is not None and not isinstance(offset, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"offset 只支持int类型参数, 传入类型为{type(offset)}"
            )

        invoke_args = {
            "collection": self,
            "count": count,
            "offset": offset,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "count" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数count不能为空")

        return FunctionHelper.apply("ImageCollection.toList", "object", invoke_args)

    def filter(self, filter: Union[str, engine.Filter]) -> engine.ImageCollection:
        node = super(ImageCollection, self).filter(filter)
        return FunctionHelper.cast(node, "engine.ImageCollection")

    def filterBounds(
        self, geometry: Union[engine.Geometry, engine.Feature, engine.FeatureCollection]
    ) -> engine.ImageCollection:
        node = super(ImageCollection, self).filterBounds(geometry)
        return FunctionHelper.cast(node, "engine.ImageCollection")

    def filterDate(self, start: str, end: str) -> engine.ImageCollection:
        if start is not None and not isinstance(start, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"start 只支持str类型参数, 传入类型为{type(start)}"
            )

        if end is not None and not isinstance(end, str):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"end 只支持str类型参数, 传入类型为{type(end)}")

        invoke_args = {
            "collection": self,
            "start": start,
            "end": end,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "start" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数start不能为空")

        if "end" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数end不能为空")

        return FunctionHelper.apply(
            "Collection.filterDate", "engine.ImageCollection", invoke_args
        )

    def first(self) -> engine.Image:
        node = super(ImageCollection, self).first()
        return FunctionHelper.cast(node, "engine.Image")

    def limit(
        self, limit: int, property: str = None, ascending: bool = True
    ) -> engine.ImageCollection:
        node = super(ImageCollection, self).limit(limit, property=None, ascending=True)
        return FunctionHelper.cast(node, "engine.ImageCollection")

    def reduce(self, reducer: engine.Reducer) -> engine.Image:
        if reducer is not None and not isinstance(reducer, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer 只支持engine.Reducer类型参数, 传入类型为{type(reducer)}",
            )

        invoke_args = {
            "collection": self,
            "reducer": reducer,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "reducer" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer不能为空")

        return FunctionHelper.apply(
            "ImageCollection.reduce", "engine.Image", invoke_args
        )

    def And(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.and", "engine.Image", invoke_args)

    def count(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.count", "engine.Image", invoke_args)

    def max(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.max", "engine.Image", invoke_args)

    def mean(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.mean", "engine.Image", invoke_args)

    def median(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.median", "engine.Image", invoke_args)

    def min(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.min", "engine.Image", invoke_args)

    def mode(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.mode", "engine.Image", invoke_args)

    def Or(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.or", "engine.Image", invoke_args)

    def product(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.product", "engine.Image", invoke_args)

    def sum(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("reduce.sum", "engine.Image", invoke_args)

    def map(
        self, baseAlgorithm: types.FunctionType
    ) -> Union[engine.ImageCollection, engine.FeatureCollection]:
        node = super(ImageCollection, self).map(baseAlgorithm)
        baseAlgorithm_return_type = type(node.invoke_args["baseAlgorithm"].body)
        if engine.Feature == baseAlgorithm_return_type:
            return FunctionHelper.cast(node, "engine.FeatureCollection")
        else:
            return FunctionHelper.cast(node, "engine.ImageCollection")

    def select(self, selectors) -> engine.ImageCollection:
        return self.map(lambda image: image.select(selectors))

    def sort(self, property: str, ascending: bool = True) -> engine.ImageCollection:
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
            "property": property,
            "ascending": ascending,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.sort", "engine.ImageCollection", invoke_args
        )

    def toBands(self) -> engine.Image:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "ImageCollection.toBands", "engine.Image", invoke_args
        )

    @staticmethod
    def fromImages(images: list) -> engine.ImageCollection:
        if images is not None and not isinstance(images, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"images 只支持list类型参数, 传入类型为{type(images)}"
            )

        invoke_args = {
            "images": images,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "images" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数images不能为空")

        return FunctionHelper.apply(
            "ImageCollection.fromImages", "engine.ImageCollection", invoke_args
        )

    def merge(self, collection2: engine.ImageCollection) -> engine.ImageCollection:
        if collection2 is not None and not isinstance(
            collection2, engine.ImageCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection2 只支持engine.ImageCollection类型参数, 传入类型为{type(collection2)}",
            )

        invoke_args = {
            "input": self,
            "collection2": collection2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection2不能为空")

        return FunctionHelper.apply(
            "ImageCollection.merge", "engine.ImageCollection", invoke_args
        )

    def cast(self, bandTypes: dict) -> engine.ImageCollection:
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

        return FunctionHelper.apply(
            "ImageCollection.cast", "engine.ImageCollection", invoke_args
        )

    def aggregate_max(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_max", "object", invoke_args
        )

    def aggregate_min(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_min", "object", invoke_args
        )

    def aggregate_mean(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_mean", "object", invoke_args
        )

    def aggregate_count(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_count", "object", invoke_args
        )

    def aggregate_sum(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_sum", "object", invoke_args
        )

    def aggregate_stats(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_stats", "object", invoke_args
        )

    def aggregate_array(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_array", "object", invoke_args
        )

    def aggregate_product(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_product", "object", invoke_args
        )

    def aggregate_sample_sd(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_sample_sd", "object", invoke_args
        )

    def aggregate_sample_var(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_sample_var", "object", invoke_args
        )

    def aggregate_total_sd(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_total_sd", "object", invoke_args
        )

    def aggregate_total_var(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_total_var", "object", invoke_args
        )

    def aggregate_histogram(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_histogram", "object", invoke_args
        )

    def aggregate_count_distinct(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_count_distinct", "object", invoke_args
        )

    def aggregate_first(self, property: str) -> object:
        if property is not None and not isinstance(property, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"property 只支持str类型参数, 传入类型为{type(property)}"
            )

        invoke_args = {
            "collection": self,
            "property": property,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "property" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数property不能为空")

        return FunctionHelper.apply(
            "ImageCollection.aggregate_first", "object", invoke_args
        )
