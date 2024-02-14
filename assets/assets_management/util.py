import io
import os
from datetime import date

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors


def retrieve_file_extension(file):
    return file.name.split(".")[-1].lower()


def check_aggregation_value(v):
    return v["total"] if v["total"] else 0


def calculate_expenses_totals(v1, v2):
    if v1 and v2:
        return v1 + v2
    elif v1 and not v2:
        return v1
    elif not v1 and v2:
        return v2
    else:
        return 0


def calculate_balance(income, expense):
    if income and expense:
        return income - expense
    elif income and not expense:
        return income
    elif not income and expense:
        return 0 - expense
    else:
        return 0


def get_month_total(qs, month):
    for item in qs:
        if item["date__month"] == month:
            return item["total"]


def fill_up_missing_months(qs):
    data = []
    months_in_qs = qs.values_list("date__month", flat=True).distinct()

    for month in range(1, 13):
        if month not in months_in_qs:
            data.append({"month": month, "total": 0})
        else:
            data.append({"month": month, "total": get_month_total(qs, month)})

    return data


def consolidate(gex, aex, inc, year):
    consolidated = {}
    metadata = {"total_income": 0, "total_expense": 0}
    for month in range(0, 12):
        consolidated[month + 1] = {
            "date": date(year, month + 1, 1),
            "income": inc[month]["total"],
            "expense": gex[month]["total"] + aex[month]["total"],
            "balance": inc[month]["total"]
            - (gex[month]["total"] + aex[month]["total"]),
        }
        metadata["total_income"] += inc[month]["total"]
        metadata["total_expense"] += gex[month]["total"] + aex[month]["total"]
    metadata.update({"balance": metadata["total_income"] - metadata["total_expense"]})

    return consolidated, metadata


def generate_annual_report_pdf(data, current_year, metadata):
    image = f"{os.getcwd()}/assets_management/static/replacements/irpf.jpg"
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColorRGB(0, 0, 102/256)

    p.drawImage(image, width / 2 - 100, height - 100, width=200, height=100)
    p.drawString(width / 2 - 55, height - 100, f"Documento Auxiliar {current_year}")

    HEADERS = ["Mês", "Entrada", "Saída", "Balanço"]

    COLS_WIDTH = [1.2*inch / 2, 1.2 * inch, 1.2 * inch, 1.2 * inch]
    TABLE_LENGTH = inch / 2 + 1.2 * inch + 1.2 * inch + 1.2 * inch

    TOTALS = [
        'Totais',
        f'R$ {metadata['total_income']:,}',
        f'R$ {metadata['total_expense']:,}',
        f'R$ {metadata['balance']:,}'
    ]

    m = []
    m.append(HEADERS)
    for key, value in data.items():
        row = None
        balance = f'R$ {value["income"] - value["expense"]:,}'
        row = [
            value["date"].strftime("%b"),
            f'R$ {value["income"]:,}',
            f'R$ {value["expense"]:,}',
            balance,
        ]
        m.append(row)
    m.append(TOTALS)

    t = Table(m, colWidths=COLS_WIDTH)
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    t.wrapOn(p, width / 2, height / 2)
    t.drawOn(p, (width-TABLE_LENGTH) / 2, height - 400)

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
