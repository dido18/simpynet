# -*- coding: utf-8 -*-
"""
This module contains the most basic type of data
"""

class Databits():
    """
    Most basic type of data
    """

    def __init__( self , size ):
        self.size=size
        self.has_error=False


    def __len__( self ):
        return self.size


    def  set_error(self, boolean):
         self.has_error=boolean
         return self
