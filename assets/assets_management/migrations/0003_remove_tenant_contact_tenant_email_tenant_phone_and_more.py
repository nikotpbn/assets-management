# Generated by Django 4.1.3 on 2023-12-22 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0002_contract_file_alter_expense_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='contact',
        ),
        migrations.AddField(
            model_name='tenant',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tenant',
            name='phone',
            field=models.CharField(default=None, max_length=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='contracts'),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
