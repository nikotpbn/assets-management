# Generated by Django 5.0 on 2024-03-27 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_emailrecovery'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailrecovery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailrecovery',
            name='expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
