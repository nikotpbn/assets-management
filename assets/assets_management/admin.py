from django.contrib import admin
from assets_management.models import (
    Tenant,
    Address,
    Asset,
    Contract,
    Deed,
    Expense,
    GeneralExpense,
    Income,
    Archive,
    Report,
    ConsumerUnity,
)


# Register your models here.
admin.site.register(Tenant)
admin.site.register(Address)
admin.site.register(Asset)
admin.site.register(Contract)
admin.site.register(Deed)
admin.site.register(Expense)
admin.site.register(GeneralExpense)
admin.site.register(Income)
admin.site.register(Archive)
admin.site.register(Report)
admin.site.register(ConsumerUnity)
