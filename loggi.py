import logging


def log():
    logger = logging.getLogger("rabota_parser")
    logger.setLevel(logging.DEBUG)


    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S')


    file_handler = logging.FileHandler("parser.log", mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)


    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)


    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger