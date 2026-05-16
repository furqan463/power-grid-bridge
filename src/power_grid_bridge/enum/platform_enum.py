# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import EnumMeta, StrEnum


class _MetaClass(EnumMeta):
    def __contains__(cls, member):
        return member in cls.__members__

class ConverterPlatform(StrEnum, metaclass=_MetaClass):
    cyme = "cyme"
    etap = "etap"
    opendss = "opendss"
    pandapower = "pandapower"
    power_grid_model = "power_grid_model"
    psse = "psse"
    sincal = "sincal"
    synergi = "synergi"

def _str_to_converter_platform(data_type: ConverterPlatform | str) -> ConverterPlatform:
    """Helper function to transform data_type str to DatasetType."""
    if isinstance(data_type, ConverterPlatform):
        return data_type
    return ConverterPlatform[data_type]
