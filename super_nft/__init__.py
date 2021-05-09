# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, g
from flask_cors import CORS
from super_nft.blueprints.public.public import public_bp
from super_nft.blueprints.user.user import user_bp
from super_nft.blueprints.admin.admin import admin_bp
from super_nft.blueprints.syncer.syncer import syncer_bp

from super_nft.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
    bootstrap,
)


def create_app(config_object="super_nft.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask('super_nft')
    with app.app_context():
        CORS(app)
        app.config.from_object(config_object)
        configure_models()
        register_extensions(app)
        register_blueprints(app)
        register_errorhandlers(app)
        register_shellcontext(app)
        # register_commands(app)
        configure_logger(app)
        g.index_add_counter = 0
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    bootstrap.init_app(app)


def configure_models():
    import super_nft.blueprints.public.models
    import super_nft.blueprints.syncer.models

def register_blueprints(app):
    """Register Flask blueprints."""
    
    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(syncer_bp, url_prefix='/syncer')

def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("errors/{}.html".format(str(error_code))), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


# def register_commands(app):
#     """Register Click commands."""
#     # from fisco_bcos_toolbox.commands import * 
#     app.cli.add_command(commands.test)
#     app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
