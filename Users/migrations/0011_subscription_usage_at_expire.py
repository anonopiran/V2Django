# Generated by Django 4.1.3 on 2022-12-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0010_fill_expired_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="usage_at_expire",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
