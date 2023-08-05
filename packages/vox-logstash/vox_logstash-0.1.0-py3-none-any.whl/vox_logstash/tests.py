from unittest import TestCase
from unittest.mock import patch, MagicMock


class LoggingTest(TestCase):

    @patch('logging.handlers.socket')
    def test_should_send_logs_to_socket(self, socket):
        import logging
        from vox_logstash.log_formatters import LogstashFormatter
        from vox_logstash.log_handlers import LogstashHandler

        class AssertCalledWithMatch(bytes):
            def __eq__(self, other):
                return self in other

        connection = MagicMock()
        socket.create_connection.return_value = connection

        logger = logging.getLogger('testing')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(handler := LogstashHandler('localhost', '1337'))
        handler.setFormatter(LogstashFormatter())

        logger.info('lets debug')

        connection.sendall.assert_called_with(AssertCalledWithMatch(b'"message": "lets debug"'))
