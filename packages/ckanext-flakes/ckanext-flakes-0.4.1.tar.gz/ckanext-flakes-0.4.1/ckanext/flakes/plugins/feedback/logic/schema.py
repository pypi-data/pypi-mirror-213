from ckan.logic.schema import validator_args


@validator_args
def feedback_create(not_missing, unicode_safe, default):
    return {
        "package_id": [not_missing, unicode_safe],
        "data": [not_missing],
        "secondary_key": [default(None)],
    }


@validator_args
def feedback_update(not_missing, unicode_safe, default):
    return {
        "id": [not_missing, unicode_safe],
        "data": [not_missing],
        "secondary_key": [default(None)],
    }


@validator_args
def feedback_delete(not_missing, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
    }


@validator_args
def feedback_list(not_missing, unicode_safe):
    return {
        "package_id": [not_missing, unicode_safe],
    }


@validator_args
def feedback_show(not_missing, unicode_safe):
    return {
        "id": [not_missing, unicode_safe],
    }


@validator_args
def feedback_lookup(not_missing, unicode_safe, default):
    return {
        "package_id": [not_missing, unicode_safe],
        "secondary_key": [default(None)],
    }
