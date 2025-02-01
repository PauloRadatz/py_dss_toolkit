# -*- coding: utf-8 -*-
# @Author  : Arthur Lopes Morais Arantes
# @Email   : arthureletricauftm@gmail.com
# Date     : 25/11/2024
# @File    : SystemPhotovoltaic.py
# @Software: PyCharm


import warnings as ws

from py_dss_interface import DSS
import pandas as pd


class SystemPhotovoltaic:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._System_Photovoltaic = pd.DataFrame()

    @property
    def System_Photovoltaic(self) -> pd.DataFrame:
        return self.__photovoltaic() #Todo - it should return a dataframe with the element names

    def __photovoltaic(self):
        photovoltaicc_system_info = []
        dss.pvsystems.first()
        data = []
        while True:

            #Pmpp do PVSystem
            pmpp_pvsystem     = float(dss.pvsystems.pmpp)
            pmpp_pvsystem_new = pmpp_pvsystem
            ZERO = float(0.0)

            #Informação barramento 1
            bus= str(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.bus1"))
            #Informação nome da barra, nós
            bus_name, bus_node = bus.split(".")[0:1], bus.split(".")[1:]
            #Armazena os nós sem ser aterrado ou isolado
            bus_node_filter = ([node_bus for node_bus in bus_node if node_bus in ['1', '2', '3']])
            len_bus_node_filter =  len(bus_node_filter)

            #Verifica a quantidade de fases
            phases = str(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.phases"))
            phasesnodes_new  = phases

            #Verifica a conexão (Delta ou Estrela)
            connection = str(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.conns"))
            connection_new =connection

            fp     = dss.pvsystems.pf
            fp_new = fp

            cutin = str(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.%cutin"))
            cutin_new = cutin
            cutout = str(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.%cutout"))
            cutout_new = cutout
            Teste = True

            warning = ''


            irradiance  = dss.pvsystems.irradiance
            temperature = float(dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.Temperature"))
            irradiance_new, temperature_new = irradiance,temperature


            tdaily_curve = (dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.Tdaily"))
            tdaily_curve_new = tdaily_curve

            tyearly_curve = (dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.Tyearly"))
            tyearly_curve_new = tyearly_curve

            eff_Curve = (dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.effCurve"))
            eff_Curve_new = eff_Curve

            pt_curve = (dss.text(f"? PVSYSTEM.{dss.pvsystems.name}.Pt-Curve"))
            pt_curve_new = pt_curve


            if pmpp_pvsystem == ZERO:
                Teste = False
                pmpp_pvsystem_new = "pmpp > 0"
                warning = f"There are missing input data for the PV System called {dss.pvsystems.name}. Solution: Add missing data"
                ws.warn(warning, UserWarning)

            #CHECK DIFFERENCE BETWEEN BUS NODE AND PHASES IN PV SYSTEM
            if int(phases) > len_bus_node_filter:
                Teste = False
                phasesnodes_new = len_bus_node_filter
                warning = f"Other solution: Number of nodes are wrong. Add other nodes -Total: {int(phases) - len_bus_node_filter}"
                ws.warn(warning, UserWarning)

            #CHECK DIFFERENCE BETWEEN BUS NODE AND PHASES IN PV SYSTEM
            if int(phases) < len_bus_node_filter:
                Teste = False
                phasesnodes_new = len_bus_node_filter
                warning = f"Other solution: Number of nodes are wrong. Delete other nodes - Total: {-int(phases) + len_bus_node_filter}"
                ws.warn(warning, UserWarning)

            #CHECK NEUTRAL CONNECTION
            if len_bus_node_filter == 3:
                if connection == 'wye' and ('0' not in bus_node or '4' not in bus_node):
                    Teste = False
                    connection_new = "0 ou 4"
                elif connection == "delta":
                    continue

            #CHECK FP
            if fp == 0.0:
                Teste = False
                fp_new = "fp > 0"
                warning = "Add fp for PV System"
                ws.warn(warning, UserWarning)

            #CHECK TEMPERATURE AND IRRADIANCE - carelessly typed
            if (irradiance < 0 ):
                Teste = False
                irradiance_new = (-1)*irradiance
            if temperature < 0:
                Teste = False
                temperature_new = (-1)*temperature

            #CHECK CUTIN AND CUTOUT
            if cutin < cutout:
                Teste = False
                cutin_new  = "cutin > cutout"
                cutout_new = "cutout < cutin"

            if (tdaily_curve == ""):
                Teste = False
                tdaily_curve_new = "Add tdaily curve"
                warning = "Desconsider if there tyearly"

            if (tyearly_curve == ""):
                Teste = False
                tyearly_curve_new = "Add tyearly curve"
                warning = "Desconsider if there tdaily"

            if (eff_Curve == ""):
                Teste = False
                eff_Curve = "Add effCurve curve"
                ws.warn(warning, UserWarning)

            if (pt_curve == ""):
                Teste = False
                pt_curve_new = "Add PtCurve curve"
                ws.warn(warning, UserWarning)

            if dss.pvsystems.next() == 0:
                break

            if Teste == False:
                data.append(
                    [dss.pvsystems.name, pmpp_pvsystem, pmpp_pvsystem_new, phases, phasesnodes_new, connection, connection_new, fp, fp_new, irradiance , irradiance_new, temperature, temperature_new, cutin, cutin_new, cutout, cutout_new, tdaily_curve, tdaily_curve_new, tyearly_curve, tyearly_curve_new, pt_curve, pt_curve_new, eff_Curve, eff_Curve_new])

        return pd.DataFrame(data, columns=["PVSystem", 'Pmpp set', "Pmpp new", "Phases set", "Phases new", "Connection set", "Connection new", "fp set", "fp new", "Irradiance set", "Irradiance new", "temperature set", "temperature new", "cutin set", "cutin new", "cutout set", "cutout new", "tdaily set", "tdaily new", "tyearly set", "tyearly new", "pt curve set", "pt_curve new", "eff_Curve set", "eff_Curve new"])

if __name__ == '__main__':
    import os
    import pathlib
    dss = DSS()
    script_path = os.path.dirname(os.path.abspath(__file__))

    dss_file = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "RITQ1305", "DU_1_Master_391_ITQ_RITQ1305.dss")
    dss.text(f"compile [{dss_file}]")

    # remove meters if present in dss files
    for name in dss.meters.names:
        dss.text(f"disable energymeter.{name}")

    #
    dss.text("New Tshape.MyTemp1 npts=24 interval=1 temp=[25, 25, 25, 25, 25, 25, 25, 25, 35, 40, 45, 50, 60, 60, 55, 40, 35, 30, 25, 25, 25, 25, 25, 25]")
    # Adding Problem (Input Power is missing)
    dss.text("New PVsystem.PVSYSTEM_Problem1 phases=2 bus1=BT3673594940205485IT05.1.2.4 conn=Delta kv=0.22 pf=0.95 pmpp=0.0 kva=1.389 irradiance=1.0 temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria")

    # Adding Problem (Bus1 is incompatible with the number of phases)
    dss.text("New PVsystem.PVSYSTEM_Problem2 phases=1 bus1=BT3673594940205485IT05.1.2.4 conn=Delta kv=0.22 pf=0.95 pmpp=0.0 kva=1.389 irradiance=1.0 temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria")

    # Adding Problem (Different Sequence)
    dss.text("New PVsystem.PVSYSTEM_Problem3 phases=2 bus1=BT3673594940205485IT05.2.1.4 conn=Delta kv=0.22 pf=0.95 pmpp=0.0 kva=1.389 irradiance=1.0 temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria ")

    # Adding Problem (FP)
    dss.text("New PVsystem.PVSYSTEM_Problem4 phases=2 bus1=BT3673594940205485IT05.2.1.4 conn=Delta kv=0.22 pf=0.0 pmpp=5 kva=1.389 irradiance=1.0 temperature=25 %cutin=0.1 %cutout=0.1 P-TCurve=MyPvsT Daily=PVIrrad_diaria ")

    # Adding Problem (CUTIN AND CUTOUT)
    #dss.text("New PVsystem.PVSYSTEM_Problem5 phases=2 bus1=BT3673594940205485IT05.2.1.4 conn=Delta kv=0.22 pf=0.0 pmpp=5 kva=1.389 irradiance=1.0 temperature=25 %cutin=0.1 %cutout=0.5 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp")

    result_1 = SystemPhotovoltaic(dss).System_Photovoltaic
    print(result_1)
