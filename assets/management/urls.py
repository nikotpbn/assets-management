from management.views import Dashboard, ManageAsset, AssetConsumerUnityView
from django.urls import path

app_name = "management"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("asset/", ManageAsset.as_view(), name="asset"),
    path("asset/unity/update/", AssetConsumerUnityView.as_view(), name="asset-unity"),
]