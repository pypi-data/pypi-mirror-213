from __future__ import annotations

import ckan.plugins.toolkit as tk

from ckanext.toolbelt.decorators import Collector

from . import config

helper, get_helpers = Collector("flakes_rating").split()


@helper
def get_rating(type_: str, id_: str) -> dict[str, int]:
    return tk.get_action("flakes_rating_average")(
        {}, {"target_id": id_, "target_type": type_}
    )


@helper
def get_rating_list(type_: str, ids: list[str]) -> dict[str, int]:
    return tk.get_action("flakes_rating_average_list")(
        {}, {"target_ids": ids, "target_type": type_}
    )


@helper
def show_package_widget() -> bool:
    return config.show_package_widget()
