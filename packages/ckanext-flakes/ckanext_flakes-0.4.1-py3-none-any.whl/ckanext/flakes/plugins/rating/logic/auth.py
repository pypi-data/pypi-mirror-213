from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.authz import is_authorized

from ckanext.toolbelt.decorators import Collector

auth, get_auth_functions = Collector("flakes_rating").split()


@auth
@tk.auth_allow_anonymous_access
def average_list(context, data_dict):
    return {"success": True}


@auth
@tk.auth_allow_anonymous_access
def average(context, data_dict):
    return {"success": True}


@auth
def average_package(context, data_dict):
    return is_authorized(
        "flakes_rating_average",
        context,
        dict(data_dict, target_type="package", target_id=data_dict["id"]),
    )


@auth
def rate(context, data_dict):
    return {"success": True}


@auth
def rate_package(context, data_dict):
    return is_authorized(
        "flakes_rating_rate",
        context,
        dict(data_dict, target_type="package", target_id=data_dict["id"]),
    )
