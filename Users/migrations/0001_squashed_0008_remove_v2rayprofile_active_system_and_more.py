# Generated by Django 4.1.3 on 2022-11-28 08:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [
        ("Users", "0001_initial"),
        ("Users", "0002_alter_v2rayprofile_admin_message_and_more"),
        ("Users", "0003_v2rayprofile_v2ray_state_and_more"),
        ("Users", "0004_remove_v2rayprofile_system_message_and_more"),
        ("Users", "0005_remove_subscription_start_volume"),
        ("Users", "0006_alter_subscription_options"),
        ("Users", "0007_rename_start_date_subscription_created_at"),
        ("Users", "0008_remove_v2rayprofile_active_system_and_more"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="V2RayProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("active_admin", models.BooleanField(default=True)),
                ("admin_message", models.TextField(blank=True)),
                (
                    "v2ray_state",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "v2ray_state_date",
                    models.DateTimeField(
                        blank=True, editable=False, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("duration", models.IntegerField(default=30)),
                (
                    "volume",
                    models.PositiveBigIntegerField(default=10737418240.0),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Users.v2rayprofile",
                    ),
                ),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("0", "Reserve"),
                            ("1", "Active"),
                            ("2", "Expire"),
                        ],
                        default="0",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
    ]
