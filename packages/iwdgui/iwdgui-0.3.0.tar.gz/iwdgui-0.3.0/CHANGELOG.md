# Iwdgui changelog

## 0.3.0

Release date: 11-JUN-2023

Main engancements:

- Ad-hoc, and access-point modes are now supported
- The modes off, station, ad-hoc, access-point are selected using radio buttons
- Connecting to a hidden network is now done through an edit option in the
  combobox for the active connection. Pin-entry and push-button connections
  are already foreseen to be done in the same manner
- Password entry fields now have a show/hide icon
- Handle cards that do not provide model information

Compatibility is now set to Python 3.10 and 3.11, not for older versions.

## 0.2.0

Release date: 8-AUG-2021

Main enhancements:

- Multiple interfaces are now fully supported. Each interface has its own tab.
- The information shown is now more user friendly, e.g.
  signal strength has been converted from "-4700 dBm" to "Strong",
  network security indication from "psk" to "Pre-shared key", or "WPA2-Personal"
- With an advanced viewing mode (Menu/Application/Advanced) detailed
  information regarding the radio interface and the signal strength is shown.
- Iwdgui can now connect to a hidden network.
- Auto connect can be toggled for known networks.

Please refer for a full list to the milestone 0.2.0
[issue list](https://gitlab.com/hfernh/iwdgui/-/milestones/1).


## 0.1.0

Release date: 14-JUL-2021

Initial release.

- Works for station mode only. Access Point or Ad-Hoc mode not supported yet.
- Supports selecting different interfaces, and networks using combo boxes.


Known issues:

- multiple interfaces don't work well.

