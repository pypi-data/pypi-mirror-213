from featuremonkey3 import CompositionError
from aspectlib import Aspect, Return
import inspect
import importlib
import re


def parse_feature_args(feature: str) -> list[str]:
    # CANNOT PARSE LISTS, DICTS OR ANY DATA TYPE WITH COMMAS AND BRACKETS
    tokens = re.split("[(,)]", feature)
    featurename = tokens[0]
    args = []
    kwargs = {}
    if len(tokens) > 1:
        for token in tokens[1:]:
            if token != '':
                arg_params = token.split("=")
                if len(arg_params) == 1:
                    args.append(eval(arg_params[0]))
                else:
                    kwargs[arg_params[0].strip()] = eval(arg_params[1])

    return featurename, args, kwargs


@Aspect
def select_parametric_features(self, *features):
    for feature in features:
        try:
            feature_name, args, kwargs = parse_feature_args(feature)
            feature_spec_module = importlib.import_module(
                feature_name + '.feature'
            )
            if not hasattr(feature_spec_module, 'select'):
                raise CompositionError(
                    'Function %s.feature.select not found!\n '
                    'Feature modules need to specify a function'
                    ' select(composer).' % (
                        feature_name
                    )
                )
            inspectargs = inspect.getfullargspec(feature_spec_module.select)
            if len(inspectargs[0]) == 0:
                raise CompositionError(
                    f"{feature_name}.feature.select must at least have one positional argument composer.")

            feature_spec_module.select(self, *args, **kwargs)
        except ImportError:
            raise
    yield Return
