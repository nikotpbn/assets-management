from management.views import (
    Dashboard,
    ManageAsset,
    AssetConsumerUnityView,
    AssetIncomeCreateView,
    AssetExpenseCreateView,
    AssetArchiveCreateView,
    AssetAnnualReportCreateView,
    MonthlyIncomeData,
    AnnualIncomeData
)
from django.urls import path

app_name = "management"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("asset/", ManageAsset.as_view(), name="asset"),
    path("asset/unity/update/", AssetConsumerUnityView.as_view(), name="asset-unity"),
    path(
        "asset/income/create/",
        AssetIncomeCreateView.as_view(),
        name="asset-income-create",
    ),
    path(
        "asset/expense/create/",
        AssetExpenseCreateView.as_view(),
        name="asset-expense-create",
    ),
    path(
        "asset/archive/",
        AssetArchiveCreateView.as_view(),
        name="asset-archive",
    ),
    path(
        "report/create/", AssetAnnualReportCreateView.as_view(), name="create-report"
    ),
    path("monthly/income/", MonthlyIncomeData.as_view(), name="monthly-income"),
    path("annual/income/", AnnualIncomeData.as_view(), name="annual-income"),
]
