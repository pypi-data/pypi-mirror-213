#!/usr/bin/python3
"""
pyiwd: A graphical frontend for iwd, Intel's iNet Wireless Daemon.
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
import sys
import time
import dbus
import dbus.service
import json
from dbus.mainloop.glib import DBusGMainLoop


IWD_PATH = "/net/connman/iwd"
IWD_SERVICE = "net.connman.iwd"
IWD_OBJECT_IF = "org.freedesktop.DBus.ObjectManager"
IWD_OBJECT_PATH = "/"
IWD_ADAPTER_IF = "net.connman.iwd.Adapter"
IWD_AGENT_IF = "net.connman.iwd.Agent"
IWD_AGENT_MGR_IF = "net.connman.iwd.AgentManager"
IWD_DEVICE_IF = "net.connman.iwd.Device"
IWD_KNOWN_NW_IF = "net.connman.iwd.KnownNetwork"
IWD_NW_IF = "net.connman.iwd.Network"
IWD_STATION_IF =" net.connman.iwd.Station"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"

PYTHONDICS = 1



def _filter_on_path(objects, path):
    " Yields the dictionary objects matching a path "
    for elem in objects:
        for elem2 in objects[elem]:
            dic2 = objects[elem]
            if elem2 == path:
                yield(dic2[elem2])
def _list(objects, key, sortkey=None):
    "returns a list based on the DBus key, and sorted in sortkey, if provided "
    lst = list(_filter_on_path(objects, key))
    if sortkey:
        try:
            lst.sort(key=lambda item: item.get(sortkey))
        except Exception as e:
            print("Could not sort:", e)
    return lst

def _station_if(bus, device_key):
    "returns a dbus station interface object for a device"
    return dbus.Interface(bus.get_object(objectIwd, device_key),iwdStation)

def _network_if(bus, network_key):
    "returns a dbus network interface object for a network"
    return dbus.Interface(bus.get_object(objectIwd, network_key),
                          iwdNetwork)

def _known_network_if(bus, network_key):
    "returns a dbus known-network interface object for a known-network"
    return dbus.Interface(bus.get_object(objectIwd, network_key),
                          iwdKnownNetwork)

def _agent_manager_if(bus):
    "returns a dbus agent_manager interface object"
    return dbus.Interface(bus.get_object(objectIwd, objectIwdPath),
                          iwdAgentManager)

def _get_station_props(bus, objects, device_key, network_name):
    station_if = _station_if(bus, device_key)
    for path, rssi in station_if.GetOrderedNetworks():
        properties = objects[path][iwdNetwork]
        if properties["Name"] == network_name:
            properties["Signalstrength"] = rssi
            #print("station_props:", properties)
            return properties
    return None

def _get_key_by_name(objects, name, recordtype):
    for elem in objects:
        dic2 = objects[elem]
        for elem2 in dic2:
            #if (elem2 == iwdDevice and 
            if (elem2 == recordtype and 
                dic2[elem2]["Name"] == name):
                return elem
    print("Oooops device_key for name", name, "not found")
    return None

class _If(dbus.Interface):
    """A generic IWD interface class.
    It needs the path (preferred) or the name of the object"""
    def __init__(self, bus, interface, path=None, dic=None):
        assert (path or dic), "Need path or dic"
        if not path:
            obj_if = ObjectIf(bus)
            path = obj_if.path_by_interface_and_name(interface, dic["Name"])
        super().__init__(bus.get_object(IWD_SERVICE, path), interface)
        self.interface = interface
        self.path = path
        #dic = obj_if.dic_by_path_and_interface(path, interface)
        if dic:
            for key in dic:
                print("setattr:", key, dic[key])
                setattr(self, key, dic[key])

    def path():
        return self.path

    def interface():
        return self.interface

class ObjectIf(_If):
    """An iwd object interface class
    Available dbus function: GetManagedObjects()"""
    def __init__(self, bus):
        super().__init__(bus, IWD_OBJECT_IF, path=IWD_OBJECT_PATH)
        self.refresh_cache()

    def refresh_cache(self):
        self.objects = self.GetManagedObjects()
        if PYTHONDICS:
            jsonstr = json.dumps(self.objects)
            #print(json.dumps(objects, indent=2))
            self.objects = json.loads(jsonstr)

    def device_list(self):
        return _list(self.objects, IWD_DEVICE_IF, "Name")

    def adapter_list(self):
        return _list(self.objects, IWD_ADAPTER_IF, "Name")

    def station_list(self):
        return _list(self.objects, IWD_STATION_IF)

    def network_list(self):
        return _list(self.objects, IWD_NW_IF, "Name")

    def knownnetwork_list(self):
        return _list(self.objects, IWD_KNOWN_NW_IF, "LastConnectedTime")

    def path_by_interface_and_name(self, interface, name):
        for elem in self.objects:
            dic2 = self.objects[elem]
            for elem2 in dic2:
                if (elem2 == interface and
                    dic2[elem2]["Name"] == name):
                    return elem
        print("Path for interface", interface, "and name", name, "not found")
        return None

    def dic_by_path_and_interface(self, path, interface):
        return self.objects[path][interface]


class Adapter(_If):
    """An iwd adapter interface class
    Available properties: Powered, Name, Model, Vendor, SupportedModes"""
    def __init__(self, bus, objects = None, path=None,
                 adapter_dic = None, name=None):
        super().__init__(bus, IWD_ADAPTER_IF, objects,
                         path=path, dic=adapter_dic, name=name)

class Device(_If):
    """An iwd device interface class
    Available properties: Name, Address, Adapter, Mode"""
    def __init__(self, bus, path=None, dic=None):
        super().__init__(bus, IWD_DEVICE_IF, path=path, dic=dic)

class Network(_If):
    """An iwd networ interface class
    Available methods: Connect
    Available properties: Name, Connected, Device, Type, KnownNetwork"""
    def __init__(self, bus, objects, path=None,
                 network_dic=None, name=None):
        super().__init__(bus, IWD_NW_IF, objects=objects,
                         path=path, dic=network_dic, name=name)

class Station(_If):
    """An iwd station interface class
    Available methods: Scan, Disconnect,
        GetOrderedNetworks(network, signal strenght),
        GetHiddenAccessPoints,
        ConnectHiddenNetwork,
        RegisterSignalLevelAgent
        UnregisterSignalLevelAgent
    Available properties: State, ConnectedNetwork, Scanning """
    def __init__(self, bus, objects, path=None):
        super().__init__(bus, IWD_STATION_IF, path, objects=objects)

class AgentManager(_If):
    """An agent manager interface object
    Available methods: RegisterAgent, UnregisterAgent"""
    def __init__(self, bus):
        super().__init__(bus, IWD_AGENT_MGR_IF, IWD_PATH)


class Agent(dbus.service.Object):
    "Agent class to handle callbacks in case iwd needs a user entry passwd"
    def __init__(self, bus, passwd_entry_callback):
        #self._bus = dbus.SystemBus()
        self._bus = bus
        self._path = '/test/agent/' + str(int(round(time.time() * 1000)))
        dbus.service.Object.__init__(self, self._bus, self._path)
        self.passwd_entry_callback = passwd_entry_callback

    @property
    def path(self):
        return self._path

    @dbus.service.method(IWD_AGENT_IF, in_signature='', out_signature='')
    def Release(self):
        "So far I have not seen this being called"
        print("Agent released")

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s')
    def RequestPassphrase(self, path):
        "This one gets called when trying to connect to a new network"
        #print("Agent: RequestPassphrase", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s')
    def RequestPrivateKeyPassphrase(self, path):
        "So far I have not seen this being called"
        print("RequestPrivateKeyPassphrase", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='o', out_signature='s,s')
    def RequestUserNameAndPassword(self, path, ):
        "So far I have not seen this being called"
        print("RequestUserNameAndPassword", path)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='os', out_signature='s')
    def RequestUserPassword(self, path, username):
        "So far I have not seen this being called"
        print("RequestUserPassword", path, username)
        return self.passwd_entry_callback(path)

    @dbus.service.method(IWD_AGENT_IF, in_signature='s')
    def Cancel(self, reason ):
        "So far I have not seen this being called"
        print("Cancel", reason)
        return

def bus():
    return dbus.SystemBus()

def register_properties_callback(fn):
    self.bus.add_signal_receiver(fn,
                        bus_name=IWD_SERVICE,
                        dbus_interface=IWD_OBJECT_IF,
                        signal_name="PropertiesChanged",
                        path_keyword="path")








# don'r use....
class ____IwdObj():
    def __init__(self, passwd_entry_callback):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.objects = _get_objects(self.bus)
        agent = Agent(self.bus, passwd_entry_callback)
        agent_manager_if = _agent_manager_if(self.bus)
        agent_manager_if.RegisterAgent(agent.path)

    def register_properties_callback(self, fn):
        "Can be used by an appication to be called when props hve changed"
        self.bus.add_signal_receiver(fn,
                            bus_name=objectIwd,
                            dbus_interface=dbusProperties,
                            signal_name="PropertiesChanged",
                            path_keyword="path")

    def refresh_objects(self):
        "Refreshes the iwd object cache"
        self.objects = _get_objects(self.bus)

    def start_scan(self, path):
        "starts a scan for a device"
        station_if = _station_if(self.bus, path)
        try:
            station_if.Scan()
        except dbus.exceptions.DBusException as e:
            print("Dbus exception:", e.args[0])


    def get_device_by_key(self, path):
        return self.objects[path][iwdDevice]

    def get_adapter_by_key(self, path):
        return self.objects[path][iwdAdapter]

    def get_station_by_key(self, path):
        return self.objects[path][iwdStation]

    def get_network_by_key(self, path):
        return self.objects[path][iwdNetwork]

    def get_device_key_by_name(self, device_name):
        "Retrieves a device name's object key (or path)"
        return _get_key_by_name(self.objects, device_name, iwdDevice)

    def get_adapter_key_by_name(self, adapter_name):
        "Retrieves a adapter name's object key (or path)"
        return _get_key_by_name(self.objects, adapter_name, iwdAdapter)

    def get_stationkey_by_name(self, station_name):
        "Retrieves a station name's object key (or path)"
        return _get_key_by_name(self.objects, station_name, iwdStation)

    def get_knownnetwork_key_by_name(self, knownnetwork_name):
        "Retrieves a known network  name's object key (or path)"
        return _get_key_by_name(self.objects,
                                knownnetwork_name, iwdKnownNetwork)

    def get_network_key_by_name(self, network_name):
        "Retrieves a network  name's object key (or path)"
        return _get_key_by_name(self.objects, network_name, iwdNetwork)

    def forget_network(self, networkname):
        "Instructs iwd to forget a network"
        network_key = self.get_knownnetwork_key_by_name(networkname)
        known_network_if = _known_network_if(self.bus, network_key)
        known_network_if.Forget()
        self.refresh_objects()

    def adapter_list(self):
        return _list(self.objects, iwdAdapter, "Name")

    def device_list(self):
        return _list(self.objects, iwdDevice, "Name")

    def station_list(self):
        return _list(self.objects, iwdStation)

    def network_list(self):                 # order by signal strength?
        return _list(self.objects, iwdNetwork, "Name")

    def knownnetwork_list(self):
        return _list(self.objects, iwdKnownNetwork, "LastConnectedTime")

    def device_network_list(self, device_key):
        """Retrieves the networks that are available on a specific device"""
        network_list = self.network_list()
        for network in network_list:
            network_path = network["Device"]
            if network_path != device_key:
                network_list.remove(network)
        return network_list

    def adapter_device_list(self, adapter):
        device_list = self.device_list()
        for device in device_list:
            adapter_path = device["Adapter"]   #
            if self.objects[adapter_path][iwdAdapter] != adapter:
                device_list.remove(device)
        return device_list

    def get_station_props(self, active_device, active_network):
        "Retrieves a station's properties"
        return _get_station_props(self.bus, self.objects,
                                  active_network["Device"],
                                  active_network["Name"])

    def connect_network(self, network):
        "Connects to a network"
        network_key = self.get_network_key_by_name(network["Name"])
        network_if = _network_if(self.bus, network_key)
        try: 
            network_if.Connect(
                reply_handler = self.connect_reply_handler,
                error_handler = self.connect_error_handler)
        except Exception as e:
            print("Connect exception:", e)

    def connect_reply_handler(self):
        "Called on connect success"
        #print("connect_reply_handler")

    def connect_error_handler(self, error):
        "Called on connect failure"
        #print("connect_error_handler", error)

    def disconnect_network(self, network):
        "Disconnects from a network, or rather a device"
        station_if = _station_if(bus, network["Device"])
        station_if.Disconnect()

