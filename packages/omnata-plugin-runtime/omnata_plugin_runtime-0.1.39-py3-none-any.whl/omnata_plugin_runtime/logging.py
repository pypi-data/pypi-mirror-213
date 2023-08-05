"""
Custom logging functionality for Omnata
"""
import threading
import datetime
import logging
import logging.handlers
from typing import List
import pandas
from snowflake.snowpark import Session
from pydantic import ValidationError

class CustomLogger(logging.getLoggerClass()):
    """
    Custom logger that can handle pydantic validation errors.
    Without this, you get "Object of type ErrorWrapper is not JSON serializable"
    when logging the exception.
    """
    def handleError(self, record):
        if record.exc_info:
            exc_type, exc_value, tb = record.exc_info
            if isinstance(exc_value, ValidationError):
                record.msg = exc_value.errors()
                record.exc_info = (exc_type, None, tb)
        super().handleError(record)


class OmnataPluginLogHandler(logging.handlers.BufferingHandler):
    """
    A logging handler to ship logs back into Omnata Snowflake tables. It uses a combination
    of time and capacity to flush the buffer.
    Additional information about the current sync and run is included, so that logs can be filtered easily.
    """
    def __init__(self,session:Session,
                sync_id:int,
                sync_branch_id:int,
                connection_id:int,
                sync_run_id:int,
                capacity=100,
                duration=5,
            ):
        logging.handlers.BufferingHandler.__init__(self,capacity=capacity)
        self.session = session
        self.duration = duration
        self.timer = None
        self.sync_id = sync_id
        self.sync_branch_id = sync_branch_id
        self.connection_id = connection_id
        self.sync_run_id = sync_run_id
        #formatter = logging.Formatter('%(message)s')
        # add formatter to ch
        #self.setFormatter(formatter)
        self.init_timer()
    
    def register(self,logging_level:str,additional_loggers:List[str] = None):
        """
        Register the handler with the omnata_plugin namespace
        """
        self.setLevel(logging_level)
        logger = logging.getLogger('omnata_plugin')
        logger.addHandler(self)
        if additional_loggers is not None:
            for additional_logger in additional_loggers:
                logger = logging.getLogger(additional_logger)
                logger.addHandler(self)
        
    def unregister(self):
        """
        Removes the handler
        """
        logger = logging.getLogger('omnata_plugin')
        logger.removeHandler(self)
    
    def init_timer(self):
        """
        Initialises the timer to trigger the flush after the duration is reached.
        Will clear any existing timer.
        """
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        self.timer = threading.Timer(self.duration,self.flush)

    def flush(self):
        """
        Send the log records to Snowflake
        """
        if len(self.buffer) > 0:
            try:
                results_df = pandas.DataFrame.from_dict([{
                        'SYNC_ID':self.sync_id,
                        'SYNC_BRANCH_ID':self.sync_branch_id,
                        'CONNECTION_ID':self.connection_id,
                        'SYNC_RUN_ID':self.sync_run_id,
                        'STREAM_NAME':data.__dict__['stream_name'] if 'stream_name' in data.__dict__ else None,
                        'LOG_LEVEL_NAME':data.levelname,
                        'LOG_LEVEL_NO':data.levelno,
                        'LOG_MESSAGE': data.getMessage(),
                        'LOG_STACK_TRACE': data.stack_info,
                        'EVENT_DATETIME': str(datetime.datetime.fromtimestamp(data.created))
                    } for data in self.buffer])
                snowflake_df = self.session.create_dataframe(results_df)
                snowflake_df.write.save_as_table(table_name='DATA.SYNC_RUN_LOG',mode='append',column_order='name')
            except Exception:
                self.handleError(None)  # no particular record
            self.buffer = []
        # restart the timer, regardless of the reason for the flush
        self.init_timer()
