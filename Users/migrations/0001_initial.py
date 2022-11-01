# Generated by Django 4.1.2 on 2022-10-31 14:43

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

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
                (
                    "email",
                    models.EmailField(
                        editable=False, max_length=254, unique=True
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "active_system",
                    models.BooleanField(default=False, editable=False),
                ),
                ("active_admin", models.BooleanField(default=False)),
                ("system_message", models.TextField(default="")),
                ("admin_message", models.TextField(default="")),
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
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("start_volume", models.PositiveBigIntegerField(blank=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Users.v2rayprofile",
                    ),
                ),
            ],
        ),
    ]
