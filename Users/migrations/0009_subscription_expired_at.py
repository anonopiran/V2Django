# Generated by Django 4.1.3 on 2022-12-09 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Users",
            "0001_squashed_0008_remove_v2rayprofile_active_system_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="expired_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]