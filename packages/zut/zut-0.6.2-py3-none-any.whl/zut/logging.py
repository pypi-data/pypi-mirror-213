from __future__ import annotations
import logging, logging.config, atexit, os
from .colors import Colors


def configure_logging(level: int|str = None, nocount: bool = False, config: dict = None):
    merged = dict(DEFAULT_LOGGING_DICTCONFIG)

    # Merge given config with default config
    if config:
        for prop, data in config.items():
            if isinstance(data, dict) and prop in merged and isinstance(merged[prop], dict):
                for key, value in data.items():
                    if value is None:
                        merged[prop].pop(key, None)
                    else:
                        merged[prop][key] = value
            else:
                merged[prop] = data

    # Set root level if missing or if explicitely provided     
    if level is not None or ('root' in merged and not 'level' in merged['root']):
        if level is None:
            level = os.environ.get('LOG_LEVEL', '').upper() or 'INFO'
        
        if isinstance(level, int):
            level = logging.getLevelName(level)

        merged['root']['level'] = level

    # Remove count handler
    if nocount:
        if 'root' in merged and 'handlers' in merged['root']:
            merged['root']['handlers'].pop('count', None)

        if 'loggers' in merged:
            for _, loggerconfig in merged['loggers'].items():
                if 'handlers' in loggerconfig:
                    loggerconfig['handlers'].pop('count', None)
    
    logging.config.dictConfig(merged)


class ColoredRecord:
    LEVELCOLORS = {
        logging.DEBUG:     Colors.GRAY,
        logging.INFO:      '',
        logging.WARNING:   Colors.YELLOW,
        logging.ERROR:     Colors.RED,
        logging.CRITICAL:  Colors.BOLD_RED,
    }

    def __init__(self, record: logging.LogRecord):
        # The internal dict is used by Python logging library when formatting the message.
        # (inspired from library "colorlog").
        self.__dict__.update(record.__dict__)
        self.__dict__.update({
            'levelcolor': self.LEVELCOLORS.get(record.levelno, ''),
            'red': Colors.RED,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'cyan': Colors.CYAN,
            'gray': Colors.GRAY,
            'bold_red': Colors.BOLD_RED,
            'reset': Colors.RESET,
        })


class ColoredFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        wrapper = ColoredRecord(record)
        message = super().formatMessage(wrapper)
        return message


class CountHandler(logging.Handler):
    def __init__(self, level=logging.WARNING):
        self.counts: dict[int, int] = {}
        atexit.register(self.print_counts)
        super().__init__(level=level)

    def print_counts(self):
        msg = ""

        levelnos = sorted(self.counts.keys(), reverse=True)
        for levelno in levelnos:
            levelname = logging.getLevelName(levelno)
            levelcolor = ColoredRecord.LEVELCOLORS.get(levelno, '')
            msg += (", " if msg else "") + f"{levelcolor}%s{Colors.RESET}" % levelname + ": %d" % self.counts[levelno]

        if msg:
            print("Logged " + msg)

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            if not record.levelno in self.counts:
                self.counts[record.levelno] = 1
            else:
                self.counts[record.levelno] += 1


DEFAULT_LOGGING_DICTCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'color': {
            '()': ColoredFormatter.__module__ + '.' + ColoredFormatter.__qualname__,
            'format': '%(levelcolor)s%(levelname)s%(reset)s %(gray)s[%(name)s]%(reset)s %(levelcolor)s%(message)s%(reset)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
        'count': {
            'class': CountHandler.__module__ + '.' + CountHandler.__qualname__,
            'level': 'WARNING',
        },
    },
    'root': {
        'handlers': ['console', 'count'],
        'level': os.environ.get('LOG_LEVEL', '').upper() or 'INFO',
    },
    'loggers': {
        'django': { 'level': os.environ.get('DJANGO_LOG_LEVEL', '').upper() or 'INFO', 'propagate': False },
        'smbprotocol': { 'level': 'WARNING' },
    },
}
