#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Image.load
ImageCollection.load
ImageCollection.fromImages
Feature
FeatureCollection.load
FeatureCollection.fromFeatures
'''

ImageConstructorsImpl = '''
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
                invoke_args = {
                    "srcImg": image,
                    "dstImg": result
                }
                result = FunctionHelper.apply("Image.addBands", "engine.Image", invoke_args)
            super(Image, self).__init__(result.func_name, result.invoke_args, result.var_name)
        elif args is None:
            image = Image(0)
            invoke_args = {
                "input": image,
                "mask": image
            }
            super(Image, self).__init__("Image.mask", invoke_args)
        elif isinstance(args, engine.variable_node.VariableNode):
            super(Image, self).__init__(args.func_name, args.invoke_args, args.var_name)
        elif isinstance(args, engine.function_node.FunctionNode):
            super(Image, self).__init__(args.func_name, args.invoke_args, args.var_name)
        else:
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"args 只支持number|str|list类型参数, 传入类型为{type(args)}")
'''

ImageCollectionConstructorsImpl = '''
    def __init__(self, args) -> engine.ImageCollection:
        if isinstance(args, str):
            invoke_args = {"id": args}
            super(ImageCollection, self).__init__("ImageCollection.load", invoke_args)
        elif isinstance(args, engine.Image):
            args = [args]
            invoke_args = {"images": args}
            super(ImageCollection, self).__init__("ImageCollection.fromImages", invoke_args)
        elif isinstance(args, (list, tuple)):
            images = [engine.Image(i) for i in args]
            invoke_args = {"images": images}
            super(ImageCollection, self).__init__("ImageCollection.fromImages", invoke_args)
        else:
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"args 只支持str|engine.Image|list类型参数, 传入类型为{type(args)}")
'''

FeatureConstructorsImpl = '''
    def __init__(self, geometry, properties=None) -> engine.Feature:
        args = geometry
        if isinstance(args, engine.Geometry):
            if properties is not None and not isinstance(properties, dict):
                raise AIEError(AIEErrorCode.ARGS_ERROR, f"properties 只支持dict类型参数, 传入类型为{type(properties)}")

            invoke_args = {
                "geometry": geometry,
                "properties": properties,
            }
            
            invoke_args = {k: v for k, v in invoke_args.items() if v is not None}
            super(Feature, self).__init__("Feature", invoke_args)
        elif isinstance(args, engine.variable_node.VariableNode):
            super(Feature, self).__init__(args.func_name, args.invoke_args, args.var_name)
        elif isinstance(args, engine.function_node.FunctionNode):
            super(Feature, self).__init__(args.func_name, args.invoke_args, args.var_name)
        elif args is None:
            invoke_args = {
                "geometry": geometry,
                "properties": properties,
            }
            
            invoke_args = {k: v for k, v in invoke_args.items() if v is not None}
            super(Feature, self).__init__("Feature", invoke_args)
        else:
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"geometry 只支持engine.Geometry类型参数, 传入类型为{type(geometry)}")

'''

FeatureCollectionConstructorsImpl = '''
    def __init__(self, args) -> engine.FeatureCollection:
        if isinstance(args, str):
            invoke_args = {"id": args}
            super(FeatureCollection, self).__init__("FeatureCollection.load", invoke_args)
        elif isinstance(args, engine.Feature):
            args = [args]
            invoke_args = {"features": args}
            super(FeatureCollection, self).__init__("FeatureCollection.fromFeatures", invoke_args)
        elif isinstance(args, (list, tuple)):
            features = [engine.Feature(i) for i in args]
            invoke_args = {"features": features}
            super(FeatureCollection, self).__init__("FeatureCollection.fromFeatures", invoke_args)
        else:
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"args 只支持str|engine.Feature|list类型参数, 传入类型为{type(args)}")
'''

CollectionElementTypeImpl = '''
    @abc.abstractmethod
    def elementType(self):
        pass
'''
ImageCollectionElementTypeImpl = '''
    def elementType(self):
        return engine.Image
'''
FeatureCollectionElementTypeImpl = '''
    def elementType(self):
        return engine.Feature
'''

CollectionMapImpl = '''
    def map(self, baseAlgorithm) -> engine.Collection:
        import types
        if baseAlgorithm is not None and not isinstance(baseAlgorithm, types.FunctionType):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"baseAlgorithm 只支持function类型参数, 传入类型为{type(baseAlgorithm)}")

        args = inspect.getfullargspec(baseAlgorithm).args
        mapping_args = ["_MAPPING_VAR_#arg" + str(k) + "_" + v for k,v in enumerate(args)]
        variables = [VariableNode(mapping_arg) for mapping_arg in mapping_args]

        element_type = self.elementType()
        def func_warp(e): return baseAlgorithm(element_type(e))
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
'''

ImageCollectionMapImpl = """
    def map(self, baseAlgorithm: types.FunctionType) -> Union[engine.ImageCollection, engine.FeatureCollection]:

        node = super(ImageCollection, self).map(baseAlgorithm)
        baseAlgorithm_return_type = type(node.invoke_args["baseAlgorithm"].body)
        if engine.Feature == baseAlgorithm_return_type:
            return FunctionHelper.cast(node, "engine.FeatureCollection")
        else:
            return FunctionHelper.cast(node, "engine.ImageCollection")
"""

FeatureCollectionMapImpl = """
    def map(self, baseAlgorithm: types.FunctionType) -> Union[engine.ImageCollection, engine.FeatureCollection]:

        node = super(FeatureCollection, self).map(baseAlgorithm)
        baseAlgorithm_return_type = type(node.invoke_args["baseAlgorithm"].body)
        if engine.Image == baseAlgorithm_return_type:
            return FunctionHelper.cast(node, "engine.ImageCollection")
        else:
            return FunctionHelper.cast(node, "engine.FeatureCollection")
"""

GetMapIdImpl = '''
    def getMapId(self, vis_params):
        if vis_params is not None and not isinstance(vis_params, dict):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"vis_params 只支持dict类型参数, 传入类型为{type(vis_params)}")
        return engine.client.Maps.getMapId(self, vis_params)
'''

ImageSelectImpl = '''
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
'''

ImageCollectionSelectImpl = '''
    def select(self, selectors) -> engine.ImageCollection:
        return self.map(lambda image: image.select(selectors))
'''

GetCenterImpl = '''
    def getCenter(self) -> tuple:
        bbox = engine.client.InteractiveSession.getBounds(self)
        if bbox is not None and isinstance(bbox, list):
            center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            return center
        raise AIEError(AIEErrorCode.ARGS_ERROR, f"获取Center失败. bbox: {bbox}")
'''

GetBoundsImpl = '''
    def getBounds(self) -> list:
        bbox = engine.client.InteractiveSession.getBounds(self)
        if bbox is not None and isinstance(bbox, list):
            bounds = [bbox[0], bbox[1], bbox[2], bbox[3]]
            return bounds
        raise AIEError(AIEErrorCode.ARGS_ERROR, f"获取Bounds失败. bbox: {bbox}")
'''

ClassifierTrainImpl = '''
    def train(
        self, features: engine.FeatureCollection, classProperty: str, inputProperties: list
    ) -> engine.Classifier:

        if features is not None and not isinstance(features, engine.FeatureCollection):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"features 只支持engine.FeatureCollection类型参数, 传入类型为{type(features)}",
            )

        if classProperty is not None and not isinstance(classProperty, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"classProperty 只支持str类型参数, 传入类型为{type(classProperty)}",
            )

        if inputProperties is not None and not isinstance(inputProperties, list):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"inputProperties 只支持list类型参数, 传入类型为{type(inputProperties)}",
            )

        invoke_args = {
            "input": self,
            "features": features,
            "classProperty": classProperty,
            "inputProperties": inputProperties,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "features" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数features不能为空")

        if "classProperty" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数classProperty不能为空")

        if "inputProperties" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数inputProperties不能为空")

        clf = FunctionHelper.apply("Classifier.train", "engine.Classifier", invoke_args)

        obj = engine.client.InteractiveSession.classifierTrain(clf)
        invoke_args['preResult'] = obj
        clf = FunctionHelper.apply("Classifier.train", "engine.Classifier", invoke_args)

        return clf
'''

GeometryConstructorsImpl = '''
    def __init__(self, geoJson: object) -> engine.Geometry:
        def _isValidGeometry(geometry):
            if not isinstance(geometry, dict):
                raise AIEError(AIEErrorCode.ARGS_ERROR, f"geoJson 不合法. 类型应该为dict")
            
            if "type" not in geometry:
                raise AIEError(AIEErrorCode.ARGS_ERROR, f"geoJson 不合法. 缺少type")

        _isValidGeometry(geoJson)

        geo_type = geoJson['type']
        coordinates = geoJson.get('coordinates')
        geometries = geoJson.get('geometries')

        ctor_args = {}
        if geo_type == 'GeometryCollection':
            ctor_name = 'MultiGeometry'
            ctor_args['geometries'] = [Geometry(g) for g in geometries]
        else:
            ctor_name = geo_type
            ctor_args['coordinates'] = coordinates

        super(Geometry, self).__init__("GeometryConstructors." + ctor_name, ctor_args)
'''


ModelConstructorsImpl = '''
    def __init__(self, modelName) -> engine.Model:
        self.modelName = modelName
        super(Model, self).__init__("Model.load" , {
            "modelName": modelName
        })
'''

IMPL = {k: v for k, v in vars().items() if not k.startswith("__")}
