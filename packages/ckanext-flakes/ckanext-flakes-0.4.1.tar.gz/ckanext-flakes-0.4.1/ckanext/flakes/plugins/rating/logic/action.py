from __future__ import annotations

import sqlalchemy as sa

import ckan.plugins.toolkit as tk
from ckan.logic import validate

from ckanext.toolbelt.decorators import Collector

from ckanext.flakes.model import Flake

from . import schema

action, get_actions = Collector("flakes_rating").split()


@action
@validate(schema.average)
def average(context, data_dict):
    tk.check_access("flakes_rating_average", context, data_dict)

    name = _name(data_dict["target_type"], data_dict["target_id"])
    q = (
        context["session"]
        .query(
            sa.func.count(Flake.id).label("count"),
            sa.func.avg(Flake.data["rating"].astext.cast(sa.Float)).label("average"),
        )
        .filter(Flake.name == name)
        .one()
    )

    try:
        own_vote = tk.get_action("flakes_flake_lookup")(context, {"name": name})
        own_rating = own_vote["data"]["rating"]
    except (tk.ObjectNotFound, tk.NotAuthorized):
        own_rating = 0

    return {
        "count": q.count or 0,
        "average": q.average or 0,
        "own": own_rating,
    }


@action
@validate(schema.average_list)
def average_list(context, data_dict):
    tk.check_access("flakes_rating_average_list", context, data_dict)

    names = {
        _name(data_dict["target_type"], id_): id_ for id_ in data_dict["target_ids"]
    }

    q = (
        context["session"]
        .query(
            Flake.name,
            sa.func.count(Flake.id).label("count"),
            sa.func.avg(Flake.data["rating"].astext.cast(sa.Float)).label("average"),
        )
        .group_by(Flake.name)
        .filter(Flake.name.in_(names))
    )

    result = {
        r.name: {
            "count": r.count,
            "average": r.average,
        }
        for r in q
    }

    return {
        id_: result[name] if name in result else {"count": 0, "average": 0}
        for name, id_ in names.items()
    }


@action
@validate(schema.average_package)
def average_package(context, data_dict):
    tk.check_access("flakes_rating_average_package", context, data_dict)
    id_or_name = data_dict.pop("id")
    pkg = tk.get_action("package_show")(dict(context), {"id": id_or_name})
    return tk.get_action("flakes_rating_average")(
        dict(context),
        dict(data_dict, target_type="package", target_id=pkg["id"]),
    )


@action
@validate(schema.rate)
def rate(context, data_dict):
    tk.check_access("flakes_rating_rate", context, data_dict)
    flake = tk.get_action("flakes_flake_override")(
        dict(context),
        {
            "name": _name(data_dict["target_type"], data_dict["target_id"]),
            "data": {"rating": data_dict["rating"]},
            "extras": {
                "flakes_rating": {
                    "type": data_dict["target_type"],
                    "id": data_dict["target_id"],
                }
            },
        },
    )
    return flake


@action
@validate(schema.rate_package)
def rate_package(context, data_dict):
    tk.check_access("flakes_rating_rate_package", context, data_dict)

    id_or_name = data_dict.pop("id")
    pkg = tk.get_action("package_show")(dict(context), {"id": id_or_name})
    return tk.get_action("flakes_rating_rate")(
        dict(context),
        dict(data_dict, target_type="package", target_id=pkg["id"]),
    )


def _name(type_: str, id_: str) -> str:
    return f"ckanext:flakes_rating:rate:{type_}:{id_}"
