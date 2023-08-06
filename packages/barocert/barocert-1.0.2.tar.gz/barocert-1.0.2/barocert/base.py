# -*- coding: utf-8 -*-
# Module for barocertService API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# 
# Author : linkhub dev
# Written : 2023-03-08
# Updated : 2023-06-13
# Thanks for your interest.

class BarocertException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message