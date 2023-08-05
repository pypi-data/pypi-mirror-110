from logging import LogRecord
from logging.handlers import SocketHandler


class LogstashHandler(SocketHandler):
    def makePickle(self, record: LogRecord) -> bytes:
        return bytes(self.formatter.format(record), 'utf-8') + b'\n'
