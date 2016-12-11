import logging
import logging.handlers
import os
 
ERROR_LOG_PATH = os.path.join(os.getcwd(), 'Log')
if not os.path.exists(ERROR_LOG_PATH):
    os.makedirs(ERROR_LOG_PATH)
 
def create_logger(filename):
    logger = logging.getLogger(filename)
    logger.handlers = []
    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(ERROR_LOG_PATH, filename)
    )
    handler.setFormatter(logging.Formatter(
        '[%(levelname)s %(asctime)s.%(msecs)d %(module)s:%(lineno)d]: %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
 
mainLog = create_logger('Error.log')
ircLog = create_logger('irc.log')
