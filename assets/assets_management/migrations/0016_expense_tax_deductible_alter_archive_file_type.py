# Generated by Django 5.0 on 2024-03-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0015_alter_archive_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='tax_deductible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='archive',
            name='file_type',
            field=models.CharField(blank=True, choices=[('video', 'video'), ('image', 'image')], max_length=5),
        ),
    ]
