# Copyright 2023 TileDB Inc.
# Licensed under the MIT License.

"""Class to render the BioImageViewer."""
import os
from IPython.display import display
from ipywidgets import DOMWidget, register
from typing import Optional, TypedDict
from traitlets import Dict, Unicode
from ._frontend import module_name, module_version

@register
class BioImageViewer(DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _model_name = Unicode("BioImageViewerModel").tag(sync=True)
    _view_name = Unicode("BioImageViewerView").tag(sync=True)
    value = Dict().tag(sync=True)

class Options(TypedDict):
    basePath: Optional[str]
    token: Optional[str]
    baseGroup: Optional[str]
class Render:
    def __init__(self, namespace, groupId, options: Options = {"token": None, "basePath": None}):
        self._value = None

        token = options.get("token") or os.getenv("TILEDB_REST_TOKEN")
        basePath = options.get("basePath") or os.getenv("TILEDB_REST_HOST")

        if token == None:
            raise Exception("Token should be provided, either as an argument or as an env variable.")

        data = {
            "namespace": namespace,
            "groupID": groupId,
            "token": token,
            "basePath": basePath,
            "baseGroup": options.get('baseGroup')
        }

        viewer = BioImageViewer()
        viewer.value = data
        display(viewer)
