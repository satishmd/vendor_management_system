from django.db import models

# Create your models here.


class VendorDetails(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(
        max_length=200, unique=True, db_index=True, primary_key=True
    )
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        db_table = "vendors"


class purchaseOrderDetails(models.Model):
    po_number = models.CharField(max_length=200, unique=True)
    vendor = models.ForeignKey(
        VendorDetails, db_column="vendor_code", db_index=True, on_delete=models.PROTECT
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "purchase_orders"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        VendorDetails, db_column="vendor_code", db_index=True, on_delete=models.PROTECT
    )
    date: models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate: models.FloatField()
    quality_rating_avg: models.FloatField()
    average_response_time: models.FloatField()
    fulfillment_rate: models.FloatField()


class UserAutenticate(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=200)
