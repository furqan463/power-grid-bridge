# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

from power_grid_bridge.enum.platform_enum import ConverterPlatform
from power_grid_bridge.errors.base_errors import PowerGridBridgeError


class InvalidPlatformError(KeyError, PowerGridBridgeError):
    def __init__(self, platform: str):
        super().__init__(f"Unsupported Platform {platform}.")

class ConverterNotImplementedError(NotImplementedError, PowerGridBridgeError):
    def __init__(self, from_platform: ConverterPlatform, to_platform: ConverterPlatform):
        super().__init__(f"The Conversion {from_platform} - {to_platform} is not yet implemented.")
