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


class FeatureCollection(engine.Collection):
    def __init__(self, args) -> engine.FeatureCollection:
        if isinstance(args, str):
            invoke_args = {"id": args}
            super(FeatureCollection, self).__init__(
                "FeatureCollection.load", invoke_args
            )
        elif isinstance(args, engine.Feature):
            args = [args]
            invoke_args = {"features": args}
            super(FeatureCollection, self).__init__(
                "FeatureCollection.fromFeatures", invoke_args
            )
        elif isinstance(args, (list, tuple)):
            features = [engine.Feature(i) for i in args]
            invoke_args = {"features": features}
            super(FeatureCollection, self).__init__(
                "FeatureCollection.fromFeatures", invoke_args
            )
        else:
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"args 只支持str|engine.Feature|list类型参数, 传入类型为{type(args)}",
            )

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

    def elementType(self):
        return engine.Feature

    def propertyNames(self) -> object:
        invoke_args = {
            "element": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "FeatureCollection.propertyNames", "object", invoke_args
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
            "FeatureCollection.aggregate_max", "object", invoke_args
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
            "FeatureCollection.aggregate_min", "object", invoke_args
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
            "FeatureCollection.aggregate_mean", "object", invoke_args
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
            "FeatureCollection.aggregate_count", "object", invoke_args
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
            "FeatureCollection.aggregate_sum", "object", invoke_args
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
            "FeatureCollection.aggregate_stats", "object", invoke_args
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
            "FeatureCollection.aggregate_array", "object", invoke_args
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
            "FeatureCollection.aggregate_product", "object", invoke_args
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
            "FeatureCollection.aggregate_sample_sd", "object", invoke_args
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
            "FeatureCollection.aggregate_sample_var", "object", invoke_args
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
            "FeatureCollection.aggregate_total_sd", "object", invoke_args
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
            "FeatureCollection.aggregate_total_var", "object", invoke_args
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
            "FeatureCollection.aggregate_histogram", "object", invoke_args
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
            "FeatureCollection.aggregate_count_distinct", "object", invoke_args
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
            "FeatureCollection.aggregate_first", "object", invoke_args
        )

    def reduceColumns(
        self, reducer: engine.Reducer, selectors: list, weightSelectors: list = None
    ) -> object:
        if reducer is not None and not isinstance(reducer, engine.Reducer):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"reducer 只支持engine.Reducer类型参数, 传入类型为{type(reducer)}",
            )

        if selectors is not None and not isinstance(selectors, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"selectors 只支持list类型参数, 传入类型为{type(selectors)}",
            )

        if weightSelectors is not None and not isinstance(weightSelectors, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"weightSelectors 只支持list类型参数, 传入类型为{type(weightSelectors)}",
            )

        invoke_args = {
            "collection": self,
            "reducer": reducer,
            "selectors": selectors,
            "weightSelectors": weightSelectors,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "reducer" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数reducer不能为空")

        if "selectors" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数selectors不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.reduceColumns", "object", invoke_args
        )

    def union(self, maxError: int = None) -> engine.FeatureCollection:
        if maxError is not None and not isinstance(maxError, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"maxError 只支持int类型参数, 传入类型为{type(maxError)}"
            )

        invoke_args = {
            "collection": self,
            "maxError": maxError,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "FeatureCollection.union", "engine.FeatureCollection", invoke_args
        )

    def distinct(self, properties: list) -> engine.FeatureCollection:
        if properties is not None and not isinstance(properties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"properties 只支持list类型参数, 传入类型为{type(properties)}",
            )

        invoke_args = {
            "collection": self,
            "properties": properties,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "properties" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数properties不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.distinct", "engine.FeatureCollection", invoke_args
        )

    def map(
        self, baseAlgorithm: types.FunctionType
    ) -> Union[engine.ImageCollection, engine.FeatureCollection]:
        node = super(FeatureCollection, self).map(baseAlgorithm)
        baseAlgorithm_return_type = type(node.invoke_args["baseAlgorithm"].body)
        if engine.Image == baseAlgorithm_return_type:
            return FunctionHelper.cast(node, "engine.ImageCollection")
        else:
            return FunctionHelper.cast(node, "engine.FeatureCollection")

    def merge(self, collection2: engine.FeatureCollection) -> engine.FeatureCollection:
        if collection2 is not None and not isinstance(
            collection2, engine.FeatureCollection
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"collection2 只支持engine.FeatureCollection类型参数, 传入类型为{type(collection2)}",
            )

        invoke_args = {
            "collection1": self,
            "collection2": collection2,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "collection2" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数collection2不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.merge", "engine.FeatureCollection", invoke_args
        )

    def randomColumn(
        self, columnName: str = "random", seed: int = 0, distribution: str = "uniform"
    ) -> engine.FeatureCollection:
        if columnName is not None and not isinstance(columnName, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"columnName 只支持str类型参数, 传入类型为{type(columnName)}",
            )

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
            "collection": self,
            "columnName": columnName,
            "seed": seed,
            "distribution": distribution,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "FeatureCollection.randomColumn", "engine.FeatureCollection", invoke_args
        )

    @staticmethod
    def randomPoints(
        region: engine.Geometry, points: int = 1000, seed: int = 0, maxError: int = None
    ) -> engine.FeatureCollection:
        if region is not None and not isinstance(region, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"region 只支持engine.Geometry类型参数, 传入类型为{type(region)}",
            )

        if points is not None and not isinstance(points, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"points 只支持int类型参数, 传入类型为{type(points)}"
            )

        if seed is not None and not isinstance(seed, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"seed 只支持int类型参数, 传入类型为{type(seed)}"
            )

        if maxError is not None and not isinstance(maxError, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"maxError 只支持int类型参数, 传入类型为{type(maxError)}"
            )

        invoke_args = {
            "region": region,
            "points": points,
            "seed": seed,
            "maxError": maxError,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "region" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数region不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.randomPoints", "engine.FeatureCollection", invoke_args
        )

    def select(
        self,
        propertySelectors: list,
        newProperties: list = None,
        retainGeometry: bool = True,
    ) -> engine.FeatureCollection:
        if propertySelectors is not None and not isinstance(propertySelectors, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"propertySelectors 只支持list类型参数, 传入类型为{type(propertySelectors)}",
            )

        if newProperties is not None and not isinstance(newProperties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"newProperties 只支持list类型参数, 传入类型为{type(newProperties)}",
            )

        if retainGeometry is not None and not isinstance(retainGeometry, bool):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"retainGeometry 只支持bool类型参数, 传入类型为{type(retainGeometry)}",
            )

        invoke_args = {
            "featurecollection": self,
            "propertySelectors": propertySelectors,
            "newProperties": newProperties,
            "retainGeometry": retainGeometry,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "propertySelectors" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数propertySelectors不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.select", "engine.FeatureCollection", invoke_args
        )

    def filter(self, filter: engine.Filter) -> engine.FeatureCollection:
        node = super(FeatureCollection, self).filter(filter)
        return FunctionHelper.cast(node, "engine.FeatureCollection")

    def filterBounds(
        self, geometry: Union[engine.Geometry, engine.Feature, engine.FeatureCollection]
    ) -> engine.FeatureCollection:
        node = super(FeatureCollection, self).filterBounds(geometry)
        return FunctionHelper.cast(node, "engine.FeatureCollection")

    def first(self) -> engine.Feature:
        node = super(FeatureCollection, self).first()
        return FunctionHelper.cast(node, "engine.Feature")

    def limit(
        self, max: [int, float], property: str = None, ascending: bool = None
    ) -> engine.FeatureCollection:
        node = super(FeatureCollection, self).limit(max, property=None, ascending=None)
        return FunctionHelper.cast(node, "engine.FeatureCollection")

    def geometry(self) -> engine.Geometry:
        invoke_args = {
            "collection": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "FeatureCollection.geometry", "engine.Geometry", invoke_args
        )

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

        return FunctionHelper.apply("FeatureCollection.toList", "object", invoke_args)

    def sort(self, property: str, ascending: bool = True) -> engine.FeatureCollection:
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
            "FeatureCollection.sort", "engine.FeatureCollection", invoke_args
        )

    def classify(
        self, classifier: engine.Classifier, outputName: str = "classification"
    ) -> engine.FeatureCollection:
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

        return FunctionHelper.apply(
            "FeatureCollection.classify", "engine.FeatureCollection", invoke_args
        )

    def errorMatrix(self, actual: str, predicted: str) -> engine.ConfusionMatrix:
        if actual is not None and not isinstance(actual, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"actual 只支持str类型参数, 传入类型为{type(actual)}"
            )

        if predicted is not None and not isinstance(predicted, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"predicted 只支持str类型参数, 传入类型为{type(predicted)}"
            )

        invoke_args = {
            "input": self,
            "actual": actual,
            "predicted": predicted,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "actual" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数actual不能为空")

        if "predicted" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数predicted不能为空")

        return FunctionHelper.apply(
            "FeatureCollection.errorMatrix", "engine.ConfusionMatrix", invoke_args
        )

    def renamePropertyNames(self, var_args: dict) -> engine.FeatureCollection:
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

        return FunctionHelper.apply(
            "FeatureCollection.renamePropertyNames",
            "engine.FeatureCollection",
            invoke_args,
        )
