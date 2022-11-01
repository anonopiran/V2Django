# Generated by Django 4.1.2 on 2022-11-01 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0002_alter_v2rayprofile_admin_message_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="v2rayprofile",
            name="v2ray_state",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="v2rayprofile",
            name="v2ray_state_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="v2rayprofile",
            name="active_admin",
            field=models.BooleanField(default=True),
        ),
    ]
