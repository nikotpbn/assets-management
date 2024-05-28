from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

import json
from django.http import JsonResponse

from assets_management.models import Asset

from management.forms import AssetEditAndCreateForm


class Dashboard(View):

    def get(self, request):
        return render(request, "dashboard.html")


class ManageAsset(View):

    def get(self, request):
        assets = Asset.objects.all()
        ctx = {"assets": assets}
        return render(request, "asset/index.html", ctx)

    def post(self, request):
        data = json.loads(request.body)
        asset = get_object_or_404(Asset, pk=data["asset_id"])
        unities = asset.unities.all().values("source", "number")
        return JsonResponse({"unities": json.dumps(list(unities))})


class AssetListView(View):
    def get(self, request):
        assets = Asset.objects.all()
        ctx = {"assets": assets}
        return JsonResponse()


class AssetCreateView(View):
    form = AssetEditAndCreateForm

    def get(self, request):
        form = self.form()
        ctx = {"form": form}
        return render(request, "", ctx)

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("management:asset-list")


class AssetConsumerUnityView(View):

    def post(self, request, slug=None):
        data = json.loads(request.body)
        unity = Asset.objects.get(pk=data["asset_id"]).unities.get(
            source=data["source"]
        )
        unity.number = data["number"]
        unity.save()
        return JsonResponse({"msg": "ok"})
