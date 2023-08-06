from __future__ import annotations

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import helpers
from .logic import action, auth

try:
    config_declarations = tk.blanket.config_declarations
except AttributeError:

    def config_declarations(cls):
        return cls


@config_declarations
class FlakesRatingPlugin(p.SingletonPlugin):
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers)

    def get_actions(self):
        return action.get_actions()

    def get_auth_functions(self):
        return auth.get_auth_functions()

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("assets", "flakes_rating")

    def get_helpers(self):
        return helpers.get_helpers()
