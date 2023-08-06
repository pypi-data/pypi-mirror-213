#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .function_node import FunctionNode


class VariableNode(FunctionNode):
    def __init__(self, var_name):
        super(VariableNode, self).__init__(None, None, var_name)
