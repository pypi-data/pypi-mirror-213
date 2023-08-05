"""S
imple Timed Logger
    Copyright (C) 2021  Karolis Andriunas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Simple Timed Logger allows to log to terminal easily. Has possibility to log elapsed time between actions.
"""

import random
import string
from datetime import datetime


class Logger:
    def __init__(self):
        """Initializes SimpleLogger class with constants"""
        self.__timed_log_dict_list = []
        self.__generated_temp_keys = []
        self.__levels_of_logs = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

        self.DEBUG = 'DEBUG'
        self.INFO = 'INFO'
        self.WARNING = 'WARNING'
        self.ERROR = 'ERROR'
        self.CRITICAL = 'CRITICAL'

        self.__MIN_LEVEL_OF_LOG = self.__levels_of_logs.index(self.DEBUG)

    def basic_config(self, **kwargs):
        """Allows to configure lowest level of log message to be printed out to console"""
        self.__MIN_LEVEL_OF_LOG = self.__levels_of_logs.index(kwargs.get('min_level_of_logging', self.DEBUG))

    def log(self, level: str, msg: str, **kwargs) -> None:
        """Prints log message to console and if needed starts timed logging

        level - Level of log message
        msg - log message

        keyword params:
        timed - Is it timed log message (True/False)
        key - key of timed log message, used to stop timer with function end_timed_log()
        """
        timed = kwargs.get('timed', False)
        key = kwargs.get('key', '')

        if timed:
            self.start_timed_log(msg, level=self.__levels_of_logs.index(level), key=key)
        else:
            self.__log_message(msg, self.__levels_of_logs.index(level))

    def debug(self, msg: str, **kwargs) -> None:
        """Prints log message to console with DEBUG level

        parameters taken are same as log() function
        """
        self.log(self.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs) -> None:
        """Prints log message to console with INFO level

        parameters taken are same as log() function
        """
        self.log(self.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs) -> None:
        """Prints log message to console with WARNING level

        parameters taken are same as log() function
        """
        self.log(self.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        """Prints log message to console with ERROR level

        parameters taken are same as log() function
        """
        self.log(self.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> None:
        """Prints log message to console with CRITICAL level

        parameters taken are same as log() function
        """
        self.log(self.CRITICAL, msg, **kwargs)

    def start_timed_log(self, msg: str, **kwargs) -> None:
        """Starts timed log message to measure elapsed time between start and end of action. Stopped using
        stop_timed_log() function. If no key is provided it generates and assigns random key"""
        key = kwargs.get('key', '')
        level = kwargs.get('level', 0)

        if key == '':
            key = self.__generate_random_key()

        if msg > '':
            self.__log_message(msg, level)

        log_dict = {
                'key': key,
                'level': level,
                'message': msg,
                'start_time': datetime.now(),
                'end_time': None
            }

        self.__timed_log_dict_list.append(log_dict.copy())
        self.__log_message(f'Timed log started for key {key}', self.__levels_of_logs.index(self.DEBUG))

    def end_timed_log(self, msg: str, **kwargs) -> None:
        """Ends timed log and prints out message with elapsed time since start. If no key is provided it will end
        last started timed log"""
        key = kwargs.get('key', '')
        use_temp_key = False

        try:
            if key == '':
                use_temp_key = True
                log_dict = list(filter(lambda log: log['key'] == self.__generated_temp_keys[-1], self.__timed_log_dict_list))
                key = log_dict[0]['key']
            else:
                log_dict = list(filter(lambda log: log['key'] == key, self.__timed_log_dict_list))

            if not log_dict:
                raise NoTimedLogKeyFound

        except NoTimedLogKeyFound:
            self.__log_message(f"No timed log found with the key: {key}, couldn't stop timed log", self.__levels_of_logs.index(self.ERROR))
            return

        log_dict[0]['end_time'] = datetime.now()
        elapsed = log_dict[0]['end_time'] - log_dict[0]['start_time']
        elapsed_ms = int(elapsed.total_seconds() * 1000)
        message = msg + ' (Elapsed time: {0}ms)'.format(elapsed_ms)
        self.__log_message(message, log_dict[0]['level'])
        self.__timed_log_dict_list[:] = [d for d in self.__timed_log_dict_list if d.get('key') != key]

        if use_temp_key:
            self.__generated_temp_keys.remove(key)

    def __log_message(self, msg: str, level: int) -> None:
        """Prints log message to console"""
        if self.__MIN_LEVEL_OF_LOG <= level:
            print('{0} {1}: {2}'.format(datetime.now(), self.__levels_of_logs[level], msg))

    def __generate_random_key(self) -> str:
        """Generates random key for timed log message if no key is provided"""
        letters = string.ascii_lowercase
        key = ''.join(random.choice(letters) for i in range(16))
        log_dict = list(filter(lambda log: log['key'] == key, self.__timed_log_dict_list))
        if not log_dict:
            self.__generated_temp_keys.append(key)
            return key
        else:
            return self.__generate_random_key()


class NoTimedLogKeyFound(Exception):
    pass
