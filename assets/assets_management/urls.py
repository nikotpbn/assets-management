from django.urls import path
from .views import (
    asset_list,
    asset_detail,
    annual_report,
    month_report,
    asset_contract,
    asset_deed,
)

urlpatterns = [
    path("assets/", asset_list, name="asset-list"),
    path("asset/<slug:slug>", asset_detail, name="asset-detail"),
    path("asset/contract/<slug:slug>", asset_contract, name="asset-contract"),
    path("asset/deed/<slug:slug>", asset_deed, name="asset-deed"),
    path("annual/report", annual_report, name="annual-report"),
    path("month/report/<int:year>/<int:month>", month_report, name="month-report"),
]
