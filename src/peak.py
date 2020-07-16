from enum import Enum


class Peak(Enum):

    # Shared with D-10 & VNBS
    RTIME = 1
    HEIGHT = 2
    AREA = 3
    AREAP = 4

    # Info Table Indicies
    SAMPLE = 0
    DATE = 1
    TIME = 2
    INJ = 3
    RACK = 4
    RACKPOS = 5
    TOTALAREA = 6
    PATTERN = 7

    # Variant Family
    TYPE = 9  # index in decoded_arr
    V2TURBOA1C = "V2TURBO_A1c_2.0"
    V2A1CNU = "V2_A1c_NU"
    V2BTHAL = "V2_BThal"
    V2DUAL = "V2_Dual"

    NGSP = 1
    CALAREA = 1

    V2_AREAP = 2
    V2_RTIME = 3
    V2_AREA = 4

    UNKNOWN = "Unknown"
