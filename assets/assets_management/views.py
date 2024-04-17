from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile

from .models import Asset, GeneralExpense, Expense, Income, Report
from .util import (
    fill_up_missing_months,
    consolidate,
    calculate_expenses_totals,
    calculate_balance,
    check_aggregation_value,
    customPdf,
)

import json
import datetime


def month_report(request, year, month):
    if not request.user.is_authenticated:
        return redirect("/login")

    general_expenses = GeneralExpense.objects.filter(date__year=year, date__month=month)
    assets_expenses = Expense.objects.filter(
        date__year=year, date__month=month
    ).order_by("asset_id", "value")
    assets_incomes = Income.objects.filter(date__year=year, date__month=month).order_by(
        "asset_id", "value"
    )

    tin = assets_incomes.aggregate(total=Sum("value"))
    tge = general_expenses.aggregate(total=Sum("value"))
    tae = assets_expenses.aggregate(total=Sum("value"))

    tex = calculate_expenses_totals(tge["total"], tae["total"])
    bal = calculate_balance(tin["total"], tex)

    ctx = {
        "date": datetime.date(year, month, 1),
        "aex": assets_expenses,
        "gex": general_expenses,
        "inc": assets_incomes,
        "tge": tge["total"],
        "tae": tae["total"],
        "tin": tin["total"] if tin["total"] else 0,
        "tex": tex,
        "bal": bal,
    }
    return render(request, "report/month.html", ctx)


def annual_report(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    initial_year = 2022
    current_year = datetime.datetime.now().year
    year_options = [i for i in range(initial_year, current_year + 1)]

    year_filter = request.GET.get("year" or None)
    if not year_filter and request.method == "POST":
        year_filter = request.POST.get("year" or None)

    if year_filter:
        current_year = int(year_filter)

    try:
        report = Report.objects.get(year=current_year)
        if request.method == "POST":
            pdf_download = request.POST.get("pdf_download", None)
            if pdf_download:
                return FileResponse(report.file, filename="file.pdf")
    except ObjectDoesNotExist:
        report = None

    general_expenses_qs = (
        GeneralExpense.objects.filter(date__year=current_year)
        .values("date__month")
        .annotate(total=Sum("value"))
        .order_by()
    )

    asset_expenses_qs = (
        Expense.objects.filter(date__year=current_year)
        .values("date__month")
        .annotate(total=Sum("value"))
        .order_by()
    )

    incomes_qs = (
        Income.objects.filter(date__year=current_year)
        .values("date__month")
        .annotate(total=Sum("value"))
        .order_by()
    )

    gex = fill_up_missing_months(general_expenses_qs)
    aex = fill_up_missing_months(asset_expenses_qs)
    inc = fill_up_missing_months(incomes_qs)

    consolidated_data, metadata = consolidate(gex, aex, inc, current_year)

    if request.method == "POST":
        try:
            ardex_qs = Expense.objects.filter(
                date__year=current_year, tax_deductible=True
            )
            ardex = fill_up_missing_months(
                ardex_qs.values("date__month").annotate(total=Sum("value")).order_by()
            )
            pdf_obj = customPdf(inc, ardex, ardex_qs, current_year)
            buffer = pdf_obj.build()
            pdf = buffer.getvalue()
            pdf_file = ContentFile(pdf)
            pdf_file.name = f"Relatório Anual {current_year}.pdf"

            if report:
                report.file.delete()
                report.file = pdf_file
                report.save()
            else:
                report = Report.objects.create(year=current_year, file=pdf_file)
        except Exception as e:
            print(f"Algo de errado aconteceu: {e}")

    ctx = {
        "report": report,
        "year_options": year_options,
        "year": current_year,
        "metadata": metadata,
        "monthly_flow": consolidated_data,
        "monthly_json": json.dumps(consolidated_data, default=str),
        "path": "/annual/report/",
    }

    return render(request, "report/annual.html", ctx)


def asset_list(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    assets = Asset.objects.all()
    ctx = {"assets": assets, "path": "/asset/list/"}

    return render(request, "asset/list.html", ctx)


def asset_detail(request, slug=None):
    if not request.user.is_authenticated:
        return redirect("/login")

    asset = get_object_or_404(Asset, slug=slug)
    consumer_unities = asset.unities.all()
    current_year = datetime.datetime.now().year
    incomes = asset.incomes.filter(date__year=current_year).order_by("date")
    expenses = asset.expenses.filter(date__year=current_year).order_by("date")
    start_date = f"{datetime.datetime.now().year}-01"
    end_date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}"
    latest_contract = asset.contracts.filter(end__isnull=True)
    latest_tenant = asset.tenants.filter(is_current=True)
    deed = hasattr(asset, "deed")

    archives = [
        {
            "id": archive.id,
            "description": archive.description,
            "file": archive.file.url,
            "file_type": archive.file_type,
            "filename": archive.filename,
        }
        for archive in asset.archives.all()
    ]

    if request.method == "POST":
        start_year, start_month = request.POST.get("start", None).split("-")
        end_year, end_month = request.POST.get("end", None).split("-")

        start_date = datetime.date(int(start_year), int(start_month), 1)
        end_date = datetime.date(int(end_year), int(end_month), 1)

        incomes = asset.incomes.filter(
            date__range=[start_date, end_date],
        ).order_by("date")

        expenses = asset.expenses.filter(
            date__range=[start_date, end_date],
        ).order_by("date")

        start_date = f"{start_date.year}-{start_date.month:02d}"
        end_date = f"{end_date.year}-{end_date.month:02d}"

    tin = check_aggregation_value(incomes.aggregate(total=Sum("value")))
    tae = check_aggregation_value(expenses.aggregate(total=Sum("value")))
    bal = calculate_balance(tin, tae)

    return render(
        request,
        "asset/detail.html",
        {
            "asset": asset,
            "consumer_unities": consumer_unities,
            "incomes": list(incomes.values("date", "value")),
            "expenses": list(expenses.values("date", "value")),
            "income_total": tin,
            "expense_total": tae,
            "liquid_total": bal,
            "start_date": start_date,
            "end_date": end_date,
            "contract": True if len(latest_contract) > 0 else None,
            "deed": asset.deed if deed else None,
            "tenant": latest_tenant[0] if len(latest_tenant) > 0 else None,
            "archives": json.dumps(archives),
            "archives_qs": archives,
            "path": "/asset/detail/",
        },
    )


def asset_contract(request, slug):
    if not request.user.is_authenticated:
        return redirect("/login")

    asset = get_object_or_404(Asset, slug=slug)
    latest_contract = asset.contracts.filter(end__isnull=True)
    return FileResponse(latest_contract[0].file, filename=f"Contrato {asset.name}.pdf")


def asset_deed(request, slug):
    if not request.user.is_authenticated:
        return redirect("/login")

    asset = get_object_or_404(Asset, slug=slug)
    return FileResponse(asset.deed.file, filename=f"Contrato {asset.name}.pdf")


def create_report(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    initial_year = 2022
    current_year = datetime.datetime.now().year
    year_options = [i for i in range(initial_year, current_year + 1)]

    ctx = {
        "year_options": year_options,
        "year": current_year,
    }

    return render(request, "report/create.html", ctx)
