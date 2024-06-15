from datetime import date
from decimal import Decimal


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")


def date_serializer(obj):
    if isinstance(obj, date):
        month = f"0{obj.month}" if obj.month < 10 else obj.month
        day = f"0{obj.day}" if obj.day < 10 else obj.day
        return f"{obj.year}-{month}-{day}"
    raise TypeError("Type not serializable")


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


def zero_if_none(value):
    if value is None:
        return 0
    return value


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
