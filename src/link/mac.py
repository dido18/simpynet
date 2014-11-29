# -*- coding: utf-8 -*-
"""
This module contains mac (Medium Access Control)
"""


class Mac():
    """
    MAC (Medium Access Control)
    """
    def __init__(self, mac = "ff:ff:ff:ff:ff:ff"):
        self.mac = mac.lower()
        
        
    def __eq__(self, m):
        return self.mac == m.mac
        
        
    def __str__(self):
        return self.mac
        
    
    def __repr__(self):
        return self.mac
        
    @staticmethod
    def get_broadcast():
        return "ff:ff:ff:ff:ff:ff"
    
    