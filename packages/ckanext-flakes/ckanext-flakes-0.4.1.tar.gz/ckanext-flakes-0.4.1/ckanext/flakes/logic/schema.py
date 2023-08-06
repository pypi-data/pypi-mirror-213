from __future__ import annotations

from ckan.logic.schema import validator_args


@validator_args
def flake_create(
    not_missing,
    convert_to_json_if_string,
    dict_only,
    ignore,
    ignore_missing,
    unicode_safe,
    flakes_flake_id_exists,
    ignore_empty,
    empty_if_not_sysadmin,
):
    return {
        "name": [ignore_empty, unicode_safe],
        "data": [not_missing, convert_to_json_if_string, dict_only],
        "parent_id": [ignore_missing, flakes_flake_id_exists],
        "extras": [ignore_missing, convert_to_json_if_string, dict_only],
        "author_id": [empty_if_not_sysadmin],
        "__extras": [ignore],
    }


@validator_args
def flake_update(
    not_missing,
    convert_to_json_if_string,
    dict_only,
    ignore,
    ignore_missing,
    unicode_safe,
    flakes_flake_id_exists,
):
    return {
        "id": [not_missing, unicode_safe],
        "data": [not_missing, convert_to_json_if_string, dict_only],
        "parent_id": [ignore_missing, flakes_flake_id_exists],
        "extras": [ignore_missing, convert_to_json_if_string, dict_only],
        "__extras": [ignore],
    }


@validator_args
def flake_override(not_empty, unicode_safe):
    schema = flake_create()
    schema["name"] = [not_empty, unicode_safe]
    return schema


@validator_args
def flake_delete(not_missing, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
    }


@validator_args
def flake_show(not_missing, boolean_validator, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
        "expand": [boolean_validator],
    }


@validator_args
def flake_list(
    boolean_validator,
    convert_to_json_if_string,
    dict_only,
    default,
    empty_if_not_sysadmin,
    ignore_missing,
):
    return {
        "author_id": [empty_if_not_sysadmin],
        "expand": [boolean_validator],
        "extras": [default("{}"), convert_to_json_if_string, dict_only],
    }


@validator_args
def flake_lookup(boolean_validator, not_empty, unicode_safe, empty_if_not_sysadmin):
    return {
        "name": [not_empty, unicode_safe],
        "expand": [boolean_validator],
        "author_id": [empty_if_not_sysadmin],
    }


@validator_args
def flake_validate(boolean_validator, not_missing, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
        "expand": [boolean_validator],
        "schema": [not_missing, unicode_safe],
    }


@validator_args
def data_validate(convert_to_json_if_string, dict_only, not_missing, unicode_safe):
    return {
        "data": [not_missing, convert_to_json_if_string, dict_only],
        "schema": [not_missing, unicode_safe],
    }


@validator_args
def data_example(
    not_missing, convert_to_json_if_string, dict_only, default, unicode_safe
):
    return {
        "factory": [not_missing, unicode_safe],
        "data": [default("{}"), convert_to_json_if_string, dict_only],
    }


@validator_args
def flake_materialize(
    boolean_validator, not_missing, flakes_into_api_action, unicode_safe
):
    return {
        "id": [not_missing, unicode_safe],
        "expand": [boolean_validator],
        "remove": [boolean_validator],
        "action": [not_missing, flakes_into_api_action],
    }


@validator_args
def flake_combine(
    default,
    not_missing,
    json_list_or_string,
    convert_to_json_if_string,
    dict_only,
):
    return {
        "id": [not_missing, json_list_or_string],
        "expand": [default("{}"), convert_to_json_if_string, dict_only],
    }


@validator_args
def flake_merge(boolean_validator, ignore_missing, unicode_safe):
    schema = flake_combine()
    schema["remove"] = [boolean_validator]
    schema["destination"] = [ignore_missing, unicode_safe]
    return schema


@validator_args
def extras_patch(
    not_missing,
    convert_to_json_if_string,
    dict_only,
    unicode_safe,
):
    return {
        "id": [not_missing, unicode_safe],
        "extras": [not_missing, convert_to_json_if_string, dict_only],
    }


@validator_args
def data_patch(
    not_missing,
    convert_to_json_if_string,
    dict_only,
    unicode_safe,
):
    return {
        "id": [not_missing, unicode_safe],
        "data": [not_missing, convert_to_json_if_string, dict_only],
    }
