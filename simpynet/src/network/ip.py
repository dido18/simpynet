# -*- coding: utf-8 -*-
"""
This module contains the IP (Internet Protocol) Address.
"""

class IP():
    """
    IP Address
    """
    def __init__(self, ip="255.255.255.255" ):
        self.ip = ip


    def __eq__(self, i):
        return self.ip == i.ip


    def __str__(self):
        return self.ip


    def __repr__(self):
        return self.ip

    @staticmethod
    def get_broadcast():
        return "255.255.255.255"
