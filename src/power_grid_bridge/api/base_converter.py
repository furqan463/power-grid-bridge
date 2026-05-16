# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

import logging
import sys

from power_grid_bridge._dispatcher.converter_dispatch import ConverterDispatch
from power_grid_bridge.enum import ConverterPlatform
from power_grid_bridge.enum.platform_enum import _str_to_converter_platform
from power_grid_bridge.errors.api_errors import ConverterNotImplementedError, InvalidPlatformError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set the minimum threshold level
console_handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

class PowerGridBridge:

    def __init__(self, from_format: ConverterPlatform | str, to_format: ConverterPlatform | str):
        try:
            from_format = _str_to_converter_platform(from_format)
        except KeyError:
            logger.error("Unsupported Platform %s.", from_format)
            raise InvalidPlatformError(str(from_format))
        self._from: ConverterPlatform = from_format

        try:
            to_format = _str_to_converter_platform(to_format)
        except KeyError:
            logger.error("Unspoorted Platform %s.", to_format)
            raise InvalidPlatformError(str(to_format))
        self._to: ConverterPlatform = to_format

        self._dispatcher = ConverterDispatch(self._from, self._to)
        self._validate()


    def _validate(self):
        if not self._dispatcher.is_conversion_supported():
            logger.error("The conversion %s - %s is not supported yet.", self._from, self._to)
            raise ConverterNotImplementedError(self._from, self._to)
