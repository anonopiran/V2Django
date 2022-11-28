# Generated by Django 4.1.3 on 2022-11-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0007_rename_start_date_subscription_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="v2rayprofile",
            name="active_system",
        ),
        migrations.AddField(
            model_name="subscription",
            name="started_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscription",
            name="state",
            field=models.CharField(
                choices=[("0", "Reserve"), ("1", "Active"), ("2", "Expire")],
                default="0",
                max_length=1,
            ),
        ),
    ]
