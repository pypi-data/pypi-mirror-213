"""
wifi: dictionaries and functionsto translate frequencies, and standards
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import bisect

from . import exitcodes
from .msg_window import show_error_message

# 2.4 GHz (802.11b/g/n/ax)
WIFI_2400_MHZ_CHANNELS = {
    2412 : 1,
    2417 : 2,
    2422 : 3,
    2427 : 4,
    2432 : 5,
    2437 : 6,
    2442 : 7,
    2447 : 8,
    2452 : 9,
    2457 : 10,
    2462 : 11,
    2467 : 12,
    2472 : 13,
    2484 : 14 }

# 3.65 GHz (802.11y)
WIFI_3650_MHZ_CHANNELS = {
    3657.5 : 131,
    3662.5 : 132,
    3667.5 : 133,
    3672.5 : 134,
    3677.5 : 135,
    3682.5 : 136,
    3687.5 : 137,
    3692.5 : 138 }

# 5 GHz (802.11a/h/j/n/ac/ax)
WIFI_5000_MHZ_CHANNELS = {
    5035 : 7,
    5040 : 8,
    5045 : 9,
    5055 : 11,
    5060 : 12,
    5080 : 16,
    5160 : 32,
    5170 : 34,
    5180 : 36,
    5190 : 38,
    5200 : 40,
    5210 : 42,
    5220 : 44,
    5230 : 46,
    5240 : 48,
    5250 : 50,
    5260 : 52,
    5270 : 54,
    5280 : 56,
    5290 : 58,
    5300 : 60,
    5310 : 62,
    5320 : 64,
    5340 : 68,
    5480 : 96,
    5500 : 100,
    5510 : 102,
    5520 : 104,
    5530 : 106,
    5540 : 108,
    5550 : 110,
    5560 : 112,
    5570 : 114,
    5580 : 116,
    5590 : 118,
    5600 : 120,
    5610 : 122,
    5620 : 124,
    5630 : 126,
    5640 : 128,
    5660 : 132,
    5670 : 134,
    5680 : 136,
    5690 : 138,
    5700 : 140,
    5710 : 142,
    5720 : 144,
    5745 : 149,
    5755 : 151,
    5765 : 153,
    5775 : 155,
    5785 : 157,
    5795 : 159,
    5805 : 161,
    5815 : 163,
    5825 : 165,
    5835 : 167,
    5845 : 169,
    5855 : 171,
    5865 : 173,
    5875 : 175,
    5885 : 177,
    5900 : 180,
    5910 : 182,
    5915 : 183,
    5920 : 184,
    5935 : 187,
    5940 : 188,
    5945 : 189,
    5960 : 192,
    5980 : 196 }

# 6 GHz (802.11ax)
WIFI_6000_MHZ_CHANNELS = {
    5955 : 1,
    5975 : 5,
    5995 : 9,
    6015 : 13,
    6035 : 17,
    6055 : 21,
    6075 : 25,
    6095 : 29,
    6115 : 33,
    6135 : 37,
    6155 : 41,
    6175 : 45,
    6195 : 49,
    6215 : 53,
    6235 : 57,
    6255 : 61,
    6275 : 65,
    6295 : 69,
    6315 : 73,
    6335 : 77,
    6355 : 81,
    6375 : 85,
    6395 : 89,
    6415 : 93 }

# Merge of all bands
"""
#This works in Python3.9+. 3.9 is not that well deployed yet
WIFI_ALL_CHANNELS = WIFI_2400_MHZ_CHANNELS   \
                    | WIFI_3650_MHZ_CHANNELS \
                    | WIFI_5000_MHZ_CHANNELS \
                    | WIFI_6000_MHZ_CHANNELS
"""
#This works in Python3.5+
WIFI_ALL_CHANNELS = {
    **WIFI_2400_MHZ_CHANNELS,
    **WIFI_3650_MHZ_CHANNELS,
    **WIFI_5000_MHZ_CHANNELS,
    **WIFI_6000_MHZ_CHANNELS }

# all the different wifi standards:
WIFI_STANDARD_a = "802.11a"
WIFI_STANDARD_b = "802.11b"
WIFI_STANDARD_g = "802.11g"
WIFI_STANDARD_n = "802.11n"
WIFI_STANDARD_y = "802.11y"
WIFI_STANDARD_ac = "802.11ac"
WIFI_STANDARD_ax = "802.11ax"

WIFI_BAND_2400 = "2.4 GHz"
WIFI_BAND_3650 = "3.65 GHz"
WIFI_BAND_5000 = "5 GHz"
WIFI_BAND_6000 = "6 GHz"

# generation based on 802.11 standard or frequency band (less reliable)
WIFI_GENERATIONS = {
    WIFI_STANDARD_a : 2,
    WIFI_STANDARD_b : 1,
    WIFI_STANDARD_g : 3,
    WIFI_STANDARD_n : 4,
    WIFI_STANDARD_y : 4,
    WIFI_STANDARD_ac : 5,
    WIFI_STANDARD_ax : 6,
    WIFI_BAND_2400 : 4,                     # most 802.11a/b/g are gone
    WIFI_BAND_3650 : 4,
    WIFI_BAND_5000 : 5,
    WIFI_BAND_6000 : 6 }

# normally between -30 and -100 dBm
WIFI_SIGNAL_STRENGTH_BRACKETS = [-90, -80, -70, -65, -39]
WIFI_SIGNAL_STRENGTH_LABELS = [
    "Faint", "Weak", "Fair", "Good", "Strong", "Excellent"]

def wifi_signal_strength(dbm):
    """returns the wifi signal strenght as a tuple:
    - pos:  0-5, whereby 0 is unusable (<90dBm), and 5 is excellent (>39dBm)
    - label: WIFI_SIGNAL_STRENGTH_LABELS """
    pos = bisect.bisect_right(WIFI_SIGNAL_STRENGTH_BRACKETS, dbm)
    label = WIFI_SIGNAL_STRENGTH_LABELS[pos]
    return label, pos

def wifi_channel(freq_mhz):
    "tries to get the band from the dictionary, returns 0 when failing"
    try:
        return WIFI_ALL_CHANNELS[freq_mhz]
    except KeyError:
        print("Frequency ", freq_mhz, "MHz for found in translation table")
        return 0
    except Exception as e:
        show_error_message("Unexpected error in wifi_channels:wifi_channel",
                            str(e), exitcode=exitcodes.INTERNAL_ERROR)

def wifi_band(freq_mhz):
    "returns which band a freq fits in: 2.4 Ghz, 3.65 Ghz, 5 Ghz, or 6 Ghz"
    if freq_mhz in WIFI_2400_MHZ_CHANNELS:
        return WIFI_BAND_2400
    elif freq_mhz in WIFI_5000_MHZ_CHANNELS:
        return WIFI_BAND_5000
    elif freq_mhz in WIFI_6000_MHZ_CHANNELS:
        return WIFI_BAND_6000
    elif freq_mhz in WIFI_3650_MHZ_CHANNELS:
        return WIFI_BAND_3650
    else:
        print("Frequency ", freq_mhz, "MHz not found in translation tables")
        return ""

def wifi_generation(standard_802 = None, freq_band = None):
    "Returns the wifi generation: 4, 5, or 6, based on 802.11n/ac/ax"
    if standard_802 and standard_802 in WIFI_GENERATIONS:
        return WIFI_GENERATIONS[standard_802]
    elif freq_band and freq_band in WIFI_GENERATIONS:
        return WIFI_GENERATIONS[freq_band]
    else:
        print("Cannot determine WiFi generation based on standard",
              standard_802, " nor on freq_band", freq_band)
        return 0


