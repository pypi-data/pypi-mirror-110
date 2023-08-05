import logging
import pytz
import socket

from datetime import datetime


class LokiFormatter(logging.Formatter, object):
    """
    Python logging formatter for Loki.
    """
    asctime_search = '%(asctime)'
    tz = 'UTC'
    source = 'Loki'
    src_host = 'localhost'

    def __init__(self, fmt: str, dfmt: str, style, fqdn=False):
        super(LokiFormatter, self).__init__()
        self.fmt = fmt
        self.dfmt = dfmt
        self.style = style
        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    def format_timestamp(self, time):
        return datetime.fromtimestamp(time, tz=pytz.timezone(self.tz))

    def usesTime(self):
        return self.fmt.find(self.asctime_search) >= 0

    def formatMessage(self, record):
        try:
            return self.fmt % record.__dict__
        except KeyError as e:
            raise ValueError('Formatting field not found in record: %s' % e)

    def format(self, record):
        # Create message dict
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.dfmt)
        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        message = {
            'streams': [
                {
                    'labels': f'{{source="{self.source}",job="{record.name}",host="{self.src_host}"}}',
                    'entries': [
                        {
                            'ts': self.format_timestamp(record.created).isoformat('T'),
                            'line': s,
                        }
                    ]
                }
            ]
        }

        return message
