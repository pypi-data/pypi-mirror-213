from setuptools import setup, find_packages

VERSION = '2.0.1'
DESCRIPTION = 'Simple Timed logger, it write logs to terminal. Can write elapsed time between logs'
LONG_DESCRIPTION = 'Simple Timed logger with timed logs, to measure elapsed times between actions in your code. Can ' \
                   'log in 5 different levels. Possibility to set up lowest level of logged messages.'

setup(
    name="simpletimedlogger",
    version=VERSION,
    author="Karolis Andriunas",
    author_email="almex.developer@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'logger', 'simple', 'simplelogger'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
