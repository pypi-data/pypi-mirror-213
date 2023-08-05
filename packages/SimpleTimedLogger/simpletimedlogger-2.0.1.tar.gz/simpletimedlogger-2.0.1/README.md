**Simple Timed Logger**

It's logging package for very basic log messages.

It has 5 levels of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL).
By using unique keys, it is possible to measure elapsed time between 2 log messages

Logging is done by these methods:
- log()
- debug()
- info()
- warning()
- error()
- critical()

log() method can be set to log message on any level.

All logging methods take these keyword arguments:
- timed - (True/False) Is log message timed
- key - Unique key for timed log message. Use this key to stop logging and print out elapsed time.

If key is not provided for timed logging, it will be automatically generated.
To stop timed logging, use stop_timed_log() method. By passing key of log timer you want to stop. If no key is given, it will stop last started timed log.

using basic_config() it is possible to configure what lowest level of log messages will be printed to terminal