#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This example can be run safely as it won't change anything
in your box configuration."""

import logging

from aiosysbus import AIOSysbus
from aiosysbus.exceptions import AuthorizationError, NotOpenError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def demo() -> None:
    """Instantiate Livebox class."""
    lvbx = AIOSysbus(host="192.168.1.1", port="80", username="admin", password="xxxxxx")

    try:
        lvbx.connect()
    except AuthorizationError as err:
        logger.error(err)
        return
    except NotOpenError as err:
        logger.error(err)
        return

    # Fetch datas
    lvbx.deviceinfo.get_deviceinfo()
    lvbx.connection.get_data_MIBS()
    lvbx.connection.get_dsl0_MIBS()
    lvbx.system.get_guest()

    lip = lvbx.connection.get_lan_luckyAddrAddress()
    wip = lvbx.connection.get_data_luckyAddrAddress()

    if lip:
        logger.info("LAN IP Address: %s", str(lip["status"]))
    if wip:
        logger.info("WAN IP Address: %s", str(wip["status"]))

    # parameters = {
    #     "expression": {
    #         "eth": 'eth and .IPAddress!="" and .DeviceType!="" and .Active==true',
    #         "wifi": 'wifi and .IPAddress!="" and .Active==true',
    #     }
    # }

    # ~ parameters={"description":"FTP","persistent":"true","enable":"true",
    # "protocol":"6","destinationIPAddress":"192.168.1.250","internalPort":"21",
    # "externalPort":"21","origin":"webui","sourceInterface":"data","sourcePrefix":"",
    # "id":"FTP"}
    # ~ lvbx.nat.set_firewall_PortForwarding(parameters)
    lvbx.nat.get_firewall_PortForwarding()

    # Reboot
    # ~ lvbx.system.reboot()

    # Close the livebox session
    lvbx.close()


demo()
