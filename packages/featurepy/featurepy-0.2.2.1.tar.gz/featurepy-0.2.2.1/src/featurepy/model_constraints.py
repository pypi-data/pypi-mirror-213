from aspectlib import Aspect, Proceed
from yaml import safe_load


class FeatureSelectionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def is_optional(feature):
    return 'optional' in feature and feature['optional']


def has_children(feature):
    return feature is not None and 'children' in feature


def is_branch(feature, type):
    return 'branch' in feature and feature['branch'] == type


def is_abstract(feature):
    return feature['name'][0].isupper()


def get_features(fm):
    featurename = fm['name']

    features = [featurename] if (
        not featurename[0].isupper()) else []
    if fm is not None and 'children' in fm:
        for child in fm['children']:
            features += get_features(child)

    return features


def _is_operator(token: str) -> bool:
    return token in ["or", "and", "not"]


def parse_reqs(reqs, selections):
    tokens = reqs.split()
    expr = " ".join([f"{token} in selections" if not _is_operator(
        token) else token for token in tokens])
    return eval(expr)


def validate_selections(fm, selections: list[str], remaining_selections: list[str]):
    if not is_optional(fm) and not is_abstract(fm) and fm['name'] not in selections:
        raise FeatureSelectionError(
            f"Mandatory feature not selected: {fm['name']}")

    if 'cross-tree-reqs' in fm and fm['name'] in selections and not parse_reqs(fm['cross-tree-reqs'], selections):
        raise FeatureSelectionError(
            f"Cross-tree requirements not satisfied for {fm['name']}")

    if fm['name'] in selections:
        remaining_selections.remove(fm['name'])

    if (is_abstract(fm) or fm['name'] in selections) and has_children(fm):

        if is_branch(fm, 'xor') and len(set([child['name'] for child in fm['children']]).intersection(set(selections))) != 1:
            raise FeatureSelectionError(
                f"Incorrect number of xor features selected for branch {fm['name']}")

        for child in fm['children']:
            if child['name'] in selections and selections.index(child['name']) > selections.index(fm['name']):
                raise FeatureSelectionError(
                    f"Child feature {child['name']} is selected before parent {fm['name']}.")
            if is_branch(fm, 'or'):
                child['optional'] = True
            remaining_selections = validate_selections(
                child, selections, remaining_selections)

    return remaining_selections


@Aspect
def model_constraints(composer, *features):
    try:
        with open('feature_model.yml') as fp:
            feature_model = safe_load(fp)

        all_features = get_features(feature_model)
        selections = [feature.split("(")[0] for feature in features]

        if not set(selections).issubset(set(all_features)):
            raise FeatureSelectionError("Undefined features selected.")

        unvalidated_selections = validate_selections(
            feature_model, list(selections), list(selections))

        if unvalidated_selections != []:
            raise FeatureSelectionError(
                f"Parent features not selected or the feature is selected more than once: {unvalidated_selections}")
    except FileNotFoundError:
        print("Feature model tree not found, proceeding without constraint checks...")
        pass

    yield Proceed(composer, *features)
