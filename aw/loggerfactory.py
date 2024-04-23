import logging

from conf import ROOT_DIR

class LoggerFactory:
    @staticmethod
    def createFactory(name, datestamp, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s %(message)s"
        )
        file_handler = logging.FileHandler(f"{datestamp}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

