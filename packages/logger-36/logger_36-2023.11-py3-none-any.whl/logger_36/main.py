# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import datetime as dttm
import logging as lggg
import platform as pltf
import sys as sstm
import time
from pathlib import Path as path_t
from typing import ClassVar, TextIO
from types import FunctionType, MethodType

from rich.color import Color as color_t
from rich.console import Console as console_t
from rich.style import Style as style_t
from rich.text import Text as text_t

try:
    from psutil import Process as process_t

    _PROCESS = process_t()
    _KILO_UNIT = 1024.0
    _MEGA_UNIT = _KILO_UNIT * 1024.0
    _GIGA_UNIT = _MEGA_UNIT * 1024.0
except ModuleNotFoundError:
    _PROCESS = None
    _KILO_UNIT = _MEGA_UNIT = _GIGA_UNIT = 0.0


LOGGER_NAME = "logger-36"


# This module is certainly imported early. Therefore, the current time should be close enough to the real start time.
_START_TIME = time.time()

_TAB_SIZE = 5  # So that _CONTEXT_SEPARATOR is aligned for all log levels
_DATE_TIME_LENGTH = 19
_LOG_LEVEL_LENGTH = 10  # Max length, including _LEVEL_OPENING and _LEVEL_CLOSING

_LEVEL_OPENING = "["
_LEVEL_CLOSING = "]"
_CONTEXT_SEPARATOR = "- "
_WHERE_SEPARATOR = "@"
_ELAPSED_TIME_SEPARATOR = "+"
_MESSAGE_FORMAT = (
    f"%(asctime)s{_LEVEL_OPENING}%(levelname)s{_LEVEL_CLOSING}\t"
    f"{_CONTEXT_SEPARATOR}"
    f"%(message)s "
    f"{_WHERE_SEPARATOR} %(module)s:%(funcName)s:%(lineno)d "
    f"{_ELAPSED_TIME_SEPARATOR}%(elapsed_time)s"
    f"%(memory_usage)s"
)
_DATE_TIME_FORMAT = "%Y-%m-%d@%H:%M:%S"

_SYSTEM_DETAILS = (
    "node",
    "machine",
    "processor",
    "architecture",
    #
    "system",
    "release",
    "version",
    "platform",
    #
    "python_implementation",
    "python_version",
    "python_revision",
    "python_branch",
    "python_compiler",
    "python_build",
)


_CONTEXT_LENGTH = _DATE_TIME_LENGTH + _LOG_LEVEL_LENGTH
_NEXT_LINE_PROLOGUE = "\n" + (_CONTEXT_LENGTH + _CONTEXT_SEPARATOR.__len__() + 1) * " "

_SYSTEM_DETAILS = {_dtl.capitalize(): getattr(pltf, _dtl)() for _dtl in _SYSTEM_DETAILS}
_MAX_DETAIL_NAME_LENGTH = max(map(len, _SYSTEM_DETAILS.keys()))


# Alternative implementations: using logging.Filter or logging.LoggerAdapter


class _handler_extension:
    __slots__ = ("formatter", "show_memory_usage", "max_memory_usage", "exit_on_error")
    formatter: lggg.Formatter
    show_memory_usage: bool
    max_memory_usage: int
    exit_on_error: bool

    def __init__(self) -> None:
        """"""
        self.formatter = lggg.Formatter(fmt=_MESSAGE_FORMAT, datefmt=_DATE_TIME_FORMAT)
        self.show_memory_usage = False
        self.max_memory_usage = -1
        self.exit_on_error = False

    def FormattedMessage(self, record: lggg.LogRecord, /) -> tuple[str, str | None]:
        """
        Note: "message" is not yet an attribute of record (it will be set by format()); Use "msg" instead.
        """
        if not isinstance(record.msg, str):
            record.msg = str(record.msg)
        if "\n" in record.msg:
            original_message = record.msg
            lines = original_message.splitlines()
            record.msg = lines[0]
            next_lines = _NEXT_LINE_PROLOGUE.join(lines[1:])
            next_lines = f"{_NEXT_LINE_PROLOGUE}{next_lines}"
        else:
            original_message = next_lines = None

        # The record is shared between handlers, so do not re-assign if already there
        if not hasattr(record, "elapsed_time"):
            record.elapsed_time = ElapsedTime()
        # Re-assign for each handler in case they have different show properties
        if self.show_memory_usage:
            record.memory_usage = self.FormattedMemoryUsage()
        else:
            record.memory_usage = ""

        formatted = self.formatter.format(record)

        # Revert the record message to its original value for subsequent handlers
        if original_message is not None:
            record.msg = original_message

        return formatted, next_lines

    def FormattedMemoryUsage(self) -> str:
        """"""
        if self.show_memory_usage:
            usage = _PROCESS.memory_info().rss
            if usage > self.max_memory_usage:
                self.max_memory_usage = usage

            usage, unit = _MemoryWithAutoUnit(usage, 1)

            return f" :{usage}{unit}"
        else:
            return ""

    def ExitOrNotIfError(self, record: lggg.LogRecord, /) -> None:
        """"""
        if self.exit_on_error and (record.levelno in (lggg.ERROR, lggg.CRITICAL)):
            sstm.exit(1)


class console_handler_t(lggg.Handler, _handler_extension):
    _LEVEL_COLOR: ClassVar[dict[int, str | style_t]] = {
        lggg.DEBUG: "orchid",
        lggg.INFO: "white",
        lggg.WARNING: "yellow",
        lggg.ERROR: "orange1",
        lggg.CRITICAL: "red",
    }
    _GRAY_STYLE: ClassVar[style_t] = style_t(color=color_t.from_rgb(150, 150, 150))
    _ACTUAL: ClassVar[str] = r" Actual=[^.]+\."
    _EXPECTED: ClassVar[str] = r" Expected([!<>]=|: )[^.]+\."

    console: console_t

    def __init__(self, /, *, level: int = lggg.NOTSET) -> None:
        """"""
        lggg.Handler.__init__(self, level=level)
        _handler_extension.__init__(self)

        self.setFormatter(self.formatter)
        self.console = console_t(record=True, force_terminal=True, tab_size=_TAB_SIZE)

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        cls = self.__class__

        formatted, next_lines = self.FormattedMessage(record)
        # Used instead of _CONTEXT_LENGTH which might include \t, thus creating a
        # mismatch between character length and length when displayed in console.
        context_end = formatted.find(_LEVEL_CLOSING)
        elapsed_time_separator = formatted.rfind(_ELAPSED_TIME_SEPARATOR)
        where_separator = formatted.rfind(
            _WHERE_SEPARATOR, context_end, elapsed_time_separator
        )

        highlighted = text_t(formatted)
        highlighted.stylize("dodger_blue2", end=_DATE_TIME_LENGTH)
        highlighted.stylize(
            cls._LEVEL_COLOR[record.levelno],
            start=_DATE_TIME_LENGTH,
            end=context_end + 1,
        )
        highlighted.stylize(
            cls._GRAY_STYLE, start=where_separator, end=elapsed_time_separator
        )
        highlighted.stylize("green", start=elapsed_time_separator)

        if next_lines is not None:
            highlighted.append(next_lines)

        highlighted.highlight_words((cls._ACTUAL,), style="red")
        highlighted.highlight_words((cls._EXPECTED,), style="green")

        self.console.print(highlighted, crop=False, overflow="ignore", highlight=False)

        self.ExitOrNotIfError(record)


class file_handler_t(lggg.FileHandler, _handler_extension):
    def __init__(self, path: str | path_t, /, *args, **kwargs) -> None:
        """"""
        lggg.FileHandler.__init__(self, str(path), *args, **kwargs)
        _handler_extension.__init__(self)

        self.setFormatter(self.formatter)

    def emit(self, record: lggg.LogRecord, /) -> None:
        """"""
        formatted, next_lines = self.FormattedMessage(record)

        padding = (_LOG_LEVEL_LENGTH - record.levelname.__len__() - 1) * " "
        message = formatted.replace("\t", padding)
        if next_lines is not None:
            message = f"{message}{next_lines}"

        print(message, file=self.stream)
        self.stream.flush()

        self.ExitOrNotIfError(record)


LOGGER = lggg.getLogger(name=LOGGER_NAME)
LOGGER.setLevel(lggg.DEBUG)
LOGGER.addHandler(console_handler_t(level=lggg.INFO))


def AddFileHandler(
    path: str | path_t, /, level: int = lggg.INFO, *args, **kwargs
) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.exists():
        raise ValueError(f"{path}: File already exists")

    handler = file_handler_t(path, *args, **kwargs)
    handler.setLevel(level)
    LOGGER.addHandler(handler)


def SetLOGLevel(level: int, /, *, which: str = "a") -> None:
    """
    which: c=console, f=file, a=all
    """
    if which not in "cfa":
        raise ValueError(
            f'{which}: Invalid handler specifier. Expected="c" for console, "f" for file, or "a" for all'
        )

    for handler in LOGGER.handlers:
        if (
            (which == "a")
            or ((which == "c") and isinstance(handler, console_handler_t))
            or ((which == "f") and isinstance(handler, file_handler_t))
        ):
            handler.setLevel(level)


def SetShowMemoryUsage(show_memory_usage: bool, /) -> None:
    """"""
    if show_memory_usage and (_PROCESS is None):
        LOGGER.warning('Cannot show memory usage: Package "psutil" not installed')
        return

    for handler in LOGGER.handlers:
        if hasattr(handler, "show_memory_usage"):
            handler.show_memory_usage = show_memory_usage


def SetExitOnError(exit_on_error: bool, /) -> None:
    """"""
    for handler in LOGGER.handlers:
        if hasattr(handler, "exit_on_error"):
            handler.exit_on_error = exit_on_error


def LogSystemDetails() -> None:
    """"""
    details = "\n".join(
        f"    {_key:>{_MAX_DETAIL_NAME_LENGTH}}: {_vle}"
        for _key, _vle in _SYSTEM_DETAILS.items()
    )

    modules = sstm.modules
    with_versions = []
    max_length = 0
    m_idx = 0
    for name in sorted(modules.keys(), key=str.lower):
        if name.startswith("_") or ("." in name):
            continue

        module = modules[name]
        version = getattr(module, "__version__", None)
        if version is None:
            continue

        if (m_idx > 0) and (m_idx % 4 == 0):
            with_versions.append("\n")
        with_versions.append(f"{name}={version}")
        max_length = max(max_length, name.__len__() + version.__len__() + 1)
        m_idx += 1

    max_length += 4
    AlignedInColumns = lambda _str: f"{_str:{max_length}}" if _str != "\n" else "\n    "
    with_versions = map(AlignedInColumns, with_versions)
    modules = "".join(with_versions)

    LOGGER.info(
        f"SYSTEM DETAILS\n"
        f"{details}\n"
        f"    {'Python Modules':>{_MAX_DETAIL_NAME_LENGTH}}:\n"
        f"    {modules}"
    )


def SaveLOGasHTML(path: str | path_t | TextIO = None) -> None:
    """"""
    cannot_save = "Cannot save logging record as HTML"

    if path is None:
        for handler in LOGGER.handlers:
            if isinstance(handler, lggg.FileHandler):
                path = path_t(handler.baseFilename).with_suffix(".htm")
                break
        if path is None:
            LOGGER.warning(f"{cannot_save}: No file handler to build a filename from")
            return
        if path.exists():
            LOGGER.warning(
                f'{cannot_save}: Automatically generated path "{path}" already exists'
            )
            return
    elif isinstance(path, str):
        path = path_t(path)

    actual_file = isinstance(path, path_t)
    if actual_file and path.exists():
        LOGGER.warning(f'{cannot_save}: File "{path}" already exists')
        return

    console = None
    found = False
    for handler in LOGGER.handlers:
        console = getattr(handler, "console", None)
        if found := isinstance(console, console_t):
            break

    if found:
        html = console.export_html()
        if actual_file:
            with open(path, "w") as accessor:
                accessor.write(html)
        else:
            path.write(html)
    else:
        LOGGER.warning(f"{cannot_save}: No handler has a RICH console")


def WhereFunction(function: FunctionType, /) -> str:
    """"""
    return f"{function.__module__}:{function.__name__}"


def WhereMethod(instance: object, method: MethodType, /) -> str:
    """
    method: Could be a str instead, which would require changing method.__name__ into getattr(cls, method). But if the
        method name changes while forgetting to change the string in the call to WhereMethod accordingly, then an
        exception would be raised here.
    """
    cls = instance.__class__

    return f"{cls.__module__}:{cls.__name__}:{method.__name__}"


def TimeStamp() -> str:
    """"""
    return (
        dttm.datetime.now()
        .isoformat(timespec="milliseconds")
        .replace(".", "-")
        .replace(":", "-")
    )


def ElapsedTime() -> str:
    """"""
    output = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - _START_TIME))
    while output.startswith("00") and (" " in output):
        output = output.split(maxsplit=1)[-1]

    return output


def MaximumMemoryUsage(
    *, unit: str | None = "a", decimals: int = None
) -> tuple[int | float, str]:
    """
    unit: b or None=bytes, k=kilo, m=mega, g=giga, a=auto
    """
    usage = max(getattr(_hdr, "max_memory_usage", -1) for _hdr in LOGGER.handlers)

    if (unit is None) or (unit == "b"):
        unit = "B"
    elif unit == "k":
        usage = _Rounded(usage / _KILO_UNIT, decimals)
        unit = "KB"
    elif unit == "m":
        usage = _Rounded(usage / _MEGA_UNIT, decimals)
        unit = "MB"
    elif unit == "g":
        usage = _Rounded(usage / _GIGA_UNIT, decimals)
        unit = "GB"
    elif unit == "a":
        usage, unit = _MemoryWithAutoUnit(usage, decimals)

    return usage, unit


def _MemoryWithAutoUnit(usage: int, decimals: int | None, /) -> tuple[int | float, str]:
    """"""
    if usage > _GIGA_UNIT:
        return _Rounded(usage / _GIGA_UNIT, decimals), "GB"

    if usage > _MEGA_UNIT:
        return _Rounded(usage / _MEGA_UNIT, decimals), "MB"

    if usage > _KILO_UNIT:
        return _Rounded(usage / _KILO_UNIT, decimals), "KB"

    return usage, "B"


def _Rounded(value: float, decimals: int | None, /) -> int | float:
    """"""
    if decimals == 0:
        decimals = None

    return round(value, ndigits=decimals)
