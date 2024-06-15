import io
import os
from decimal import Decimal

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

PAGE_WIDTH, PAGE_HEIGHT = A4


class customPdf:
    def __init__(self, incomes, expenses, expenses_qs, year):
        self.PAGE_WIDTH = A4[1]
        self.PAGE_HEIGHT = A4[0]
        self.incomes = incomes
        self.expenses = expenses
        self.expenses_qs = expenses_qs
        self.year = year
        self.filename = "Informe de Rendimentos"
        self.logo = f"{os.getcwd()}/assets_management/static/replacements/logo.png"
        self.INCOME_HEADERS = [
            "Mês",
            "Entrada",
            "Despesas",
            "Total",
            "Aliquota",
            "Bruto",
            "Dedução",
            "Liquido",
        ]
        self.EXPENSE_HEADERS = ["Data", "Descrição", "Imóvel", "Valor"]
        self.table_style = TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )

    def _first_page(self, canvas, doc):
        canvas.saveState()
        canvas.drawImage(
            self.logo,
            self.PAGE_WIDTH / 2 - 100,
            self.PAGE_HEIGHT / 2,
            width=200,
            height=300,
            mask="auto",
        )
        canvas.drawString(
            self.PAGE_WIDTH / 2 - 80,
            self.PAGE_HEIGHT / 2,
            f"Informe de Rendimentos {self.year}",
        )
        canvas.restoreState()

    def _later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.drawImage(
            self.logo,
            self.PAGE_WIDTH / 2 - 30,
            self.PAGE_HEIGHT - 100,
            width=60,
            height=90,
            mask="auto",
        )
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(inch, 0.75 * inch, "Página %d" % doc.page)
        canvas.restoreState()

    def build(self):
        COLS_WIDTH = [1.2 * inch / 2, 1.2 * inch, 1.2 * inch, 1.2 * inch]

        styles = getSampleStyleSheet()
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=(A4[1], A4[0]))
        story = [PageBreak(), Spacer(1, 0.5 * inch)]
        heading = ParagraphStyle(
            "asset_name_paragraph",
            alignment=1,
            parent=styles["Heading1"],
            spaceBefore=0,
        )
        subtext = ParagraphStyle(
            "asset_tenant_paragraph",
            alignment=1,
            parent=styles["Heading2"],
            spaceBefore=0,
        )

        text = "<strong>Rendimentos</strong>"
        p = Paragraph(text, heading)
        story.append(p)
        story.append(Spacer(1, 0.5 * inch))

        data = []
        data.append(self.INCOME_HEADERS)
        tax_total = 0
        for index, el in enumerate(self.incomes):
            month, extended = get_month_name(el["month"])
            income_per_owner = el["total"] / 2
            expense_per_owner = (self.expenses[index]["total"] / 2) * -1
            month_total = Decimal(income_per_owner) + Decimal(expense_per_owner)
            tax_rate, deduction = get_tax_rate(month_total)
            tax_value = (Decimal(income_per_owner) * Decimal(tax_rate)) / 100
            reduced_tax = tax_value - Decimal(deduction)
            tax_total += reduced_tax
            row = [
                month,
                f"R$ {income_per_owner:,.2f}",
                f"R$ {expense_per_owner:,.2f}",
                f"R$ {month_total:,.2f}",
                f"{tax_rate} %",
                f"R$ {tax_value:,.2f}",
                f"R$ {deduction:,.2f}",
                f"R$ {reduced_tax:,.2f}",
            ]
            data.append(row)
        data.append(["-", "-", "-", "-", "-", "-", "-", f"R$ {tax_total:,.2f}"])
        t = Table(data, colWidths=COLS_WIDTH)
        t.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                    ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ]
            )
        )
        story.append(t)
        story.append(PageBreak())
        story.append(Spacer(1, 0.5 * inch))

        text = "Despesas Discriminadas"
        p = Paragraph(text, heading)
        story.append(p)
        story.append(Spacer(1, 0.1 * inch))

        text = "Reparo e Manutenção"
        p = Paragraph(text, subtext)
        story.append(p)
        story.append(Spacer(1, 0.3 * inch))

        data = []
        data.append(self.EXPENSE_HEADERS)
        total = 0
        for i in range(1, 13):
            expense_per_month = self.expenses_qs.filter(date__month=i)

            if expense_per_month:
                month_total = 0
                for el in expense_per_month:
                    expense_per_owner = el.value / 2
                    row = [
                        el.date,
                        el.description,
                        el.asset.name,
                        f"R$ {expense_per_owner:,.2f}",
                    ]
                    month_total += expense_per_owner
                    total += expense_per_owner
                    data.append(row)
                month, extended_name = get_month_name(i)
                data.append([extended_name, "Total", "-", f"R$ {month_total:,.2f}"])

        data.append(["-", "-", "-", f"R$ {total:,.2f}"])
        t = Table(data)
        t.setStyle(self.table_style)
        story.append(t)
        story.append(PageBreak())

        doc.build(story, onFirstPage=self._first_page, onLaterPages=self._later_pages)
        buffer.seek(0)
        return buffer


def get_month_name(month_number):
    match month_number:
        case 1:
            return "Jan", "Janeiro"
        case 2:
            return "Fev", "Fevereiro"
        case 3:
            return "Mar", "Março"
        case 4:
            return "Abr", "Abril"
        case 5:
            return "Mai", "Maio"
        case 6:
            return "Jun", "Junho"
        case 7:
            return "Jul", "Julho"
        case 8:
            return "Ago", "Agosto"
        case 9:
            return "Set", "Setemro"
        case 10:
            return "Out", "Outubro"
        case 11:
            return "Nov", "Novembro"
        case 12:
            return "Dez", " Dezembro"


def get_tax_rate(value):
    if value <= 2112:
        return 0, 0
    if value >= 2112.01 and value <= 2826.65:
        return 7.5, 158.4
    if value >= 2826.55 and value <= 3751.06:
        return 15, 370.4
    if value >= 3751.07 and value <= 4664.68:
        return 22.5, 661.73
    if value >= 4664.69:
        return 27.5, 884.96
