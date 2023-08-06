from __future__ import annotations

from ckan.logic.schema import validator_args

from .. import config


def cap_rating(value):
    max_value = config.max_rating()
    min_value = config.min_rating()

    if value > max_value:
        return max_value

    if value < min_value:
        return min_value

    return value


@validator_args
def rate_package(not_missing, int_validator, unicode_safe):
    return {
        "rating": [not_missing, int_validator, cap_rating],
        "id": [not_missing, unicode_safe],
    }


@validator_args
def rate(not_missing, int_validator, unicode_safe):
    return {
        "rating": [not_missing, int_validator, cap_rating],
        "target_id": [not_missing, unicode_safe],
        "target_type": [not_missing, unicode_safe],
    }


@validator_args
def average(not_missing, unicode_safe):
    return {
        "target_id": [not_missing, unicode_safe],
        "target_type": [not_missing, unicode_safe],
    }


@validator_args
def average_list(not_missing, unicode_safe, list_of_strings):
    return {
        "target_ids": [not_missing, list_of_strings],
        "target_type": [not_missing, unicode_safe],
    }


@validator_args
def average_package(not_missing, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
    }
