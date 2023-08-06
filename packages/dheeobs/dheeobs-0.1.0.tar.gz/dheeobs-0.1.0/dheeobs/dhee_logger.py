import logging
from .dhee_loghandler import DheeLogHandler


class DheeLogger:

    @staticmethod
    def get_logger(**log_params):
        """
        Invokes DheeLogger Handler
        :param log_params: Log Integrations like InfluxDB,Cloudwatch,etc, Log Level , Glue Context
        :return logger object
        """
        logger = logging.getLogger(__name__)
        dhee_logger_handler = DheeLogHandler(**log_params)
        logger.addHandler(dhee_logger_handler)
        logger.setLevel(log_params.get('loglevel'))
        return logger
