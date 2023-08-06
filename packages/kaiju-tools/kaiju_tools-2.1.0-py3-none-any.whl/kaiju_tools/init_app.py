import logging
import uuid
from typing import cast

from aiohttp.web import Application, run_app

from kaiju_tools.CLI import run_command
from kaiju_tools.config import ConfigLoader, ProjectSettings
from kaiju_tools.services import service_class_registry, ServiceContextManager, App
from kaiju_tools.http.middlewares import error_middleware

__all__ = ('App', 'init_config', 'init_app', 'main')


def init_config(base_config_paths=None, base_env_paths=None, default_env_paths=None) -> (str, ProjectSettings):
    """Configure."""
    if base_config_paths is None:
        base_config_paths = ['./settings/config.yml']
    if base_env_paths is None:
        base_env_paths = ['./settings/env.json']
    if default_env_paths is None:
        default_env_paths = ['./settings/env.local.json']
    logging.basicConfig(level='INFO')
    config_loader = ConfigLoader(
        base_config_paths=base_config_paths, base_env_paths=base_env_paths, default_env_paths=default_env_paths
    )
    command, config = config_loader.configure()
    logging.root.handlers = []
    return command, config


def init_app(settings: ProjectSettings, attrs: dict = None) -> App:
    app = Application(middlewares=[error_middleware], logger=logging.getLogger(settings.main.name), **settings.app)
    app = cast(App, app)
    app.id = uuid.uuid4()
    app.loglevel = settings.main['loglevel']
    for key, value in settings.main.items():
        app[key] = value
        setattr(app, key, value)
    if attrs:
        for key, value in attrs.items():
            app[key] = value
            setattr(app, key, value)
    app.settings = settings
    app.services = services = ServiceContextManager(
        app=app, settings=settings.services, class_registry=service_class_registry, logger=app.logger
    )
    app.cleanup_ctx.append(services.cleanup_context)
    return app


def main(_init_app, **config_settings):
    command, config = init_config(**config_settings)
    app: App = _init_app(config)
    if config.app.debug:
        print('\n-- RUNNING IN DEBUG MODE --\n')
    if command:
        run_command(app, command)
    else:
        run_app(app, access_log=False, **config.run)  # noqa
