# Generated by Django 4.2.16 on 2025-02-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='data_pedido',
            field=models.DateTimeField(default='2025-01-01 00:00:00'),
        ),
    ]
