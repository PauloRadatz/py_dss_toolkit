# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 01:09:28
 Project: py_dss_tools [set, 2021]
"""
from ReportFPDF import Report

report = Report(open_=True, font='Times', font_size=16, italic=False, bold=False, underline=False)
report.sample()
