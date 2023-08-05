from Alogger import Alogger, LogLevel
logger = Alogger(log_level=LogLevel.ALL, log_to_file=True)
logger.fatal("fatal")
logger.error("error")
logger.warning("warning")
logger.info("info")
logger.debug("debug")
logger.trace("trace")
logger.test("test")
# https://barisariburnu.github.io/blog/2015/08/17/pypi-paketi-olusturma.html


def deneme():
    logger.fatal("fatal")
    logger.error("error")
    logger.warning("warning")
    logger.info("info")
    logger.debug("debug")
    logger.trace("trace")
    logger.test("test")


deneme()
