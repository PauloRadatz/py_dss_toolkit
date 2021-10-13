# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 03/10/2021 at 02:34:45
 Project: py-dss-tools [out, 2021]
"""


class MyException(Exception):
    pass


class PDElementError(MyException):

    def __init__(self, name, message):
        self.message = "\n\nPAY ATTENTION HERE: An error occur when you are work in element " + name + ". Your error " \
                                                                                                       "was: " + message
        super().__init__(self.message)
