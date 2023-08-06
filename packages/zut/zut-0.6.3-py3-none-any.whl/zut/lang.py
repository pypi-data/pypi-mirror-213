from __future__ import annotations
import sys
from pathlib import Path


# Export root directory of the library
ZUT_ROOT = Path(__file__).parent


# Export typings from adequate library
if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Literal, Protocol
else:
    from typing import Literal, Protocol
    
if sys.version_info[0:2] < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


def is_list_or_tuple_of(instance, element_type: type|tuple[type]):
    if not isinstance(instance, (list,tuple)):
        return False

    for element in instance:
        if not isinstance(element, element_type):
            return False
        
    return True
