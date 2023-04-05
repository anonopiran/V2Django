import logging
import typing
from abc import abstractmethod

from django.core.management.base import BaseCommand

if typing.TYPE_CHECKING:
    _BaseModel = BaseCommand
else:
    _BaseModel = object


class CommandLogFormatter(logging.Formatter):
    RECORD_MAP = {
        logging.ERROR: "ERROR",
        logging.WARN: "WARNING",
        logging.INFO: "SUCCESS",
        logging.DEBUG: "NOTICE",
    }
    cmd_style = None

    def set_console_style(self, style):
        self.cmd_style = style

    def format(self, record: logging.LogRecord) -> str:
        rec = super(CommandLogFormatter, self).format(record=record)
        rec = getattr(self.cmd_style, self.RECORD_MAP[record.levelno])(rec)
        return rec


class LoggingCommandMixin(_BaseModel):
    logger: logging.Logger

    def setup_logger(self, verb: int):
        ll = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
        console = logging.StreamHandler(stream=self.stderr)
        fmt = CommandLogFormatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        fmt.set_console_style(self.style)
        console.setFormatter(fmt)
        self.logger = logging.getLogger(self.logger_name)
        self.logger.addHandler(console)
        self.logger.setLevel(ll[verb])

    def execute(self, *args, **options):
        self.setup_logger(options["verbosity"])
        return super().execute(*args, **options)

    def handle(self, *args, **options):
        super(LoggingCommandMixin, self).handle(*args, **options)

    @property
    @abstractmethod
    def logger_name(self) -> str:
        return ""
