from __future__ import annotations

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import views
from .logic import action, auth

try:
    config_declarations = tk.blanket.config_declarations
except AttributeError:

    def config_declarations(cls):
        return cls


@config_declarations
class FlakesFeedbackPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IBlueprint, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("assets", "flakes_feedback")

    def get_blueprint(self):
        return views.get_blueprints()

    def get_helpers(self):
        return {
            "flakes_feedback_enable_views": enable_views,
        }

    def get_actions(self):
        return action.get_actions()

    def get_auth_functions(self):
        return auth.get_auth_functions()


def enable_views() -> bool:
    return tk.asbool(tk.config.get("ckanext.flakes_feedback.enable_views", False))
