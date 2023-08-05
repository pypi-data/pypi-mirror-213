import logging  # imported  the library   (default library )


# create a class for our package 
class MT_Logger:
   def testLog(self):                   #create a function 
       #logger = logging.getLogger('demologger')

       #setting logger levels 
       logger = logging.getLogger(MT_Logger.__name__)
       logger.setLevel(logging.INFO)   #the level is set to INFO level

       #using filehandler (it defines the status of the each meassage in a logger )
       fileHandler = logging.FileHandler("demo.log",mode='a')    # creating file with name demo.log and setting mode to append 
       fileHandler.setLevel(logging.INFO)
       formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p') # it provides additional control over the log records
       fileHandler.setFormatter(formatter)  #setting handler 
       logger.addHandler(fileHandler)
       #logger levels
       logger.debug('debug message')        # low level sysytem info for debug purpose
       logger.info('info message')           # general sysytem info 
       logger.warn('warn message')             # Info of minor problem that has occured 
       logger.error('error message')         # Info of mijor problem that has occured
       logger.critical('critical message')    # Info of critical  problem that has occured

demo = MT_Logger()   #we are assinging  class to the variable demo
demo.testLog()  #calling the funtion

print("Done") 


















