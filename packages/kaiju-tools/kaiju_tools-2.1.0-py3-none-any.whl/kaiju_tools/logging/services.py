import logging
from typing import TypedDict, Iterable, Union, List

from kaiju_tools.services import ContextableService
from kaiju_tools.logging.types import HANDLERS, FORMATTERS

__all__ = ['LoggingService']


class _HandlerSettings(TypedDict, total=False):
    cls: str
    name: str
    formatter: str
    enabled: bool
    settings: dict
    formatter_settings: dict
    loglevel: str


class _LoggerSettings(TypedDict, total=False):
    name: str
    enabled: bool
    handlers: Union[List[str], bool]
    loglevel: str


class LoggingService(ContextableService):
    """Log handler and formatter configuration for application loggers."""

    handler_classes = HANDLERS
    formatter_classes = FORMATTERS

    def __init__(
        self,
        *args,
        loggers: Iterable[_LoggerSettings] = None,
        handlers: Iterable[_HandlerSettings] = None,
        loglevel: str = None,
        **kws,
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self.loggers = loggers
        self.handlers = handlers
        self.loglevel = loglevel if loglevel else getattr(self.app, 'loglevel', 'INFO')
        self.clear_root_logger()
        _handlers = {handler['name']: handler for handler in self.handlers} if self.handlers else {}
        _loggers = {logger['name']: logger for logger in self.loggers} if self.loggers else {}
        app_logger_name = self.app.logger.name
        if app_logger_name not in _loggers:
            _loggers[app_logger_name] = _LoggerSettings(name=app_logger_name, enabled=True, handlers=True)
        self._handlers = {  # noqa
            name: self._init_handler(handler) for name, handler in _handlers.items() if handler.get('enabled')
        }
        self._loggers = {  # noqa
            name: self._init_logger(logger) for name, logger in _loggers.items() if logger.get('enabled')
        }

    @staticmethod
    def clear_root_logger():
        """Remove all existing handlers from the root logger."""
        logger = logging.getLogger()
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)

    def _init_handler(self, handler: _HandlerSettings) -> logging.Handler:
        """Initialize a handler with handler settings."""
        if isinstance(handler['cls'], str):
            handler['cls'] = self.handler_classes[handler['cls']]
        if isinstance(handler['formatter'], str):
            handler['formatter'] = self.formatter_classes[handler['formatter']]
        _handler = handler['cls'](self.app, **handler.get('settings', {}))
        formatter = handler['formatter'](**handler.get('formatter_settings', {}))
        _handler.setFormatter(formatter)
        loglevel = handler.get('loglevel', self.loglevel)
        _handler.setLevel(loglevel)
        return _handler

    def _init_logger(self, logger: _LoggerSettings) -> logging.Logger:
        """Initialize a logger with logger settings."""
        _logger = logging.getLogger(logger['name'])
        _logger.handlers = []
        if logger['handlers'] is True:
            _handlers = self._handlers.values()
        else:
            _handlers = (self._handlers[name] for name in logger['handlers'])
        for handler in _handlers:
            _logger.addHandler(handler)
        loglevel = logger.get('loglevel', self.loglevel)
        _logger.setLevel(loglevel)
        return _logger
