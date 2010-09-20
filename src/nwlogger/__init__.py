import os, sys, datetime, base64
import logging
from logging.handlers import RotatingFileHandler
from atexit import register

# only import the public APIs
__all__ = ["setup_logging"]

# default log info
NW_DEFAULT_LOG_LEVEL=logging.DEBUG
NW_DEFAULT_LOG_DATE_FORMAT="%m-%d %H:%M:%S"
NW_DEFAULT_LOG_MSG_FORMAT="%(asctime)-15s %(levelname)-8s:%(name)-8s: %(message)s"
NW_DEFAULT_LOG_FILE_PATH="/tmp/logs/"
NW_DEFAULT_LOG_FILE_MODE="a" # create or append
NW_DEFAULT_LOG_MODULE_NAME=os.path.basename(__file__).replace(".py", "")
NW_DEFAULT_ROTATING_FILES_MAX_BYTE=(1024*1000)*5 # 5 Meg
NW_DEFAULT_ROTATING_BACKUP_NUM=5
  
# Build a unique log file name for this process
def _nwBuildFullPath(self, path=NW_DEFAULT_LOG_FILE_PATH):
    file=os.path.basename(__file__).replace(".py", "")
    dest=path.rstrip("").rstrip("/")
    uneek=base64.b64encode(file)
    user = os.getenv("USER")
    time=datetime.datetime.now().strftime("%Y-%m-%d")
    name=dest+"/"+file+"-"+time+"-"+user+"-"+uneek+".txt"
    return name

# Remove all logging resource upon exit 
def _shutdown():
    if logging._handlers:
        logging.info("Logger Shutting Down!")
        logging.shutdown()
        logging._handlers.clear()
register(_shutdown)

# Setup logging API, Must be called ONLY once
# console = True for debuging
# rotate = True for multi-file logging, each file grows upto maxBytes before being rotated out
# maxBytes = 0 to grow the single log file without a limit
_nwLogger_Configured = False
def setup_logging(logdir=NW_DEFAULT_LOG_FILE_PATH, 
                  filelog=True, 
                  rotate=True,
                  maxBytes=NW_DEFAULT_ROTATING_FILES_MAX_BYTE,
                  backupCount=NW_DEFAULT_ROTATING_BACKUP_NUM,
                  loglevel=NW_DEFAULT_LOG_LEVEL,
                  console=False
                  ):
    
    # Make sure this function is only called once
    global _nwLogger_Configured
    if _nwLogger_Configured:
        return
    
    # Drop any previous logging setup
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    
    # Setup the root logger
    log = logging.getLogger()
    log.setLevel(loglevel)

    # Setup the logger format
    log_formatter = logging.Formatter(NW_DEFAULT_LOG_MSG_FORMAT)

    if filelog:
        if not rotate: backupCount = 0
        logdir = os.path.abspath(logdir)
        if not os.path.exists(logdir): os.mkdir(logdir)
        logfile = _nwBuildFullPath(logdir)
        file_hdlr = RotatingFileHandler(filename=logfile, 
                                        maxBytes=maxBytes, 
                                        backupCount=backupCount,
                                        mode="a"
                                        )
        file_hdlr.doRollover()
        file_hdlr.setFormatter(log_formatter)
        log.addHandler(file_hdlr)
        log.info("Logger Initialized!")

    if console:
        console_hdlr = logging.StreamHandler()
        console_hdlr.setFormatter(log_formatter)
        log.addHandler(console_hdlr)

    _nwLogger_Configured = True
    
    
    
def uTest():
    # Setup the logger first 
    setup_logging(logdir='/tmp/logs', filelog=True, rotate=False, console=True)
    uLogCore = logging.getLogger('nwLogger.core')
    uLogCore.info("Testing: Instantiate nwLogger()")

    # Root Logger still works
    logging.info("-----------------------------------")
        
    # define a couple of other loggers to represent areas in your application:
    appA="app.A"
    logging.info("Testing: Setting up the logger for (%s)" % appA)
    uLogA = logging.getLogger(appA)
    if not uLogA:
        logging.error("Failed!: Setting up the logger for (%s)" % appA)
    else:
        uLogA.info("Passed!: Setting up the logger for (%s)" % appA)
        uLogA.debug("Debug test for app (%s)" % appA)
        uLogA.info("Info test for app (%s)" % appA)
        uLogA.warning("Warning test for app (%s)" % appA)
        uLogA.error("Error test for app (%s)" % appA)
        uLogA.critical("Critical test for app (%s)" % appA)

    # Root Logger still works
    logging.info("-----------------------------------")

    # appA logger still works
    uLogA.info("Test: Logger still active for app (%s)" % appA)
       
    # Root Logger still works
    logging.info("-----------------------------------")
     
    appB="app.B"
    logging.info("Testing: Setting up the logger for (%s)" % appB)
    uLogB = logging.getLogger(appB)
    if not uLogB:
        logging.error("Failed!: Setting up the logger for (%s)" % appB)
    else:
        uLogB.info("Passed!: Setting up the logger for (%s)" % appB)
        uLogB.debug("Debug test for app (%s)" % appB)
        uLogB.info("Info test for app (%s)" % appB)
        uLogB.warning("Warning test for app (%s)" % appB)
        uLogB.error("Error test for app (%s)" % appB)
        uLogB.critical("Critical test for app (%s)" % appB)
        
    # Root Logger still works
    logging.info("-----------------------------------")

    # Test if modules can pass their name as __file__ format
    appC=os.path.basename(__file__).replace(".py", "")
    logging.info("Testing: Setting up the logger for (%s)" % appC)
    uLogC = logging.getLogger(appC)
    if not uLogC:
        logging.error("Failed!: Setting up the logger for (%s)" % appC)
    else:
        uLogC.info("Passed!: Setting up the logger for (%s)" % appC)
        uLogC.debug("Debug test for app (%s)" % appC)
        uLogC.info("Info test for app (%s)" % appC)
        uLogC.warning("Warning test for app (%s)" % appC)
        uLogC.error("Error test for app (%s)" % appC)
        uLogC.critical("Critical test for app (%s)" % appC)
        
    # Root Logger still works
    logging.info("-----------------------------------")
    
    # appA logger still works
    uLogA.info("Test: Logger still active for app (%s)" % appA)
    uLogB.info("Test: Logger still active for app (%s)" % appB)
       
    # Root Logger still works
    logging.info("-----------------------------------")
    
    # Test the root logger via our API
    root="root"
    logging.info("Testing: Setting up the logger for (%s)" % root)
    uLogR = logging.getLogger("")
    if not uLogR:
        logging.error("Failed!: Setting up the logger for (%s)" % root)
    else:
        uLogR.info("Passed!: Setting up the logger for (%s)" % root)
        uLogR.debug("Debug test for app (%s)" % root)
        uLogR.info("Info test for app (%s)" % root)
        uLogR.warning("Warning test for app (%s)" % root)
        uLogR.error("Error test for app (%s)" % root)
        uLogR.critical("Critical test for app (%s)" % root)
        
        # Root Logger still works
    logging.info("-----------------------------------")
    
    # appA logger still works
    uLogA.info("Test: Logger still active for app (%s)" % appA)
    uLogB.info("Test: Logger still active for app (%s)" % appB)
    uLogC.info("Test: Logger still active for app (%s)" % appC)
       
    # Root Logger still works
    logging.info("-----------------------------------")
    
    # Test second getLogger calls
    logging.info("Testing: 2nd call to setup for the logger (%s)" % appA)
    uLogA2 = logging.getLogger(appA)
    if not uLogA2:
        logging.error("Failed!: 2nd setup call for the logger (%s)" % appA)
        uLogA.info("1st logger handle still works for (%s) ?" % appA)
    elif uLogA2 == uLogA:
        uLogA2.info("2nd call hander is the same as the 1st (%s)" % appA)
        uLogA.info("1st call hander is the same as the 2nd (%s)" % appA)
    else:
        uLogA2.info("Passed!: Setting up the logger for (%s)" % appA)
        uLogA2.debug("Debug test for app (%s)" % appA)
        uLogA2.info("Info test for app (%s)" % appA)
        uLogA2.warning("Warning test for app (%s)" % appA)
        uLogA2.error("Error test for app (%s)" % appA)
        uLogA2.critical("Critical test for app (%s)" % appA)
        
    # Root Logger still works
    logging.info("-----------------------------------")
    
    logging.info("Done! With Single File Logging")
    
# CommandLine
if __name__ == "__main__":
    sys.exit(uTest())



