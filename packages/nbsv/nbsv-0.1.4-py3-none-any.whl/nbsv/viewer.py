#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Megan Riel-Mehan.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""
import ipywidgets
from traitlets import Unicode, Int
from ._frontend import module_name, module_version

@ipywidgets.register
class ViewerWidget(ipywidgets.DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('TrajectoryModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('Viewport').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    trajectory = Unicode("").tag(sync=True)
    width = Int(500).tag(sync=True)
    height = Int(300).tag(sync=True)

    def load_model(self, trajectory):
        pass

    