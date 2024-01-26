from datetime import date
import os
from decimal import Decimal

from fpdf import FPDF  # https://pyfpdf.readthedocs.io/en/latest/index.html


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


def create_annual_report_pdf(data, year):
    filename = f"AUXILIAR_IRPF_{year}.pdf"

    pdf = FPDF(orientation="P", format="A4")
    pdf.add_page()
    image_path = f"{os.getcwd()}/assets_management/static/replacements/irpf.jpg"
    pdf.image(image_path, 75, 0, 45, 30)
    pdf.ln(15)

    pdf.set_text_color(0, 0, 77)
    pdf.set_font("Arial", "B", 15)
    pdf.cell(180, 10, "Documento Auxiliar", 0, 1, "C")
    pdf.cell(180, 10, f"{year}", 0, 1, "C")
    pdf.ln(13)

    pdf.set_font("Arial", "B", 14)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)

    pdf.cell(60, 10, "Mês", 1)
    pdf.cell(60, 10, "Entrada", 1)
    pdf.cell(60, 10, "Saída", 1)
    pdf.set_font("Arial", "", 12)
    pdf.ln("20")

    for key, value in data.items():
        year, month, day = value["date"].split("-")
        month = date(int(year), int(month), int(day))
        pdf.cell(60, 10, month.strftime("%b"), 1)
        pdf.cell(60, 10, "R$ {:,.2f}".format(Decimal(value["income"])), 1)
        pdf.cell(60, 10, "R$ {:,.2f}".format(Decimal(value["expense"])), 1)
        pdf.ln("20")

    pdf.output(f"staticfiles/{filename}", "F")

    return filename
