# sample package on Logging Error 


# Project Title

Mouritech

package name : Mouritech_LoggingErrorMT_PY_ErrorLogging

Creating custom package for Logging Errorin python.
This is the project ,Whenever you need to check the level of Errors in a code . 



## Technologie 
Python



## Installation

Install my-project with Python
Install  MT_PY_ErrorLogging
```bash
  pip install   MT_PY_ErrorLogging
  cd   MT_PY_ErrorLogging
```

(globally)
pip install MT_PY_ErrorLogging

## Steps 




pip install  MT_PY_ErrorLogging

(or)

pip install MT_PY_ErrorLogging

from MT_PY_ErrorLogging.MT_Errorlogging import MT_Logger
from MT_ErrorLogging import MT_Logger

MT_Logger(

)





## Authors

- [@Sirisha](https://www.github.com/octokatherine)



## Used By

This project is used by the following Cases:

- Projects :-Logging Error is one of the debugging tool which is used to track the log levels of the cod e(error levels of the code )
- 




# Receiver Example :

pip install  MT_PY_ErrorLogging


from MT_PY_ErrorLogging.MT_Errorlogging import MT_Logger
from MT_Errorlogging import MT_PY_ErrorLogging

MT_PY_ErrorLogging(

)


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
        if isinstance(record.exc_info[1], LoggerDemoConsole):
            print(f"Custom Error: {record.msg}")
            

# Add the custom error handler to the logger
logger.addHandler(MT_LoggerHandler())      


# Output:

06/01/2023 05:31:15PM - LoggerDemoConsoleINFO: info message
06/01/2023 05:31:15PM - LoggerDemoConsoleWARNING: warn message
06/01/2023 05:31:15PM - LoggerDemoConsoleERROR: error message
06/01/2023 05:31:15PM - LoggerDemoConsoleCRITICAL: critical message