# Generated by Django 4.2.7 on 2023-11-30 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("vendors", "0002_remove_vendordetails_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAutenticate",
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
                ("username", models.CharField(max_length=100)),
                ("token", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalPerformance",
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
                    "vendor",
                    models.ForeignKey(
                        db_column="vendor_code",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="vendors.vendordetails",
                    ),
                ),
            ],
        ),
    ]
