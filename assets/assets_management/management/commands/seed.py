from django.core.management.base import BaseCommand

from assets_management.models import Asset, Address, Income, Expense, GeneralExpense


class Command(BaseCommand):
    help = "Seeds initial data"

    def handle(self, *args, **options):
        addresses = [
            {"street": "Rua João Balbi", "number": 328, "postal_code": "66055-280"},
            {
                "street": "Tv. Alm. Wandenkolk",
                "number": 811,
                "postal_code": "66055-280",
            },
            {
                "street": "Tv. Alm. Wandenkolk",
                "number": 809,
                "postal_code": "66055-280",
            },
        ]

        for address in addresses:
            Address.objects.create(**address)

        assets = [
            {"name": "Casa João Balbi", "address": Address.objects.get(pk=1)},
            {"name": "Sala Village (306)", "address": Address.objects.get(pk=2)},
            {"name": "Sala Village (304)", "address": Address.objects.get(pk=2)},
            {"name": "Dijon", "address": Address.objects.get(pk=2)},
            {"name": "Rio de Janeiro", "address": Address.objects.get(pk=2)},
            {"name": "3 de Maio", "address": Address.objects.get(pk=2)},
            {"name": "Alcindo Cacela", "address": Address.objects.get(pk=2)},
            {"name": "Garagem", "address": Address.objects.get(pk=3)},
            {"name": "Garagem Altos", "address": Address.objects.get(pk=3)},
        ]

        for asset in assets:
            Asset.objects.create(**asset)

        joao_balbi = Asset.objects.get(pk=1)
        village_306 = Asset.objects.get(pk=2)
        village_304 = Asset.objects.get(pk=3)
        dijon = Asset.objects.get(pk=4)
        rio_de_janeiro = Asset.objects.get(pk=5)
        tres_de_maio = Asset.objects.get(pk=6)
        alcindo_cacela = Asset.objects.get(pk=7)
        garagem = Asset.objects.get(pk=8)

        Income.objects.bulk_create(
            [
                Income(date="2023-01-05", asset=joao_balbi, value=5000),
                Income(date="2023-02-05", asset=joao_balbi, value=5000),
                Income(date="2023-03-05", asset=joao_balbi, value=4500),
                Income(date="2023-04-05", asset=joao_balbi, value=4500),
                Income(date="2023-05-05", asset=joao_balbi, value=9000),
                Income(date="2023-06-05", asset=joao_balbi, value=9000),
                Income(date="2023-07-05", asset=joao_balbi, value=9000),
                Income(date="2023-08-05", asset=joao_balbi, value=9000),
                Income(date="2023-09-05", asset=joao_balbi, value=9000),
                Income(date="2023-10-05", asset=joao_balbi, value=9000),
                Income(date="2023-11-05", asset=joao_balbi, value=9000),
                Income(date="2023-12-05", asset=joao_balbi, value=9000),
                Income(date="2023-01-05", asset=village_306, value=1170),
                Income(date="2023-02-05", asset=village_306, value=1170),
                Income(date="2023-03-05", asset=village_306, value=1170),
                Income(date="2023-04-05", asset=village_306, value=1170),
                Income(date="2023-05-05", asset=village_306, value=1170),
                Income(date="2023-06-05", asset=village_306, value=1170),
                Income(date="2023-07-05", asset=village_306, value=1170),
                Income(date="2023-08-05", asset=village_306, value=1170),
                Income(date="2023-09-05", asset=village_306, value=1170),
                Income(date="2023-10-05", asset=village_306, value=1170),
                Income(date="2023-11-05", asset=village_306, value=1170),
                Income(date="2023-12-05", asset=village_306, value=1170),
                Income(date="2023-01-05", asset=village_304, value=800),
                Income(date="2023-02-05", asset=village_304, value=800),
                Income(date="2023-03-05", asset=village_304, value=1125),
                Income(date="2023-04-05", asset=village_304, value=1125),
                Income(date="2023-05-05", asset=village_304, value=1125),
                Income(date="2023-06-05", asset=village_304, value=1125),
                Income(date="2023-07-05", asset=village_304, value=1125),
                Income(date="2023-08-05", asset=village_304, value=1125),
                Income(date="2023-09-05", asset=village_304, value=1125),
                Income(date="2023-10-05", asset=village_304, value=1125),
                Income(date="2023-11-05", asset=village_304, value=1125),
                Income(date="2023-12-05", asset=village_304, value=1125),
                Income(date="2023-01-05", asset=dijon, value=2100),
                Income(date="2023-02-05", asset=dijon, value=2100),
                Income(date="2023-03-05", asset=dijon, value=1939.5),
                Income(date="2023-04-05", asset=dijon, value=1939.5),
                Income(date="2023-05-05", asset=dijon, value=1939),
                Income(date="2023-06-05", asset=dijon, value=1939),
                Income(date="2023-07-05", asset=dijon, value=1939),
                Income(date="2023-08-05", asset=dijon, value=1939),
                Income(date="2023-09-05", asset=dijon, value=1939),
                Income(date="2023-10-05", asset=dijon, value=1939),
                Income(date="2023-11-05", asset=dijon, value=1939),
                Income(date="2023-12-05", asset=dijon, value=1939),
                Income(date="2023-01-05", asset=rio_de_janeiro, value=2360.07),
                Income(date="2023-02-05", asset=rio_de_janeiro, value=2422.75),
                Income(date="2023-03-05", asset=rio_de_janeiro, value=2489.56),
                Income(date="2023-04-05", asset=rio_de_janeiro, value=2489.56),
                Income(date="2023-05-05", asset=rio_de_janeiro, value=1170.81),
                Income(date="2023-06-05", asset=rio_de_janeiro, value=1170.81),
                Income(date="2023-07-05", asset=rio_de_janeiro, value=1170.81),
                Income(date="2023-08-05", asset=rio_de_janeiro, value=624.13),
                Income(date="2023-09-05", asset=rio_de_janeiro, value=1942.88),
                Income(date="2023-10-05", asset=rio_de_janeiro, value=1942.88),
                Income(date="2023-11-05", asset=rio_de_janeiro, value=1942.88),
                Income(date="2023-12-05", asset=rio_de_janeiro, value=1942.88),
                Income(date="2023-01-05", asset=tres_de_maio, value=0),
                Income(date="2023-02-05", asset=tres_de_maio, value=0),
                Income(date="2023-03-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-04-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-05-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-06-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-07-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-08-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-09-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-10-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-11-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-12-05", asset=tres_de_maio, value=1438.11),
                Income(date="2023-01-05", asset=alcindo_cacela, value=0),
                Income(date="2023-02-05", asset=alcindo_cacela, value=0),
                Income(date="2023-03-05", asset=alcindo_cacela, value=0),
                Income(date="2023-04-05", asset=alcindo_cacela, value=0),
                Income(date="2023-05-05", asset=alcindo_cacela, value=0),
                Income(date="2023-06-05", asset=alcindo_cacela, value=0),
                Income(date="2023-07-05", asset=alcindo_cacela, value=0),
                Income(date="2023-08-05", asset=alcindo_cacela, value=0),
                Income(date="2023-09-05", asset=alcindo_cacela, value=0),
                Income(date="2023-10-05", asset=alcindo_cacela, value=0),
                Income(date="2023-11-05", asset=alcindo_cacela, value=0),
                Income(date="2023-12-05", asset=alcindo_cacela, value=0),
                Income(date="2023-01-05", asset=garagem, value=0),
                Income(date="2023-02-05", asset=garagem, value=0),
                Income(date="2023-03-05", asset=garagem, value=0),
                Income(date="2023-04-05", asset=garagem, value=0),
                Income(date="2023-05-05", asset=garagem, value=0),
                Income(date="2023-06-05", asset=garagem, value=0),
                Income(date="2023-07-05", asset=garagem, value=0),
                Income(date="2023-08-05", asset=garagem, value=0),
                Income(date="2023-09-05", asset=garagem, value=0),
                Income(date="2023-10-05", asset=garagem, value=0),
                Income(date="2023-11-05", asset=garagem, value=0),
                Income(date="2023-12-05", asset=garagem, value=0),
            ]
        )

        Expense.objects.bulk_create(
            [
                Expense(
                    date="2023-01-20",
                    value=350,
                    description="Goteira da João Balbi Marão de obra sem material",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-02-22",
                    value=500,
                    description="Manutenção Telhado da João Balbi Mão de Obra",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-02-22",
                    value=710,
                    description="Material da João Balbi variados",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-02-22",
                    value=339,
                    description="Nova Caixa D'agua",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-03-22",
                    value=1500,
                    description="Telhado 3 de maio material",
                    asset=tres_de_maio,
                ),
                Expense(
                    date="2023-03-22",
                    value=1500,
                    description="Telhado 3 de maio mão de obra",
                    asset=tres_de_maio,
                ),
                Expense(
                    date="2023-04-22",
                    value=170,
                    description="Agua João Balbi (Parcelamento Cosanpa)",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-05-22",
                    value=170,
                    description="Agua João Balbi (Parcelamento Cosanpa)",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-06-22",
                    value=170,
                    description="Agua João Balbi (Parcelamento Cosanpa)",
                    asset=joao_balbi,
                ),
                Expense(
                    date="2023-09-22", value=50.91, description="Celpa", asset=garagem
                ),
                Expense(
                    date="2023-09-22", value=57.46, description="Celpa", asset=garagem
                ),
                Expense(
                    date="2023-09-22", value=81.46, description="Celpa", asset=garagem
                ),
                Expense(
                    date="2023-12-22", value=5000, description="Documentação Escritura (mudança de nome)", asset=tres_de_maio
                ),
            ]
        )

        GeneralExpense.objects.bulk_create(
            [
                GeneralExpense(
                    date="2023-02-22", value=250, description="Padre do velorio"
                ),
                GeneralExpense(
                    date="2023-02-22", value=200, description="Padre da missa"
                ),
                GeneralExpense(
                    date="2023-02-22", value=570, description="letras ossuario"
                ),
                GeneralExpense(date="2023-02-22", value=3960, description="ossuario"),
                GeneralExpense(
                    date="2023-02-22", value=150, description="musico funeral/missa"
                ),
                GeneralExpense(date="2023-02-22", value=300, description="igreja"),
                GeneralExpense(
                    date="2023-03-22", value=3971.6, description="Salário empregadas"
                ),
                GeneralExpense(
                    date="2023-04-22", value=3986.46, description="Salário empregadas"
                ),
                GeneralExpense(
                    date="2023-04-22",
                    value=863,
                    description="Salinas Material de Pintura",
                ),
                GeneralExpense(
                    date="2023-04-22",
                    value=375.65,
                    description="Salinas Material Hidraulico e Limpeza",
                ),
                GeneralExpense(
                    date="2023-04-22",
                    value=600,
                    description="Salinas Mão de obra do reboco",
                ),
                GeneralExpense(
                    date="2023-04-22",
                    value=500,
                    description="Salinas reforma da calçcada e reforma da grade",
                ),
                GeneralExpense(
                    date="2023-04-22", value=72, description="Salinas Material eletrico"
                ),
                GeneralExpense(
                    date="2023-04-22", value=200, description="Salinas Piscina"
                ),
                GeneralExpense(
                    date="2023-04-22", value=400, description="Salinas Caseira"
                ),
                GeneralExpense(date="2023-04-22", value=100, description="Luz Salinas"),
                GeneralExpense(
                    date="2023-04-22", value=160, description="Maxima Salinas"
                ),
                GeneralExpense(
                    date="2023-04-22",
                    value=546.4,
                    description="Maxima Salinas (Contas atrasadas)",
                ),
                GeneralExpense(
                    date="2023-05-22", value=2161.23, description="Empregada Ângela"
                ),
                GeneralExpense(
                    date="2023-05-22", value=2161.23, description="Empregada Dila"
                ),
                GeneralExpense(
                    date="2023-05-22", value=400, description="Caseira Salinas"
                ),
                GeneralExpense(
                    date="2023-05-22", value=170, description="Máxima Salinas"
                ),
                GeneralExpense(
                    date="2023-06-22", value=2161.23, description="Empregada Ângela"
                ),
                GeneralExpense(
                    date="2023-06-22", value=2161.23, description="Empregada Dila"
                ),
                GeneralExpense(
                    date="2023-06-22", value=170, description="Máxima Salinas"
                ),
                GeneralExpense(
                    date="2023-06-22", value=400, description="Caseira Salinas"
                ),
                GeneralExpense(
                    date="2023-07-22", value=1980, description="Salário Ângela"
                ),
                GeneralExpense(
                    date="2023-07-22", value=1980, description="Salário Edileuza"
                ),
                GeneralExpense(
                    date="2023-07-22", value=368, description="Vale transporte ângela"
                ),
                GeneralExpense(
                    date="2023-07-22", value=400, description="Caseira salinas"
                ),
                GeneralExpense(date="2023-08-22", value=404.75, description="Cartório"),
                GeneralExpense(date="2023-08-22", value=400, description="Caseira"),
                GeneralExpense(
                    date="2023-08-22", value=2137, description="Salário ângela"
                ),
                GeneralExpense(
                    date="2023-08-22",
                    value=127.64,
                    description="Celpa Salinas",
                ),
                GeneralExpense(
                    date="2023-08-22",
                    value=357.72,
                    description="Celpa Salinas",
                ),
                GeneralExpense(
                    date="2023-08-22",
                    value=174.96,
                    description="Celpa Salinas",
                ),
                GeneralExpense(
                    date="2023-08-22",
                    value=4575.42,
                    description="Aposentadoria Edileuza",
                ),
                GeneralExpense(
                    date="2023-08-22", value=548.96, description="Maxima salinas"
                ),
                GeneralExpense(
                    date="2023-09-22", value=400, description="Caseira Salinas"
                ),
                GeneralExpense(date="2023-09-22", value=58.19, description="PM Belém"),
                GeneralExpense(date="2023-09-22", value=2000, description="IPTU"),
                GeneralExpense(
                    date="2023-09-22", value=3000, description="Aposentadoria Edileuza"
                ),
                GeneralExpense(
                    date="2023-09-22", value=2153.8, description="Salário Ângela"
                ),
                GeneralExpense(
                    date="2023-10-22", value=400, description="Caseira Salinas"
                ),
                GeneralExpense(
                    date="2023-10-22", value=3000, description="Aposentadoria Edileuza"
                ),
                GeneralExpense(
                    date="2023-10-22", value=2153.8, description="Salário Ângela"
                ),
                GeneralExpense(
                    date="2023-10-22", value=202.42, description="Maxima Salinas"
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=286.9,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=1806.06,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=796.38,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=1204.64,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=1204.62,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=1443.22,
                    description="E-Social Edileuza e Angela",
                ),
                GeneralExpense(
                    date="2023-11-22", value=2289, description="Salário Ângela"
                ),
                GeneralExpense(
                    date="2023-11-22", value=1953, description="Salário Ângela (13)"
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=1235,
                    description="Cosanpa débitos de parcelamentos anteriores",
                ),
                GeneralExpense(
                    date="2023-11-22",
                    value=522,
                    description="Cartorio - reconhecimento de documentos para cosanpa",
                ),
                GeneralExpense(
                    date="2023-12-22", value=400, description="Caseira Salinas"
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS("seeding finished"))
