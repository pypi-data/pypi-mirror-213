# this is the file here we are doing some testcase purpose

import logging
  #we are importing our package here
from MT_PY_ErrorLogging.MT_Errorlogging import MT_Logger
 # Create a logger

logger = logging.getLogger("fileerrors:")
logger.setLevel(logging.ERROR)

# Define a custom error handler
class MT_LoggerHandler(logging.Handler):                     # creating a class
    def emit(self, record):                                          # creating a function
        if isinstance(record.exc_info[1],MT_Logger):
            print(f"Custom Error: {record.msg}")
            

# Add the custom error handler to the logger
logger.addHandler(MT_LoggerHandler())      

