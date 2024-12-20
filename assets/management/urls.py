from management.views import (
    Dashboard,
    ManageAsset,
    AssetConsumerUnityView,
    AssetIncomeCreateView,
    AssetExpenseCreateView,
    AssetArchiveCreateView,
    AssetArchiveDeleteView,
    AssetAnnualReportCreateView,
    MonthlyIncomeData,
    AnnualIncomeData,
    AssetFlowView,
    AssetFlowDeleteView,
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
        "<slug:slug>/archive/delete/<int:archive_id>/",
        AssetArchiveDeleteView.as_view(),
        name="asset-archive-delete",
    ),
    path("report/create/", AssetAnnualReportCreateView.as_view(), name="create-report"),
    path("monthly/income/", MonthlyIncomeData.as_view(), name="monthly-income"),
    path("annual/income/", AnnualIncomeData.as_view(), name="annual-income"),
    path("asset/flow/", AssetFlowView.as_view(), name="asset-flow"),
    path(
        "<slug:slug>/flow/delete/<int:flow_id>/<str:action>/",
        AssetFlowDeleteView.as_view(),
        name="delete-flow",
    ),
]
