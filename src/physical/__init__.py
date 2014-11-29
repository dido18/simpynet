# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:28:27 2014

@author: unkown
"""
from databits import Databits
from link_agent import Link
from link_agent import PointToPoint
from hub import Hub


def plug(Object1, Object2):
    """
    connect(Object1, Object2) - add the handlers to both the Object1 and 
    Object2
    """
    Object1.add_handler(repr(Object2), Object2.get_handler())
    Object2.add_handler(repr(Object1), Object1.get_handler())
    
    
def unplug(Object1, Object2):
    """
    disconnect(Object1, Object2) - remove the handlers from both Object1 and 
    Object2
    """
    Object1.remove_handler(repr(Object2))
    Object2.remove_handler((repr(Object1)))