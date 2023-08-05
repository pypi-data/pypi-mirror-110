# -*- coding: utf-8 -*-

import openpyxl
import os

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table

from ossreport.proto.proto import Component, File, Level, Risk


risk_head = {
    "A": Risk.__name__.capitalize(),
    "B": Level.CRITICAL,
    "C": Level.HIGH,
    "D": Level.MEDIUM,
    "E": Level.LOW,
    "F": Level.NONE,
}

component_head = {
    "A": Component.COMPONENT,
    "B": Component.SOURCE,
    "C": Component.MATCH_TYPE,
    "D": Component.USAGE,
    "E": Component.LICENSE,
    "F": Component.SECURITY_RISK,
    "G": Component.OPERATIONAL_RISK,
}

file_head = {
    "A": File.ID,
    "B": File.NAME,
    "C": File.LINES,
    "D": File.OSS_LINES,
    "E": File.MATCHED,
    "F": File.PURL,
    "G": File.VENDOR,
    "H": File.COMPONENT,
    "I": File.VERSION,
    "J": File.LATEST,
    "K": File.URL,
    "L": File.RELEASE_DATE,
    "M": File.FILE,
    "N": File.DEPENDENCIES,
    "O": File.LICENSES,
    "P": File.VULNERABILITIES,
}


class PrinterException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Printer(object):
    def __init__(self, risks, components, files, name):
        self._risks = risks
        self._components = components
        self._files = files
        self._name = name

    def _pdf(self):
        def _styling_title(style):
            return style["Title"]

        def _styling_head(style):
            return style["Heading3"]

        def _styling_table():
            return [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("FONTSIZE", (0, 1), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]

        def _write_table(head, data, style):
            content = [[head[key] for key in sorted(head.keys())]]
            for _, val in data.items():
                for v in val:
                    buf = [v[head[_k]] for _k in sorted(head.keys())]
                    content.append(buf)
            return Table(data=content, style=style, colWidths=["*"])

        stylesheet = getSampleStyleSheet()
        story = [
            Paragraph("SecTrend SCA Report", _styling_title(stylesheet)),
            Paragraph("", _styling_head(stylesheet)),
            _write_table(risk_head, self._risks, _styling_table()),
            Paragraph("", _styling_head(stylesheet)),
            _write_table(component_head, self._components, _styling_table()),
        ]
        doc = SimpleDocTemplate(self._name)
        doc.build(story)

    def _xlsx(self):
        def _styling_head(sheet, head):
            for item in head.keys():
                sheet[item + "1"].alignment = openpyxl.styles.Alignment(
                    horizontal="center", shrink_to_fit=True, vertical="center"
                )
                sheet[item + "1"].font = openpyxl.styles.Font(bold=True, name="Calibri")
            sheet.freeze_panes = sheet["A2"]

        def _styling_content(sheet, head, rows):
            for key in head.keys():
                for row in range(rows):
                    sheet[key + str(row + 2)].alignment = openpyxl.styles.Alignment(
                        horizontal="center", vertical="center"
                    )
                    sheet[key + str(row + 2)].font = openpyxl.styles.Font(
                        bold=False, name="Calibri"
                    )

        def _write_table(book, head, data):
            sheet = book.create_sheet()
            sheet.append([head[key] for key in sorted(head.keys())])
            head_len = 0
            for key, val in data.items():
                sheet.title = key
                for v in val:
                    buf = [v[head[_k]] for _k in sorted(head.keys())]
                    head_len = len(buf)
                    sheet.append(buf)
            _styling_head(sheet, head)
            _styling_content(sheet, head, head_len)

        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        _write_table(wb, risk_head, self._risks)
        _write_table(wb, component_head, self._components)
        _write_table(wb, file_head, self._files)
        wb.save(filename=self._name)

    def run(self):
        func = Printer.__dict__.get(
            os.path.splitext(self._name)[1].replace(".", "_"), None
        )
        if func is not None:
            func(self)
