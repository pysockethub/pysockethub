"""
This module provides subclasses of logging.Formatter and logging.Logger that
support colorization.

To use:
>>> import colorlog
>>> import logging
>>> logging.setLoggerClass(colorlog.ColorLog)
>>> log = logging.getLogger(__name__)
>>> log_handler = logging.StreamHandler()
>>> log_formatter = colorlog.ColorFormatter()
>>> log_handler.setFormatter(log_formatter)
>>> log.addHandler(log_handler)

>>> log.debug('Error count: %d', err_cnt, color='RED')
>>> log.debug('Error count: %d', err_cnt, color='RED:WHITE')

The color argument is a colon-separated list of foreground:background:style
strings.

See ansicolor.py for a list of available colors and styles.

"""

import logging
import time

import ansicolor

class ColorFormatter(logging.Formatter):
    """
    A logging formatter that applies ANSI color escape codes to log messages
    as directed by the .color attribute of LogRecords.  To pass the color
    argument to a logger, use the `color` parameter:

    >>> log.debug('message', color='RED')

    Use color names from ansicolor.py.

    If color name isn't found, color is ignored.
    """
    def format(self, record):
        fmtd_msg = record.msg % record.args

        if record.color:
            color_info = record.color.split(':')

            try:
                fore = getattr(ansicolor.fore, color_info[0])
            except AttributeError:
                fore = ''

            try:
                back = getattr(ansicolor.back, color_info[1])
            except (IndexError, AttributeError):
                back = ''

            try:
                style = getattr(ansicolor.style, color_info[2])
            except (IndexError, AttributeError):
                style = ''

            fmtd_msg = fore + back + style + fmtd_msg + ansicolor.style.RESET

        datefmt = '%Y-%m-%d %H:%M:%S'
        time_str = time.strftime(datefmt, time.localtime(record.created))

        return f'{time_str}.{int(record.msecs):03d} [{record.levelname}] {fmtd_msg}'

class ColorLog(logging.Logger):
    """
    Subclass of logging.Logger that accepts a color parameter.  The color parameter value is
    placed into the LogRecord's extra dict where it can be picked up by a custom formatter,
    such as ColorFormatter, above.
    """
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1,
             color=None):
        if extra is None:
            extra = {'color': color}
        else:
            extra['color'] = color
        super()._log(level, msg, args, exc_info=None, extra=extra, stack_info=False)
