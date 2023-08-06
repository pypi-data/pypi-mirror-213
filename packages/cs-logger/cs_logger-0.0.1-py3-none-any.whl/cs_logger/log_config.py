import logging

def setup_logger():
    logger = logging.getLogger()  # gets root logger
    logger.setLevel(logging.DEBUG)  # set minimum log level to send to handlers

    if not logger.handlers:
        # Create handlers
        c_handler = logging.StreamHandler()  # console handler
        f_handler = logging.FileHandler('file.log', 'a', 'utf-8')  # file handler
        c_handler.setLevel(logging.INFO)  # set minimum log level this handler will process
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
