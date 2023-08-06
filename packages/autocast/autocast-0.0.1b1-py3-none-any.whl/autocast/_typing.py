import sys
from typing import Any, Callable, TypeVar

__all__ = ["Annotated", "Any", "Callable", "get_type_hints", "ParamSpec", "TypeVar"]

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_type_hints
else:
    from typing import Annotated, get_type_hints

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec
