from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from django.db.models import Sum
from django.http import JsonResponse

import json
import decimal
import datetime

from assets_management.models import Asset, Income, Expense, Archive, ConsumerUnity
from management.forms import AssetEditAndCreateForm


def decimal_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError("Type not serializable")


class Dashboard(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        labels = []
        data = []

        years = list(Income.objects.values_list("date__year", flat=True).distinct())
        qs = (
            Income.objects.filter(date__year__in=years)
            .values("date__year")
            .annotate(Sum("value"))
            .order_by()
        )
        for obj in qs:
            labels.append(obj['date__year'])
            data.append(obj['value__sum'])

        return render(
            request,
            "dashboard.html",
            {
                'labels': json.dumps(labels),
                'data': json.dumps(data, default=decimal_serializer)
            }
        )


class ManageAsset(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        assets = Asset.objects.all()
        ctx = {"assets": assets}
        return render(request, "asset/index.html", ctx)

    def post(self, request):
        data = json.loads(request.body)
        asset = get_object_or_404(Asset, pk=data["asset_id"])
        unities = asset.unities.all().values("source", "number")
        return JsonResponse({"unities": json.dumps(list(unities))})


class AssetListView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        return JsonResponse()


class AssetCreateView(LoginRequiredMixin, View):
    login_url = "/login/"
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


class AssetConsumerUnityView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, slug=None):
        status = 500
        msg = 'Algo de errado aconteceu'
        data = json.loads(request.body)

        try:
            asset = Asset.objects.get(pk=data["asset_id"])
            unity = ConsumerUnity.objects.get(asset=asset, source=data["source"])
            unity.number = data["number"]
            unity.save()
            status = 200
            msg = 'Unidade atualizada com succeso'

        except ConsumerUnity.DoesNotExist:
            create_defaults = {'asset': asset, 'source': data["source"], 'number': data["number"]}
            unity = ConsumerUnity.objects.create(**create_defaults)
            status = 200
            msg = 'Unidade criada com succeso'

        return JsonResponse({"message": msg, 'status': status})


class AssetArchiveCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request):
        status = 500
        msg = 'Algo de errado aconteceu'
        archive = None

        asset = Asset.objects.get(pk=request.POST['asset_id'])
        title = request.POST['title'].strip()
        description = request.POST['description'].strip()
        data_is_valid = title != "" and description != ""

        if data_is_valid:
            archive = Archive.objects.create(
                asset=asset,
                file=request.FILES['file'],
                title=request.POST['title'],
                description=request.POST['description']
            )

        if archive:
            status = 200
            msg = "Arquivo adicionado com sucesso."

        return JsonResponse({'message': msg, 'status': status})


class AssetIncomeCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request):
        data = json.loads(request.body)
        value = data['value'].replace(".", "").replace(",", ".")
        year, month, day = data['date'].split("-")
        asset = Asset.objects.get(pk=data['asset_id'])
        validated_data = {
            'value': decimal.Decimal(value),
            'date': datetime.date(int(year), int(month), int(day)),
            'asset': asset
        }
        income = Income.objects.create(**validated_data)

        if income:
            msg = f'Criada entrada no valor de R$ {data['value']} para o imóvel {asset.name}'
            status = 200
        else:
            msg = 'Algo de errado aconteceu'
            status = 500

        return JsonResponse({'message': msg, 'status': status})


class AssetExpenseCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request):
        data = json.loads(request.body)
        value = data['value'].replace(".", "").replace(",", ".")
        year, month, day = data['date'].split("-")
        asset = Asset.objects.get(pk=data['asset_id'])
        validated_data = {
            'value': decimal.Decimal(value),
            'date': datetime.date(int(year), int(month), int(day)),
            'description': data['description'],
            'asset': asset
        }
        expense = Expense.objects.create(**validated_data)

        if expense:
            msg = f'Criada saída no valor de R$ {data['value']} para o imóvel {asset.name}'
            status = 200
        else:
            msg = 'Algo de errado aconteceu'
            status = 500

        return JsonResponse({'message': msg, 'status': status})
