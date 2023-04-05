# Generated by Django 4.1.5 on 2023-01-12 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0014_fill_due_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="downlink",
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="uplink",
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
    ]