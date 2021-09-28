# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 01:18:48
 Project: py_dss_tools [set, 2021]
"""
import os
import pathlib

from fpdf import FPDF


class Report(FPDF):

    def header(self):
        # Logo
        self.image('../../logo/EPRI.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, self.title, 1, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def __init__(self, **kwargs):
        self.font = 'Arial'
        self.font_size = 12
        self.open_ = True
        self.style = None
        self.italic = False
        self.bold = False
        self.underline = False
        self.title = "My Title"

        self.check_kwargs(**kwargs)

        # Report.df = dataframe
        super().__init__()

        self.alias_nb_pages()
        self.add_page()

        self.image("../../resources/header_cropped.jpg", 0, 0, 210)
        self.cell(0,10, "TITLE", 0, 0, 210)

    def sample(self):
        for i in range(1, 41):
            self.cell(0, 10, 'Printing line number ' + str(i), 0, 1)

        self.set_author("Ênio Rodrigues Viana")
        self.set_creator("Ênio Rodrigues Viana")

        # pdf.cell(60, 20, 'Powered by FPDF.', 0, 1, 'C')
        name = "tuto1.pdf"
        try:
            self.output('../../output/' + name, 'F')
            current_dir = pathlib.Path(__file__).parent.resolve()
            current_dir = current_dir.joinpath('../../output')
            if self.open_:
                os.startfile(current_dir.joinpath(name))
            else:
                print("Report generate succesfully!")
        except Exception as e:
            print(e)

    def check_kwargs(self, **kwargs):
        if 'italic' in kwargs:
            self.style = 'I'
        if 'bold' in kwargs:
            self.style = 'B'
        if 'underline' in kwargs:
            self.style = 'U'

        if 'font' in kwargs:
            self.font = kwargs.get('font')
        if 'font_size' in kwargs:
            self.font_size = kwargs.get('font_size')

        if 'title' in kwargs:
            self.title = kwargs.get('title')
