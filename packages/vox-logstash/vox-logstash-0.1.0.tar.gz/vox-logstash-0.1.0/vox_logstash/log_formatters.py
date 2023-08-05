import importlib
import json
import logging
import os
from logging import LogRecord
from datetime import datetime
import socket


if importlib.find_loader('django.conf'):
    from django.conf import settings

    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    organization = settings.ORGANIZATION
else:
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')
    organization = os.getenv('ORGANIZATION')


default_record = {
    "ecs.version": "1.6",
    "transaction.id": "UUID",
    "service.version": app_version,
    "organization.name": organization,
    "log.level": "INFO",
    "appName": app_name,
    "@version": 1,
    "source.ip": socket.gethostname(),
}


class LogstashFormatter(logging.Formatter):
    def format(self, record: LogRecord):
        json_record = {
            **default_record,
            "log.logger": record.name,
            "message": record.getMessage(),
            "@timestamp": self.format_timestamp(record.created),
            "log.level": record.levelname,
        }

        return json.dumps(json_record) + "\\r"

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

