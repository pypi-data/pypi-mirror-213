from datetime import datetime, timezone
import logging
import requests
import os
import sys


class DheeLogHandler(logging.Handler):

    def __init__(self, **logparams) -> None:
        super().__init__()
        self.log_integration_list = logparams.get('log_integration_list')
        if logparams.get('glueContext') is not None:
            self.glueContext = logparams.get('glueContext')

    def emit(self, record: logging.LogRecord) -> None:
        """
        Inherited Method invoked for all log levels
        :param record: logging record object
        :return:
        """
        try:

            if self.log_integration_list is not None:
                if "influxdb" in self.log_integration_list:
                    self.post_logs_to_influxdb(record)

                if "cloudwatch" in self.log_integration_list:
                    self.post_logs_to_cloudwatch(record)

        except Exception:
            self.handleError(record)

    def post_logs_to_influxdb(self, record: logging.LogRecord):
        """
        Post Logs to InfluxDB Server
        :param record: logging record object
        :return:
        """
        message = self.format(record)
        level = record.levelname
        log_location = record.filename + "::" + record.funcName + "::" + str(record.lineno)  # Eg., dhee_loghandler.py::post_logs_to_influxdb::45

        if hasattr(self,'glueContext') and self.glueContext is not None:
            args =  self.get_commandline_args()
        else:
            args = {'INFLUXDB_URL': os.getenv('INFLUXDB_URL'), 'INFLUXDB_ORG': os.getenv('INFLUXDB_ORG'),
                    'INFLUXDB_BUCKET': os.getenv('INFLUXDB_BUCKET'), 'INFLUXDB_TOKEN': os.getenv('INFLUXDB_TOKEN'),
                    'MEASUREMENT_NAME': os.getenv('MEASUREMENT_NAME')}

        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000000000)
        url = args['INFLUXDB_URL'] + "/api/v2/write?org=" + args['INFLUXDB_ORG'] + "&bucket=" + args[
            'INFLUXDB_BUCKET'] + "&precision=ns"
        headers = {
            'Authorization': 'Token ' + args['INFLUXDB_TOKEN'],
            'Content-Type': 'text/plain; charset=utf-8'
        }
        payload = args['MEASUREMENT_NAME'] + ",level=" + level + " message=\"" + message + "\",location=\"" + log_location +"\" " + str(timestamp)
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()

    def post_logs_to_cloudwatch(self, record: logging.LogRecord):
        """
        Post Logs to Cloudwatch from AWS Glue Job
        :param record: logging record object
        :return:
        """
        if hasattr(self,'glueContext') and self.glueContext is not None and "get_logger" in dir(self.glueContext):
            glue_logger = self.glueContext.get_logger()
            message = self.format(record)
            if record.levelname == "WARNING":
                glue_logger.warn(message)
            elif record.levelname == "ERROR":
                glue_logger.error(message)
            elif record.levelname == "DEBUG":
                glue_logger.debug(message)
            else:
                glue_logger.info(message)


    def get_commandline_args(self):
        """
        To get Command Line arguments to setup integration endpoint configuration
        :return:
        """
        arguments_dict = {}
        for index, argument in enumerate(sys.argv):
            if argument.startswith("--"):
                arguments_dict[argument[2:]] = sys.argv[index + 1]
        return arguments_dict

