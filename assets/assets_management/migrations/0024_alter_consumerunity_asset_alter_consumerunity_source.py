# Generated by Django 5.0 on 2024-06-16 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0023_alter_consumerunity_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerunity',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unities', to='assets_management.asset'),
        ),
        migrations.AlterField(
            model_name='consumerunity',
            name='source',
            field=models.CharField(choices=[('E', 'energia'), ('W', 'água'), ('G', 'gás')], max_length=16),
        ),
    ]
