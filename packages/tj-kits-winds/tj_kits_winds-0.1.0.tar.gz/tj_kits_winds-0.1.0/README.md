## tj_kits_wind

自用工具包 - wind 系列:  内置模块的相关工具包

### logger 相关

所有 终端 logger 共用一个 handler, 其格式 会被最后一个声明的 logger 覆盖.

```python
logger1 = logger_console("wordy")
logger2 = logger_console("normal")
logger3 = logger_console("short")
logger4 = logger_console("very_short")

logger1.info("Hello")   # [INFO] Hello
logger2.info("Hello")   # [INFO] Hello
logger3.info("Hello")   # [INFO] Hello
logger4.info("Hello")   # [INFO] Hello

```



文件 logger 目前只支持 RotatingFileHandler.

```python
pwd = os.path.abspath('.')
logger_path = os.path.join(pwd, "logs")

logger1 = logger_auto(name="logger1", log_path=logger_path, logger_format="very_short")
logger2 = logger_auto(name="logger2", log_path=logger_path, logger_format="short")
logger3 = logger_auto(name="logger3", log_path=logger_path, logger_format="normal")
logger4 = logger_auto(name="logger4", log_path=logger_path, logger_format="wordy")

logger1.info("Hello")
logger2.info("Hello")
logger3.info("Hello")
logger4.info("Hello")

# logs
#	logger1.log: [INFO] Hello
#   logger2.log: [05-01 17:37:42 | INFO] Hello
#   logger3.log: [05-01 17:37:42 | INFO | pid:18716 | test_logger.py:27] Hello
#   logger4.log: [05-01 17:37:42 | INFO | pid:18716 | tid:20520 | test_logger | test_logger_auto | test_logger.py:28] Hello


```

