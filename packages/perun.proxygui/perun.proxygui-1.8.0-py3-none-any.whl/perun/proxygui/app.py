import os
from typing import Union

import jinja2
import yaml
from cryptojwt.key_jar import init_key_jar
from flask import Flask, request, session
from flask_babel import Babel
from idpyoidc.client.configure import Configuration, RPHConfiguration
from idpyoidc.client.rp_handler import RPHandler
from idpyoidc.configure import create_from_config_file, Base

from perun.proxygui.api.backchannel_logout_api import (
    construct_backchannel_logout_api_blueprint,
)
from perun.proxygui.api.ban_api import construct_ban_api_blueprint
from perun.proxygui.api.kerberos_auth_api import construct_kerberos_auth_api_blueprint
from perun.proxygui.api.consent_api import construct_consent_api
from perun.proxygui.gui.gui import construct_gui_blueprint
from perun.utils.CustomRPHandler import CustomRPHandler

PROXYGUI_CFG = "perun.proxygui.yaml"
BACKCHANNEL_LOGOUT_CFG = "backchannel-logout.yaml"


def get_config_path(filename: str) -> Union[str, FileNotFoundError]:
    etc_filepath = f"./etc/{filename}"
    if os.path.exists(etc_filepath):
        return etc_filepath

    template_filepath = f"./config_templates/{filename}"
    if os.path.exists(template_filepath):
        return template_filepath

    raise FileNotFoundError("No viable config file was found.")


def get_config(filename=PROXYGUI_CFG):
    cfg_path = get_config_path(filename)
    with open(
        cfg_path,
        "r",
        encoding="utf8",
    ) as ymlfile:
        loaded_cfg = yaml.safe_load(ymlfile)

    return loaded_cfg


def init_oidc_rp_handler() -> RPHandler:
    rp_conf = get_rp_config()

    key_jar = init_key_jar(**rp_conf.key_conf)
    key_jar.httpc_params = rp_conf.httpc_params

    public_path = rp_conf.key_conf["public_path"]
    norm_public_path = os.path.normpath(public_path)

    rph = CustomRPHandler(
        keyjar=key_jar,
        jwks_path=norm_public_path,
    )
    return rph


def get_rp_config() -> Base:
    # the entire filepath is required, not just the filename
    cfg_path = get_config_path(BACKCHANNEL_LOGOUT_CFG)
    return create_from_config_file(
        Configuration,
        entity_conf=[{"class": RPHConfiguration, "attr": "rp"}],
        filename=cfg_path,
    )


def get_flask_app(cfg):
    if "css_framework" not in cfg:
        cfg["css_framework"] = "bootstrap"

    if "bootstrap_color" not in cfg:
        cfg["bootstrap_color"] = "primary"

    def get_locale():
        if request.args.get("lang"):
            session["lang"] = request.args.get("lang")
        return session.get("lang", "en")

    app = Flask(__name__)
    app.jinja_loader = jinja2.FileSystemLoader("perun/proxygui/gui/templates")
    Babel(app, locale_selector=get_locale)

    app.secret_key = cfg["secret_key"]

    app.config["SERVER_NAME"] = cfg["host"]["server_name"]

    @app.context_processor
    def inject_conf_var():
        return dict(cfg=cfg, lang=get_locale())

    # Register GUI component
    app.register_blueprint(construct_gui_blueprint(cfg))

    # Register API endpoints
    app.register_blueprint(construct_ban_api_blueprint(cfg))
    app.register_blueprint(construct_kerberos_auth_api_blueprint(cfg))
    # to avoid breaking change
    if "consent" in cfg:
        app.register_blueprint(construct_consent_api(cfg))

    logout_cfg = get_config(filename=BACKCHANNEL_LOGOUT_CFG)
    if logout_cfg:
        app.register_blueprint(
            construct_backchannel_logout_api_blueprint(cfg, logout_cfg)
        )

        # Initialize the oidc_provider after views to be able to set correct urls
        app.rp_handler = init_oidc_rp_handler()

    return app


# for uWSGI
def get_app(*args):
    cfg = get_config()
    app = get_flask_app(cfg)
    return app(*args)


if __name__ == "__main__":
    cfg = get_config()
    app = get_flask_app(cfg)
    app.run(
        host=cfg["host"]["ip-address"],
        port=cfg["host"]["port"],
        debug=cfg["host"]["debug"],
    )
