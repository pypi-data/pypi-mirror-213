from featuremonkey3 import compose
from aspectlib import weave
from functools import wraps
from types import FunctionType

import inspect


def feature_method(func):
    wraps(func)

    def wrapper(self, *args, **kwargs):

        cutpoint_aspects = self.aspects[func.__name__] if func.__name__ in self.aspects else {
        }
        result_func = func
        for cutpoint, aspects in cutpoint_aspects.items():
            base_func = result_func
            # if isinstance(cutpoint, str):
            #     cutpoint = eval(cutpoint)

            def weaved_func(self, *args, **kwargs):
                with weave(cutpoint, aspects):
                    return base_func(self, *args, **kwargs)

            result_func = weaved_func

        return result_func(self, *args, **kwargs)

    return wrapper


# TODO: weave aspects on methods
def feature(cls):
    wraps(cls)

    class Wrapper(cls):
        aspects = {}

        @classmethod
        def register_aspect(clss, method, cutpoint, aspect, **kwargs):  # Missing options
            if method not in clss.aspects:
                clss.aspects[method] = {}
            if cutpoint not in clss.aspects[method]:
                clss.aspects[method][cutpoint] = []
            clss.aspects[method][cutpoint].append(aspect)

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

    for name, function in inspect.getmembers(Wrapper, inspect.isfunction):
        setattr(Wrapper, name, feature_method(function))

    return Wrapper
