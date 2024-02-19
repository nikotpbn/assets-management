from django.urls import path
from .views import asset_list, asset_detail, annual_report, month_report

urlpatterns = [
    path("assets/", asset_list, name="asset-list"),
    path("asset/<slug:slug>", asset_detail, name="asset-detail"),
    path("annual/report", annual_report, name="annual-report"),
    path("month/report/<int:year>/<int:month>", month_report, name="month-report")
]
