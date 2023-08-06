from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.authz import is_authorized

from ckanext.toolbelt.decorators import Collector

auth, get_auth_functions = Collector("flakes_feedback").split()


@auth
def feedback_create(context, data_dict):
    return is_authorized("flakes_flake_create", context, data_dict)


@auth
def feedback_update(context, data_dict):
    return is_authorized("flakes_flake_update", context, data_dict)


@auth
def feedback_delete(context, data_dict):
    return is_authorized("flakes_flake_delete", context, data_dict)


@auth
@tk.auth_allow_anonymous_access
def feedback_list(context, data_dict):
    return is_authorized("package_show", context, {"id": data_dict["package_id"]})


@auth
@tk.auth_allow_anonymous_access
def feedback_show(context, data_dict):
    return {"success": True}
