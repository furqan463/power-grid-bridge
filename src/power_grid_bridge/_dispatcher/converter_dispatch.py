# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

from power_grid_bridge.enum.platform_enum import ConverterPlatform


class ConverterDispatch:
    def __init__(self, from_platform: ConverterPlatform, to_platform: ConverterPlatform):
        self._from = from_platform
        self._to = to_platform

    def is_conversion_supported(self) -> bool:
        return False
