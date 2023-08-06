#!/usr/bin/env python3

"""
pyiwd_test: the pyiwd test suite
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.

Usage: python -m unittest iwdgui.pyiwd_test

"""
import unittest
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib

import pyiwd

PRINT = False

POWERTEST = False

loop = GLib.MainLoop()
main_context = GLib.MainLoop.get_context(loop)

def wait4condition(secs, condition):

    def timeup():
        return  starttime + sec < time.now()

    global main_context
    starttime, now = time.time()
    while not condition or timeup():
        main_context.iteration(False)

#class TestStringMethods(unittest.TestCase):
class test_pyiwd_lists(unittest.TestCase):
    "pyiwd tests: for the iwd dbus bindings"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_obj_get(self):
        dic = pyiwd.obj_get()

    def test_dev_list(self):
        lst = pyiwd.dev_list()

    def test_adapterlist(self):
        lst = pyiwd.adapter_list()

    def test_known_nw_list(self):
        lst = pyiwd.known_nw_list()

    def test_station_list(self):
        lst = pyiwd.station_list()


class test_pyiwd_known_nws(unittest.TestCase):

    def test_known_nw(self):
        path = pyiwd.known_nw_path_by_name("Belair5")
        known_nw_dic = pyiwd.known_nw_dic_by_path(path)
        autoconnect = known_nw_dic['AutoConnect']

        #turn autoconnect off and check
        pyiwd.known_nw_autoconnect_off(path)
        self.assertFalse(
            pyiwd.known_nw_dic_by_path(path)['AutoConnect'])
        #turn autoconnect on and check
        pyiwd.known_nw_autoconnect_on(path)
        self.assertTrue(
            pyiwd.known_nw_dic_by_path(path)['AutoConnect'])

        #reset to previous
        pyiwd.known_nw_autoconnect(path, autoconnect)
        self.assertEqual(
            pyiwd.known_nw_dic_by_path(path)['AutoConnect'],
            autoconnect)


class test_pyiwd_dev(unittest.TestCase):

    def test_dev_mode(self):
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        dev_dic = pyiwd.dev_dic_by_path(path)
        mode = dev_dic["Mode"]

        #test access point mode
        pyiwd.dev_set_ap_mode(path)
        self.assertEqual("ap", pyiwd.dev_dic_by_path(path)["Mode"])

        #test ad-hoc mode
        pyiwd.dev_set_adhoc_mode(path)
        time.sleep(0.5)
        self.assertEqual("ad-hoc", pyiwd.dev_dic_by_path(path)["Mode"])

        #test station mode
        pyiwd.dev_set_station_mode(path)
        time.sleep(0.5)
        self.assertEqual("station", pyiwd.dev_dic_by_path(path)["Mode"])

        #reset mode
        pyiwd.dev_set_mode(path, mode)
        time.sleep(0.5)
        self.assertEqual(mode, pyiwd.dev_dic_by_path(path)["Mode"])

    def test_dev_power(self):
        if not POWERTEST:
            return
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        dev_dic = pyiwd.dev_dic_by_path(path)
        power = dev_dic["Powered"]

        #test power on
        pyiwd.dev_set_power_on(path)
        time.sleep(0.5)
        self.assertTrue(pyiwd.dev_dic_by_path(path)["Powered"])

        #test power off
        pyiwd.dev_set_power_off(path)
        time.sleep(0.5)
        self.assertFalse(pyiwd.dev_dic_by_path(path)["Powered"])

        #reset power
        pyiwd.dev_set_power(path, power)
        time.sleep(0.5)
        self.assertEqual(power, pyiwd.dev_dic_by_path(path)["Powered"])

class test_pyiwd_adapter(unittest.TestCase):

    def test_adapter_power(self):
        if not POWERTEST:
            return
        name  = pyiwd.adapter_list()[0]["Name"]
        path = pyiwd.adapter_path_by_name(name)
        adapter_dic = pyiwd.adapter_dic_by_path(path)
        power = adapter_dic["Powered"]

        #test power on
        pyiwd.adapter_set_power_on(path)
        time.sleep(0.5)
        self.assertTrue(pyiwd.adapter_dic_by_path(path)["Powered"])

        #test power off
        pyiwd.adapter_set_power_off(path)
        time.sleep(0.5)
        self.assertFalse(pyiwd.adapter_dic_by_path(path)["Powered"])

        #reset power
        pyiwd.adapter_set_power(path, power)
        time.sleep(0.5)
        self.assertEqual(power, pyiwd.adapter_dic_by_path(path)["Powered"])


class test_pyiwd_station(unittest.TestCase):

    def test_station_scan(self):
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        station_dic = pyiwd.station_dic_by_path(path)

        # wait for scanning to be done
        while pyiwd.station_dic_by_path(path)['Scanning']:
            time.sleep(0.1)

        #scan
        #pyiwd.station_scan(path)
        #time.sleep(1)

        #self.assertTrue(pyiwd.station_dic_by_path(path)['Scanning'])

        # wait for scanning to be done
        while pyiwd.station_dic_by_path(path)['Scanning']:
            time.sleep(0.1)

    def test_station_connect_blocking(self):
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        nw_list = pyiwd.station_nws(path)
        this_nw = nw_list[0][0]
        that_nw = nw_list[1][0]
        print("connecting that nw", that_nw)
        pyiwd.nw_connect_blocking(that_nw)
        time.sleep(9)
        print("connected_nw", pyiwd.nw_dic_connected_to_dev(path))


    def test_station_connect_async(self):
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        nw_list = pyiwd.station_nws(path)
        this_nw = nw_list[0][0]
        that_nw = nw_list[1][0]
        self.handler_called = False
        print("connecting that nw", that_nw)
        pyiwd.nw_connect_async(that_nw, 
                                    self.reply_handler, self.error_handler)
        while not self.handler_called:
            main_context.iteration(False)

        print("connected_nw", pyiwd.nw_dic_connected_to_dev(path))

        print("connecting this nw", this_nw)
        pyiwd.nw_connect_blocking(this_nw)
        time.sleep(9)
        print("connected_nw", pyiwd.nw_dic_connected_to_dev(path))

    def test_rssi(self):
        name = pyiwd.dev_list()[0]["Name"]
        path = pyiwd.dev_path_by_name(name)
        nw_list = pyiwd.station_nws(path)
        this_nw = nw_list[0][0]
        rssi = pyiwd.station_rrsi(path, this_nw)
        print("rssi", rssi)


    def reply_handler(self):
        print("connect reply_handler")
        self.handler_called = True

    def error_handler(self, error):
        self.handler_called = True
        print("connect error_handler", error)




if __name__ == '__main__':
    unittest.main()


