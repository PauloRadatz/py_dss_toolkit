# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:02
 Project: py_dss_tools [set, 2021]
"""


class FMonitor:
    name = "FMonitor"
    name_plural = "FMonitors"
    columns = ['action', 'attack_defense', 'b_curt_ctrl', 'basefreq', 'cluster_num', 'comm_hide', 'comm_node_hide',
               'commdelayvector', 'commvector', 'egen', 'element', 'elemtableline', 'enabled', 'like', 'maxlocalmem',
               'mode', 'node_num', 'nodes', 'p_mode', 'p_sensor', 'p_trans_ref', 'ppolar', 'residual', 't_intvl_smpl',
               'terminal', 'total_clusters', 'up_dly', 'v_sensor', 'vipolar', 'virtual_ld_node:', 'volt_limits_pu']

    def __init__(self):
        self.__attack_defense = None
        self.__b_curt_ctrl = None
        self.__cluster_num = None
        self.__comm_hide = None
        self.__comm_node_hide = None
        self.__commdelayvector = None
        self.__commvector = None
        self.__egen = None
        self.__elemtableline = None
        self.__maxlocalmem = None
        self.__mode = None
        self.__node_num = None
        self.__nodes = None
        self.__p_mode = None
        self.__p_sensor = None
        self.__p_trans_ref = None
        self.__ppolar = None
        self.__residual = None
        self.__t_intvl_smpl = None
        self.__total_clusters = None
        self.__up_dly = None
        self.__v_sensor = None
        self.__vipolar = None
        self.__virtual_ld_node = None
        self.__volt_limits_pu = None

    @property
    def attack_defense(self):
        return self.__attack_defense

    @attack_defense.setter
    def attack_defense(self, value):
        self.__attack_defense = value

    @property
    def b_curt_ctrl(self):
        return self.__b_curt_ctrl

    @b_curt_ctrl.setter
    def b_curt_ctrl(self, value):
        self.__b_curt_ctrl = value

    @property
    def cluster_num(self):
        return self.__cluster_num

    @cluster_num.setter
    def cluster_num(self, value):
        self.__cluster_num = value

    @property
    def comm_hide(self):
        return self.__comm_hide

    @comm_hide.setter
    def comm_hide(self, value):
        self.__comm_hide = value

    @property
    def comm_node_hide(self):
        return self.__comm_node_hide

    @comm_node_hide.setter
    def comm_node_hide(self, value):
        self.__comm_node_hide = value

    @property
    def commdelayvector(self):
        return self.__commdelayvector

    @commdelayvector.setter
    def commdelayvector(self, value):
        self.__commdelayvector = value

    @property
    def commvector(self):
        return self.__commvector

    @commvector.setter
    def commvector(self, value):
        self.__commvector = value

    @property
    def egen(self):
        return self.__egen

    @egen.setter
    def egen(self, value):
        self.__egen = value

    @property
    def elemtableline(self):
        return self.__elemtableline

    @elemtableline.setter
    def elemtableline(self, value):
        self.__elemtableline = value

    @property
    def maxlocalmem(self):
        return self.__maxlocalmem

    @maxlocalmem.setter
    def maxlocalmem(self, value):
        self.__maxlocalmem = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def node_num(self):
        return self.__node_num

    @node_num.setter
    def node_num(self, value):
        self.__node_num = value

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, value):
        self.__nodes = value

    @property
    def p_mode(self):
        return self.__p_mode

    @p_mode.setter
    def p_mode(self, value):
        self.__p_mode = value

    @property
    def p_sensor(self):
        return self.__p_sensor

    @p_sensor.setter
    def p_sensor(self, value):
        self.__p_sensor = value

    @property
    def p_trans_ref(self):
        return self.__p_trans_ref

    @p_trans_ref.setter
    def p_trans_ref(self, value):
        self.__p_trans_ref = value

    @property
    def ppolar(self):
        return self.__ppolar

    @ppolar.setter
    def ppolar(self, value):
        self.__ppolar = value

    @property
    def residual(self):
        return self.__residual

    @residual.setter
    def residual(self, value):
        self.__residual = value

    @property
    def t_intvl_smpl(self):
        return self.__t_intvl_smpl

    @t_intvl_smpl.setter
    def t_intvl_smpl(self, value):
        self.__t_intvl_smpl = value

    @property
    def total_clusters(self):
        return self.__total_clusters

    @total_clusters.setter
    def total_clusters(self, value):
        self.__total_clusters = value

    @property
    def up_dly(self):
        return self.__up_dly

    @up_dly.setter
    def up_dly(self, value):
        self.__up_dly = value

    @property
    def v_sensor(self):
        return self.__v_sensor

    @v_sensor.setter
    def v_sensor(self, value):
        self.__v_sensor = value

    @property
    def vipolar(self):
        return self.__vipolar

    @vipolar.setter
    def vipolar(self, value):
        self.__vipolar = value

    @property
    def virtual_ld_node(self):
        return self.__virtual_ld_node

    @virtual_ld_node.setter
    def virtual_ld_node(self, value):
        self.__virtual_ld_node = value

    @property
    def volt_limits_pu(self):
        return self.__volt_limits_pu

    @volt_limits_pu.setter
    def volt_limits_pu(self, value):
        self.__volt_limits_pu = value
