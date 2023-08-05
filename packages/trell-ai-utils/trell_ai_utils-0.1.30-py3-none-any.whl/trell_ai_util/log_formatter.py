import json
import logging
from datetime import datetime


class TrellAILogFormatter(logging.Formatter):
    """Log Formatter class for trell ai usage"""

    __date_format = '%d/%b/%Y:%H:%M:%S %Z'

    @staticmethod
    def apply():
        """
        Start logging in json format.
        :return:
        """
        trell_ai_json_log_format = {
            'ts': '%(asctime)s',
            'level': '%(levelname)s',
            'location': '%(pathname)s:%(lineno)d',
            'msg': '%(message)s'
        }
        log_format = json.dumps(trell_ai_json_log_format)
        logging.basicConfig(format=log_format, level=logging.DEBUG, datefmt=TrellAILogFormatter.__date_format)
        if len(logging.root.handlers) > 0:
            logging.root.handlers[0].setFormatter(TrellAILogFormatter(fmt=log_format,
                                                                      datefmt=TrellAILogFormatter.__date_format))

    def formatException(self, execution_info):
        """
        Handle logging in case of exceptions.
        :param execution_info:
        :return:
        """
        stacktrace = super(TrellAILogFormatter, self).formatException(execution_info)
        record = {
            'message': stacktrace,
            'levelname': 'EXCEPTION',
            'pathname': 'stacktrace in msg',
            'lineno': -1
        }
        try:
            record['asctime'] = datetime.now().strftime(TrellAILogFormatter.__date_format)
            return self._fmt % record
        except Exception as err:
            return repr(stacktrace)
