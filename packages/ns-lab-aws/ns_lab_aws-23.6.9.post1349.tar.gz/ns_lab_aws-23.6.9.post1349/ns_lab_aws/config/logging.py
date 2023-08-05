logging_conf = '''[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=defaultFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=defaultFormatter
args=(sys.stdout,)

[formatter_defaultFormatter]
class=colorlog.ColoredFormatter
format=%(asctime)s - %(name)s - %(log_color)s%(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S:%MS %z
'''