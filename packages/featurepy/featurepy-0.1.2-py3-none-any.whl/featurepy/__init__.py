from aspectlib import Aspect, weave, Proceed, Return
from .model_constraints import model_constraints
from .parametric_features import select_parametric_features

from featuremonkey3 import Composer, select, select_equation
weave(select, [select_parametric_features, model_constraints])
