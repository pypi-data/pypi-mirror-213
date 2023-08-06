import os

from ..config_loader import ConfigLoader


def test_settings(logger):
    test_config = {
        'main': {'name': '[APP_NAME]', 'version': '0.0', 'env': 'dev', 'loglevel': 'DEBUG'},
        'app': {},
        'run': {'host': 'localhost', 'port': 8080},
        'etc': {},
        'services': [{'cls': 'JSONRPCServer', 'settings': {}}],
    }
    custom_env = {'APP_NAME': 'custom_app'}
    configurator = ConfigLoader()
    config = configurator._from_dict(test_config, custom_env)
    logger.debug(config)
    assert config.main.name == 'custom_app'
