
import logging
import os
if not os.path.exists("Logs"):
    os.makedirs("Logs")

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='Logs/test.log',
                    level=logging.DEBUG)
logging.debug('debug 信息')
logging.info('info 信息')
logging.warning('warning 信息')
logging.error('error 信息')
logging.critical('critial 信息')
