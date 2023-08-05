from tj_kits_wind.tj_logger.LoggerFactory import *


def test_logger_console():
    logger1 = logger_console("wordy")
    logger2 = logger_console("normal")
    logger3 = logger_console("short")
    logger4 = logger_console("very_short")

    logger1.info("Hello")
    logger2.info("Hello")
    logger3.info("Hello")
    logger4.info("Hello")


def test_logger_auto():
    pwd = os.path.abspath('.')
    logger_path = os.path.join(pwd, "logs")

    logger2 = logger_auto(name="logger2", log_path=logger_path, logger_format="short")
    logger3 = logger_auto(name="logger3", log_path=logger_path, logger_format="normal")
    logger4 = logger_auto(name="logger4", log_path=logger_path, logger_format="wordy")
    logger1 = logger_auto(name="logger1", log_path=logger_path, logger_format="very_short")

    logger1.info("Hello")
    logger2.info("Hello")
    logger3.info("Hello")
    logger4.info("Hello")


if __name__ == '__main__':
    test_logger_console()
    # test_logger_auto()
#
