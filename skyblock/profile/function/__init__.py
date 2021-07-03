from .action import action_functions
from .display import display_functions
from .item import item_functions
from .math import math_functions


__all__ = ['profile_functions']

profile_functions = {**action_functions, **display_functions,
                     **item_functions, **math_functions}
