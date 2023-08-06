#!/usr/bin/python3
"""
profile_store:: code related to storing profile config files
(c) 202102923 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
import bisect
import configparser
from datetime import datetime

from . import pyiwd

# FIXME move to separate module
IWDGUI_CONFIG_DIR = os.path.expanduser("~/.iwdgui")
IWDGUI_CONFIG_DIR_MODE = 0o700
IWDGUI_CONFIG_FILE_MODE = 0o600

CONFIG_DIR = {
    pyiwd.ACCESS_POINT_MODE : IWDGUI_CONFIG_DIR + "/ap",
    pyiwd.AD_HOC_MODE : IWDGUI_CONFIG_DIR + "/adhoc" }

CONFIG_EXT = {
    pyiwd.ACCESS_POINT_MODE : ".ap",
    pyiwd.AD_HOC_MODE : ".adhoc" }


b2s = lambda b: "true" if b else "false"
s2b = lambda s: True if s.lower() in ["true", "yes"] else False

def _protected_opener(path, flags):
    "Opens file with mode 0o600, read write by owner only"
    return os.open(path, flags, mode=IWDGUI_CONFIG_FILE_MODE)


class profile_store():

    def __init__(self, mode):
        self.mode = mode
        self.config_dir = CONFIG_DIR[mode]
        self.config_ext = CONFIG_EXT[mode]
        os.makedirs(self.config_dir, IWDGUI_CONFIG_DIR_MODE, exist_ok=True)
        self._change_callbacks = []

    def _fname(self, nw_name):
        "constructs the filename of an access point network config file"
        return self.config_dir + "/" + nw_name + self.config_ext

    def add_callback(self, callback_fn):
        "adds the callback function to the callback list"
        self._change_callbacks.append(callback_fn)

    def _call_callbacks(self):
        for fn in self._change_callbacks:
            fn()

    def store_profile(self, profile_dic):
        "Stores a profile on disk"
        fname = self._fname(profile_dic["Name"])
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config["Security"] = {"Passphrase" : profile_dic["Passphrase"]}
        config["Settings"] = {
            "AutoConnect": b2s(profile_dic["AutoConnect"])}
        with open(fname, 'w', opener=_protected_opener) as fh:
            config.write(fh, space_around_delimiters=False)
        self._call_callbacks()

    def read_profile(self, nw_name):
        "Reads a profile from disk"
        profile = {}
        if nw_name == None or len(nw_name) == 9:
            return None
        fname = self._fname(nw_name)
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(fname)
        profile["Name"] = nw_name
        profile["Passphrase"] = config["Security"]["Passphrase"]
        profile["AutoConnect"] = s2b(config["Settings"]["AutoConnect"])
        stat = os.stat(fname)
        dt = datetime.utcfromtimestamp(stat.st_mtime)
        profile["LastConnectedTime"] = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        return profile

    def profile_list(self):
        times = []
        nw_names = []
        fname_ext_len = len(self.config_ext)
        with os.scandir(self.config_dir) as it:
            for entry in it:
                if entry.name.endswith(self.config_ext) and entry.is_file():
                    stat = entry.stat()
                    time = stat.st_mtime_ns
                    pos = bisect.bisect_left(times, time)
                    times.insert(pos, time)
                    nw_name = entry.name[:-fname_ext_len]
                    nw_names.insert(pos, nw_name)
        return nw_names

    def rm_profile(self, nw_name):
        "Removes an ap prpfile"
        fname = self._fname(nw_name)
        try:
            os.remove(fname)
        except Exception as e:
            print("Unable to remove file", fname,", error:", e)
        self._call_callbacks()

    def touch(self, nw_name):
        os.utime(self._fname(nw_name))
        self._call_callbacks()


# create instances for access point and adhoc
ap_store = profile_store(pyiwd.ACCESS_POINT_MODE)
adhoc_store = profile_store(pyiwd.AD_HOC_MODE)
