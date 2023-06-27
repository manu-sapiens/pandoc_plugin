# --------------- SHARED ---------------------------------------------------
import sys
from typing import List, Any
sys.path.append('.')  # Add the current directory to the sys path
sys.path.append('utils')  # Add the utils directory to the sys path

from utils.omni_utils_http import CdnResponse, ImageMeta, create_api_route, plugin_main, init_plugin
from pydantic import BaseModel
endpoints = []
app, router = init_plugin()
# ---------------------------------------------------------------------------
plugin_module_name = "Plugins.pandoc_plugin.pandoc" 

# ---------------------------------------------------
# --------------- PANDOC CONVERT ---------------------
# ---------------------------------------------------
ENDPOINT_PANDOC_CONVERT = "/pandoc/convert"

class PandocConvert_Input(BaseModel):
    documents: List[CdnResponse]
    input_format: str
    output_format: str

    class Config:
        schema_extra = {
            "title": "Pandoc: Convert documents"
        }

class PandocConvert_Response(BaseModel):
    media_array: List[CdnResponse]

    class Config:
        schema_extra = {
            "title": "Pandoc Convert Output"
        }

PandocConvert_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_PANDOC_CONVERT,
    input_class=PandocConvert_Input,
    response_class=PandocConvert_Response,
    handle_post_function="PandocConvert_HandlePost",
    plugin_module_name=plugin_module_name,
)

endpoints = [ENDPOINT_PANDOC_CONVERT]

# --------------- SHARED ---------------------------------------------------
plugin_main(app, __name__, __file__)
# --------------------------------------------------------------------------