import os
from typing import Optional
import streamlit.components.v1 as components

_RELEASE = True


if not _RELEASE:
    _cartographer = components.declare_component(
        "mapbot_frontend", url=os.environ["FRONTEND_URL"]
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("mapbot_frontend", path=build_dir)


def cartographer(cartographer_state, key: Optional[str] = None):
    component_value = _cartographer(cartographer_state=cartographer_state, key=key)
    return component_value

