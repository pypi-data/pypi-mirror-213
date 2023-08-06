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


class Geometry(FunctionNode):
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

    def __init__(self, geoJson: object) -> engine.Geometry:
        def _isValidGeometry(geometry):
            if not isinstance(geometry, dict):
                raise AIEError(AIEErrorCode.ARGS_ERROR, f"geoJson 不合法. 类型应该为dict")

            if "type" not in geometry:
                raise AIEError(AIEErrorCode.ARGS_ERROR, f"geoJson 不合法. 缺少type")

        _isValidGeometry(geoJson)

        geo_type = geoJson["type"]
        coordinates = geoJson.get("coordinates")
        geometries = geoJson.get("geometries")

        ctor_args = {}
        if geo_type == "GeometryCollection":
            ctor_name = "MultiGeometry"
            ctor_args["geometries"] = [Geometry(g) for g in geometries]
        else:
            ctor_name = geo_type
            ctor_args["coordinates"] = coordinates

        super(Geometry, self).__init__("GeometryConstructors." + ctor_name, ctor_args)

    def getMapId(self, vis_params):
        if vis_params is not None and not isinstance(vis_params, dict):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"vis_params 只支持dict类型参数, 传入类型为{type(vis_params)}",
            )
        return engine.client.Maps.getMapId(self, vis_params)

    @staticmethod
    def BBox(
        west: [int, float], south: [int, float], east: [int, float], north: [int, float]
    ) -> engine.Geometry:
        if west is not None and not isinstance(west, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"west 只支持(int,float)类型参数, 传入类型为{type(west)}"
            )

        if south is not None and not isinstance(south, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"south 只支持(int,float)类型参数, 传入类型为{type(south)}"
            )

        if east is not None and not isinstance(east, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"east 只支持(int,float)类型参数, 传入类型为{type(east)}"
            )

        if north is not None and not isinstance(north, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"north 只支持(int,float)类型参数, 传入类型为{type(north)}"
            )

        invoke_args = {
            "west": west,
            "south": south,
            "east": east,
            "north": north,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "west" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数west不能为空")

        if "south" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数south不能为空")

        if "east" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数east不能为空")

        if "north" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数north不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.BBox", "engine.Geometry", invoke_args
        )

    @staticmethod
    def Point(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.Point", "engine.Geometry", invoke_args
        )

    @staticmethod
    def Polygon(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.Polygon", "engine.Geometry", invoke_args
        )

    @staticmethod
    def Rectangle(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.Rectangle", "engine.Geometry", invoke_args
        )

    @staticmethod
    def LineString(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.LineString", "engine.Geometry", invoke_args
        )

    @staticmethod
    def MultiPoint(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.MultiPoint", "engine.Geometry", invoke_args
        )

    @staticmethod
    def MultiLineString(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.MultiLineString", "engine.Geometry", invoke_args
        )

    @staticmethod
    def MultiPolygon(coordinates: list) -> engine.Geometry:
        if coordinates is not None and not isinstance(coordinates, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"coordinates 只支持list类型参数, 传入类型为{type(coordinates)}",
            )

        invoke_args = {
            "coordinates": coordinates,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "coordinates" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数coordinates不能为空")

        return FunctionHelper.apply(
            "GeometryConstructors.MultiPolygon", "engine.Geometry", invoke_args
        )

    def voronoiDiagram(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Geometry.voronoiDiagram", "engine.Geometry", invoke_args
        )

    def delaunayTriangulation(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Geometry.delaunayTriangulation", "engine.Geometry", invoke_args
        )

    def smooth(
        self, iterations: int, offset: [int, float], maxAngle: [int, float]
    ) -> engine.Geometry:
        if iterations is not None and not isinstance(iterations, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"iterations 只支持int类型参数, 传入类型为{type(iterations)}",
            )

        if offset is not None and not isinstance(offset, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"offset 只支持(int,float)类型参数, 传入类型为{type(offset)}",
            )

        if maxAngle is not None and not isinstance(maxAngle, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"maxAngle 只支持(int,float)类型参数, 传入类型为{type(maxAngle)}",
            )

        invoke_args = {
            "geometry": self,
            "iterations": iterations,
            "offset": offset,
            "maxAngle": maxAngle,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "iterations" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数iterations不能为空")

        if "offset" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数offset不能为空")

        if "maxAngle" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数maxAngle不能为空")

        return FunctionHelper.apply("Geometry.smooth", "engine.Geometry", invoke_args)

    def area(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.area", "object", invoke_args)

    def perimeter(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.perimeter", "object", invoke_args)

    def length(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.length", "object", invoke_args)

    def coordinates(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.coordinates", "object", invoke_args)

    def type(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.type", "object", invoke_args)

    def bounds(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.bounds", "engine.Geometry", invoke_args)

    def centroid(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.centroid", "engine.Geometry", invoke_args)

    def convexHull(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply(
            "Geometry.convexHull", "engine.Geometry", invoke_args
        )

    def cutLines(self, distance: list) -> engine.Geometry:
        if distance is not None and not isinstance(distance, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"distance 只支持list类型参数, 传入类型为{type(distance)}"
            )

        invoke_args = {
            "geometry": self,
            "distance": distance,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "distance" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数distance不能为空")

        return FunctionHelper.apply("Geometry.cutLines", "engine.Geometry", invoke_args)

    def simplify(self, tolerance: [int, float]) -> engine.Geometry:
        if tolerance is not None and not isinstance(tolerance, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"tolerance 只支持(int,float)类型参数, 传入类型为{type(tolerance)}",
            )

        invoke_args = {
            "geometry": self,
            "tolerance": tolerance,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "tolerance" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数tolerance不能为空")

        return FunctionHelper.apply("Geometry.simplify", "engine.Geometry", invoke_args)

    def transform(self, proj: str) -> engine.Geometry:
        if proj is not None and not isinstance(proj, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"proj 只支持str类型参数, 传入类型为{type(proj)}"
            )

        invoke_args = {
            "geometry": self,
            "proj": proj,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "proj" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数proj不能为空")

        return FunctionHelper.apply(
            "Geometry.transform", "engine.Geometry", invoke_args
        )

    def distance(self, right: engine.Geometry) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.distance", "object", invoke_args)

    def withinDistance(self, right: engine.Geometry, distance: [int, float]) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        if distance is not None and not isinstance(distance, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"distance 只支持(int,float)类型参数, 传入类型为{type(distance)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
            "distance": distance,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        if "distance" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数distance不能为空")

        return FunctionHelper.apply("Geometry.withinDistance", "object", invoke_args)

    def containedIn(self, right: engine.Geometry) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.containedIn", "object", invoke_args)

    def contains(self, right: engine.Geometry) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.contains", "object", invoke_args)

    def difference(self, right: engine.Geometry) -> engine.Geometry:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply(
            "Geometry.difference", "engine.Geometry", invoke_args
        )

    def disjoint(self, right: engine.Geometry) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.disjoint", "object", invoke_args)

    def dissolve(self) -> engine.Geometry:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.dissolve", "engine.Geometry", invoke_args)

    def intersection(self, right: engine.Geometry) -> engine.Geometry:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply(
            "Geometry.intersection", "engine.Geometry", invoke_args
        )

    def intersects(self, right: engine.Geometry) -> object:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.intersects", "object", invoke_args)

    def symmetricDifference(self, right: engine.Geometry) -> engine.Geometry:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply(
            "Geometry.symmetricDifference", "engine.Geometry", invoke_args
        )

    def union(self, right: engine.Geometry) -> engine.Geometry:
        if right is not None and not isinstance(right, engine.Geometry):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持engine.Geometry类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "left": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Geometry.union", "engine.Geometry", invoke_args)

    def buffer(self, distance: [int, float]) -> engine.Geometry:
        if distance is not None and not isinstance(distance, (int, float)):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"distance 只支持(int,float)类型参数, 传入类型为{type(distance)}",
            )

        invoke_args = {
            "geometry": self,
            "distance": distance,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "distance" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数distance不能为空")

        return FunctionHelper.apply("Geometry.buffer", "engine.Geometry", invoke_args)

    def geometries(self) -> object:
        invoke_args = {
            "geometry": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Geometry.geometries", "object", invoke_args)
