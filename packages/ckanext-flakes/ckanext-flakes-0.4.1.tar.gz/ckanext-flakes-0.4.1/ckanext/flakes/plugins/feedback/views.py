from __future__ import annotations

from typing import Any

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
from ckan.logic import parse_params

bp = Blueprint("flakes_feedback", __name__)


def get_blueprints():
    return [bp]


def _pkg(id_: str):
    try:
        return tk.get_action("package_show")({}, {"id": id_})
    except (tk.ObjectNotFound, tk.NotAuthorized):
        return tk.abort(404)


def _existing(id_: str, secondary_key: str | None):
    try:
        return tk.get_action("flakes_feedback_feedback_lookup")(
            {},
            {
                "package_id": id_,
                "secondary_key": secondary_key,
            },
        )
    except (tk.NotAuthorized, tk.ObjectNotFound):
        pass


@bp.route("/<package_type>/<id>/feedback")
@bp.route("/dataset/<id>/feedback", defaults={"package_type": "dataset"})
def index(package_type: str, id: str) -> str:
    try:
        tk.check_access("flakes_feedback_feedback_list", {}, {"package_id": id})
        pkg_dict = tk.get_action("package_show")({}, {"id": id})
        feedbacks = tk.get_action("flakes_feedback_feedback_list")(
            {}, {"package_id": id}
        )
    except (tk.ObjectNotFound, tk.NotAuthorized):
        return tk.abort(404)

    data = {
        "pkg_dict": pkg_dict,
        "feedbacks": feedbacks,
    }

    return tk.render("flakes_feedback/index.html", data)


class PostView(MethodView):
    def _render(self, data: dict[str, Any]) -> str:
        return tk.render("flakes_feedback/post.html", data)

    def post(self, package_type: str, id: str):
        pkg_dict = _pkg(id)
        data = parse_params(tk.request.form)
        secondary_key = tk.request.args.get("secondary_key")
        feedback = _existing(id, secondary_key)

        if feedback:
            action = "flakes_feedback_feedback_update"
            pk = {"id": feedback["id"]}
        else:
            action = "flakes_feedback_feedback_create"
            pk = {"package_id": id}

        try:
            feedback = tk.get_action(action)(
                {},
                dict(pk, data=data, secondary_key=secondary_key),
            )
        except tk.NotAuthorized:
            return tk.abort(403)
        except tk.ValidationError as e:
            return self._render(
                {
                    "pkg_dict": pkg_dict,
                    "error_summary": e.error_summary,
                    "errors": e.error_dict,
                    "data": data,
                    "feedback_id": feedback["id"] if feedback else "",
                }
            )

        return tk.redirect_to("flakes_feedback.index", id=id, package_type=package_type)

    def get(self, package_type: str, id: str):
        pkg_dict = _pkg(id)
        secondary_key = tk.request.args.get("secondary_key")
        feedback = _existing(id, secondary_key)

        data = {
            "pkg_dict": pkg_dict,
            "error_summary": {},
            "errors": {},
            "data": feedback["data"] if feedback else {},
            "feedback_id": feedback["id"] if feedback else "",
        }

        return self._render(data)


class DeleteView(MethodView):
    def _render(self, data: dict[str, Any]) -> str:
        return tk.render("flakes_feedback/delete.html", data)

    def post(self, package_type: str, id: str, feedback_id: str):
        try:
            tk.get_action("flakes_feedback_feedback_delete")(
                {},
                {
                    "id": feedback_id,
                },
            )
        except tk.NotAuthorized:
            return tk.abort(403)
        except tk.ObjectNotFound:
            return tk.abort(404)

        return tk.redirect_to("flakes_feedback.index", id=id, package_type=package_type)

    def get(self, package_type: str, id: str, feedback_id: str):
        pkg_dict = _pkg(id)

        data = {
            "pkg_dict": pkg_dict,
        }

        return self._render(data)


post_view = PostView.as_view("post")
delete_view = DeleteView.as_view("delete")

bp.add_url_rule(
    "/dataset/<id>/feedback/post",
    defaults={"package_type": "dataset"},
    view_func=post_view,
)
bp.add_url_rule("/<package_type>/<id>/feedback/post", view_func=post_view)
bp.add_url_rule(
    "/dataset/<id>/feedback/delete/<feedback_id>",
    defaults={"package_type": "dataset"},
    view_func=delete_view,
)
bp.add_url_rule(
    "/<package_type>/<id>/feedback/delete/<feedback_id>", view_func=delete_view
)
