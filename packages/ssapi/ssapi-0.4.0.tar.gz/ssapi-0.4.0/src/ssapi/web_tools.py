import collections
import re
import bottle

camel_case_rxp = re.compile(r"^(?P<minor>[a-z]+)(?P<major>[A-Z]{1}\w*)$")


def camel_to_snake_case(data):
    """Convert camelCase to snake_case"""
    new_data = {}
    for key, val in data.items():
        if matched := camel_case_rxp.match(key):
            minor, major = matched.groups()
            new_data[f"{minor}_{major.lower()}"] = val
        else:
            new_data[key] = val

    return new_data


def get_bottle_routes(app: bottle.Bottle) -> dict[str, list[str]]:
    """Convert a bottle instance to a map that describes its active routes"""
    ns: dict = collections.defaultdict(list)
    route: bottle.Route
    for route in app.routes:
        ns[route.rule] += [route.method]
    return ns
