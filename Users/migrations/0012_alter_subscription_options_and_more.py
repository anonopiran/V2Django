# Generated by Django 4.1.3 on 2022-12-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0011_subscription_usage_at_expire"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={},
        ),
        migrations.AlterField(
            model_name="subscription",
            name="usage_at_expire",
            field=models.JSONField(blank=True, editable=False, null=True),
        ),
    ]