from django.urls import path
from .views import (
    asset_list,
    asset_detail,
    month_report,
    asset_contract,
    asset_deed,
    AllTimeReportView,
    AnnualReportView,
)

urlpatterns = [
    path("assets/", asset_list, name="asset-list"),
    path("asset/<slug:slug>", asset_detail, name="asset-detail"),
    path("asset/contract/<slug:slug>", asset_contract, name="asset-contract"),
    path("asset/deed/<slug:slug>", asset_deed, name="asset-deed"),
    path("annual/report", AnnualReportView.as_view(), name="annual-report"),
    path("month/report/<int:year>/<int:month>", month_report, name="month-report"),
    path("alltime/report", AllTimeReportView.as_view(), name="all-time-report"),
]
