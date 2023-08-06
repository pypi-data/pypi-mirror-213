from bottle import get, post, request, response, default_app, Bottle

from ssapi.entities import Sale
from ssapi.env import get_env_database
from ssapi.types import Undefined
from ssapi.web_tools import get_bottle_routes
from ssapi.web_decorators import accepts_json, returns_json, handles_db_errors
from ast import literal_eval


def get_application() -> Bottle:
    """Get the WSGI application"""
    return default_app()


@get("/")
@returns_json
def get_root():
    app = get_application()
    routes = get_bottle_routes(app)
    del routes["/"]
    return routes


@get("/shops")
@returns_json
def get_shops():
    return list(get_env_database().get_shops())


@get("/sales")
@returns_json
def get_sales():
    query = request.query.decode()
    start = query.get("start", None)
    end = query.get("end", None)
    shop = query.get("shop", None)
    is_discounted = query.get("isDiscounted", None)
    return [
        dict(sale.as_map())
        for sale in get_env_database().get_sales(
            date_start=start,
            date_end=end,
            shop=shop,
            is_discounted=(
                Undefined() if is_discounted is None else literal_eval(
                    is_discounted
                )
            )
        )
    ]


@get("/sales/<id:int>")
@returns_json
def get_sale(id: int) -> dict:
    sale = get_env_database().get_sale(id)
    if sale:
        return dict(sale.as_map())
    else:
        response.status = 404
        return {"outcome": f"not found: {request.path}"}


@post("/sales")
@accepts_json
@returns_json
@handles_db_errors
def post_sales():
    try:
        new_sale = Sale(**request.adapted_json)
    except TypeError as exc:
        response.status = 400
        outcome = (
            f"creation failed: "
            f"invalid parameters for type 'sale': "
            f"{request.json} {exc}"
        )
    else:
        db = get_env_database()
        count = db.add_sales(new_sale)
        outcome = f"creation ({count}) succeeded in database at: {db.name}"

    return {"outcome": outcome}

@get("/products")
@returns_json
def get_products():
    return tuple(get_env_database().get_products())


@post("/drop")
@accepts_json
@returns_json
def drop():
    # FIXME: add security
    db = get_env_database()
    db.drop()
    db.open()
    return {"outcome": f"Database dropped at: {db.name}"}
