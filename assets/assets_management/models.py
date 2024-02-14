from django.db import models
from .validators import validate_format, check_format
import uuid


def generate_file_name():
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return uuid.uui4()


def archive_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"{instance.asset.id}/archive/{uuid.uuid4()}.{ext}"


def contract_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"{instance.asset.id}/contract/{uuid.uuid4()}.{ext}"


def asset_income_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"{instance.asset.id}/income/{uuid.uuid4()}.{ext}"


def asset_expense_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"{instance.asset.id}/expense/{uuid.uuid4()}.{ext}"


def general_expense_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"expense/{instance.date.year}/{instance.date.month}/{uuid.uuid4()}.{ext}"


def asset_directory_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"{instance.asset.id}/cover/{uuid.uuid4()}.{ext}"


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=128)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=128)  # check this one

    def __str__(self):
        return f"{self.street} {self.number}"


class Asset(models.Model):
    name = models.CharField(max_length=128)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    cover = models.ImageField(null=True, blank=True, upload_to=asset_directory_path)

    def __str__(self):
        return self.name


class Tenant(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    is_current = models.BooleanField(default=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="tenants")


class Contract(models.Model):
    rent_value = models.DecimalField(max_digits=9, decimal_places=2)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="contracts")
    file = models.FileField(blank=True, null=True, upload_to=contract_directory_path)

    def __str__(self):
        return f"{self.start} - {self.end}"


class Expense(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="expenses")
    document = models.FileField(
        null=True, blank=True, upload_to=asset_expense_directory_path
    )


class GeneralExpense(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    document = models.FileField(
        null=True, blank=True, upload_to=general_expense_directory_path
    )


class Income(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="incomes")
    document = models.FileField(
        null=True, blank=True, upload_to=asset_income_directory_path
    )

    def __str__(self):
        return f"{self.asset.name}-{self.date} - {self.value}"


class Archive(models.Model):
    FILE_TYPE_CHOICES = {("video", "video"), ("image", "image")}

    title = models.CharField(max_length=128)
    description = models.TextField()
    file = models.FileField(
        upload_to=archive_directory_path, validators=[validate_format]
    )
    file_type = models.CharField(max_length=5, choices=FILE_TYPE_CHOICES, blank=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="archives")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.file_type = check_format(self.file.name)
        return super().save()

    @property
    def filename(self):
        return self.file.name
