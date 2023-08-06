from __future__ import annotations
from typing import Any

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.logic import validate

from ckanext.toolbelt.decorators import Collector

from . import schema

action, get_actions = Collector("flakes_feedback").split()


@action
@validate(schema.feedback_create)
def feedback_create(context, data_dict):
    tk.check_access("flakes_feedback_feedback_create", context, data_dict)

    pkg = model.Package.get(data_dict["package_id"])
    if not pkg:
        raise tk.ObjectNotFound("Package not found")

    secondary_key: str | None = data_dict["secondary_key"]

    payload: dict[str, Any] = {
        "data": data_dict["data"],
        "extras": {
            "flakes_feedback": {
                "type": "package",
                "id": pkg.id,
                "secondary_key": secondary_key,
            }
        },
    }

    try:
        existing = tk.get_action("flakes_feedback_feedback_lookup")(
            {},
            {
                "package_id": pkg.id,
                "secondary_key": secondary_key,
            },
        )
    except tk.ObjectNotFound:
        payload["name"] = _name(pkg.id, secondary_key)
        action = "flakes_flake_create"
    else:
        if tk.asbool(tk.config.get("ckanext.flakes_feedback.allow_overrides")):
            payload["id"] = existing["id"]
            action = "flakes_flake_update"
        else:
            raise tk.ValidationError({"name": ["Already exists"]})

    flake = tk.get_action(action)(context, payload,)

    return flake


@action
@validate(schema.feedback_update)
def feedback_update(context, data_dict):
    tk.check_access("flakes_feedback_feedback_update", context, data_dict)
    secondary_key: str | None = data_dict["secondary_key"]

    try:
        flake = tk.get_action("flakes_flake_update")(context, data_dict)
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    extras = flake["extras"]["flakes_feedback"]
    if extras.get("secondary_key") != secondary_key:
        old_id = flake["id"]
        flake = tk.get_action("flakes_flake_override")(
            context,
            {
                "name": _name(extras["id"], secondary_key),
                "data": flake["data"],
                "extras": {
                    "flakes_feedback": dict(extras, secondary_key=secondary_key)
                },
            },
        )

        tk.get_action("flakes_feedback_feedback_delete")(context, {"id": old_id})

    return flake


@action
@validate(schema.feedback_delete)
def feedback_delete(context, data_dict):
    tk.check_access("flakes_feedback_feedback_delete", context, data_dict)

    try:
        flake = tk.get_action("flakes_flake_delete")(context, {"id": data_dict["id"]})
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


@action
@tk.side_effect_free
@validate(schema.feedback_list)
def feedback_list(context, data_dict):
    tk.check_access("flakes_feedback_feedback_list", context, data_dict)

    pkg = model.Package.get(data_dict["package_id"])

    flakes = tk.get_action("flakes_flake_list")(
        dict(context, ignore_auth=True),
        {
            "author_id": None,
            "extras": {"flakes_feedback": {"type": "package", "id": pkg.id}},
        },
    )

    return flakes


@action
@tk.side_effect_free
@validate(schema.feedback_show)
def feedback_show(context, data_dict):
    tk.check_access("flakes_feedback_feedback_show", context, data_dict)

    try:
        flake = tk.get_action("flakes_flake_show")(
            dict(context, ignore_auth=True), {"id": data_dict["id"]}
        )
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


@action
@tk.side_effect_free
@validate(schema.feedback_lookup)
def feedback_lookup(context, data_dict):
    tk.check_access("flakes_feedback_feedback_list", context, data_dict)
    secondary_key: str | None = data_dict["secondary_key"]

    pkg = model.Package.get(data_dict["package_id"])
    if not pkg:
        raise tk.ObjectNotFound("Package not found")

    try:
        flake = tk.get_action("flakes_flake_lookup")(context, {"name": _name(pkg.id, secondary_key)})
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


def _name(id_: str, secondary_key: str | None) -> str:
    name = f"ckanext:flakes_feedback:feedback:package:{id_}"
    if secondary_key:
        name = f"{name}:{secondary_key}"

    return name
