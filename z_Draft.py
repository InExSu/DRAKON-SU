# организация логирования

import logging

logging.basicConfig(
    filename='drakon_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def foo():
    logging.debug("Вход в функцию foo")
    logging.info("инфо")
