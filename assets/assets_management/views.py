import json
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import FileResponse
from django.views import View

from .models import Asset, GeneralExpense, Expense, Income, Report
from management.util import get_month_name
from .util import (
    fill_up_missing_months,
    consolidate,
    calculate_expenses_totals,
    calculate_balance,
    check_aggregation_value,
    decimal_serializer,
    date_serializer,
    zero_if_none,
)


class AllTimeReportView(LoginRequiredMixin, View):
    """All incomes and expenses for an asset since the beginning."""

    login_url = "/login/"

    def get(self, request):
        assets = Asset.objects.all()
        metadata = {}
        selected_asset = int(request.GET.get("asset", "1"))

        asset = Asset.objects.get(id=selected_asset)

        expenses_qs = asset.expenses.all().order_by("-date")
        incomes_qs = asset.incomes.all().order_by("-date")
        metadata["total_expense"] = zero_if_none(
            expenses_qs.aggregate(Sum("value"))["value__sum"]
        )
        metadata["total_income"] = zero_if_none(
            incomes_qs.aggregate(Sum("value"))["value__sum"]
        )
        metadata["balance"] = calculate_balance(
            metadata["total_income"], metadata["total_expense"]
        )

        expenses = [
            {
                "date": date_serializer(obj.date),
                "value": decimal_serializer(obj.value),
                "description": obj.description,
            }
            for obj in expenses_qs
        ]

        return render(
            request,
            "report/all_time.html",
            {
                "selected_asset": selected_asset,
                "assets": assets,
                "asset": asset,
                "expenses": json.dumps(expenses),
                "metadata": metadata,
            },
        )


class MonthReportView(LoginRequiredMixin, View):
    """All incomes, expenses and general expenses within a month."""

    login_url = "/login/"
    years = list(Income.objects.values_list("date__year", flat=True).distinct())
    months = [{"number": i, "name": get_month_name(i)[0]} for i in range(1, 13)]

    def get(self, request, year, month):
        print(year, month)
        general_expenses = GeneralExpense.objects.filter(
            date__year=year, date__month=month
        )

        assets_expenses = Expense.objects.filter(
            date__year=year, date__month=month
        ).order_by("asset_id", "value")

        assets_incomes = Income.objects.filter(
            date__year=year, date__month=month
        ).order_by("asset_id", "value")

        tin = assets_incomes.aggregate(total=Sum("value"))
        tge = general_expenses.aggregate(total=Sum("value"))
        tae = assets_expenses.aggregate(total=Sum("value"))
        tex = calculate_expenses_totals(tge["total"], tae["total"])
        bal = calculate_balance(tin["total"], tex)

        ctx = {
            "months": self.months,
            "years": self.years,
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

    def post(self, request, year, month):
        print(year)
        print(month)
        general_expenses = GeneralExpense.objects.filter(
            date__year=year, date__month=month
        )

        assets_expenses = Expense.objects.filter(
            date__year=year, date__month=month
        ).order_by("asset_id", "value")

        assets_incomes = Income.objects.filter(
            date__year=year, date__month=month
        ).order_by("asset_id", "value")

        tin = assets_incomes.aggregate(total=Sum("value"))
        tge = general_expenses.aggregate(total=Sum("value"))
        tae = assets_expenses.aggregate(total=Sum("value"))
        tex = calculate_expenses_totals(tge["total"], tae["total"])
        bal = calculate_balance(tin["total"], tex)

        ctx = {
            "months": self.months,
            "years": self.years,
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


class AnnualReportView(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request):
        initial_year = 2022
        current_year = datetime.datetime.now().year

        selected_year = request.GET.get("year", None)
        if not selected_year:
            selected_year = datetime.datetime.now().year
        else:
            selected_year = int(selected_year)

        year_options = [i for i in range(initial_year, current_year + 1)]

        asset_expenses_qs = (
            Expense.objects.filter(date__year=selected_year)
            .values("date__month")
            .annotate(total=Sum("value"))
            .order_by()
        )

        general_expenses_qs = (
            GeneralExpense.objects.filter(date__year=selected_year)
            .values("date__month")
            .annotate(total=Sum("value"))
            .order_by()
        )

        asset_expenses_qs = (
            Expense.objects.filter(date__year=selected_year)
            .values("date__month")
            .annotate(total=Sum("value"))
            .order_by()
        )

        incomes_qs = (
            Income.objects.filter(date__year=selected_year)
            .values("date__month")
            .annotate(total=Sum("value"))
            .order_by()
        )

        gex = fill_up_missing_months(general_expenses_qs)
        aex = fill_up_missing_months(asset_expenses_qs)
        inc = fill_up_missing_months(incomes_qs)

        try:
            report = Report.objects.get(year=selected_year)
        except ObjectDoesNotExist:
            report = None

        consolidated_data, metadata = consolidate(gex, aex, inc, selected_year)
        ctx = {
            "report": report,
            "year_options": year_options,
            "year": selected_year,
            "metadata": metadata,
            "monthly_flow": consolidated_data,
            "monthly_json": json.dumps(consolidated_data, default=str),
            "path": "/annual/report/",
        }

        return render(request, "report/annual.html", ctx)

    def post(self, request):
        year = request.POST.get("year", None)

        try:
            report = Report.objects.get(year=year)
            return FileResponse(report.file, filename="file.pdf")

        except ObjectDoesNotExist:
            report = None


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
    selected_year = datetime.datetime.now().year
    incomes = asset.incomes.filter(date__year=selected_year).order_by("date")
    expenses = asset.expenses.filter(date__year=selected_year).order_by("date")
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
