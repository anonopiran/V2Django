# Generated by Django 4.1.3 on 2022-11-15 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0004_remove_v2rayprofile_system_message_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="start_volume",
        ),
    ]
