# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 08/10/2021 at 20:49:28
 Project: py-dss-tools [out, 2021]
"""
from py_dss_tools.model.pdelement import Reactor
from py_dss_tools.service.pdelement.ReactorService import ReactorService


class ReactorController:

    @staticmethod
    def save(reactor: Reactor):
        ReactorService.save(reactor)
