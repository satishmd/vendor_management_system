from rest_framework import serializers
from vendors.models import VendorDetails, purchaseOrderDetails, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, required=True)
    contact_details = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    vendor_code = serializers.CharField(max_length=200, required=True)
    on_time_delivery_rate = serializers.FloatField(default=0.0)
    quality_rating_avg = serializers.FloatField(default=0.0)
    average_response_time = serializers.FloatField(default=0.0)
    fulfillment_rate = serializers.FloatField(default=0.0)

    class Meta:
        model = VendorDetails
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_number = serializers.CharField(max_length=200, required=True)
    delivery_date = serializers.DateTimeField(required=True)
    items = serializers.JSONField(required=True)
    quantity = serializers.IntegerField(required=True)
    status = serializers.CharField(max_length=100, default="pending")
    # quality_rating = serializers.FloatField(default = None)

    class Meta:
        model = purchaseOrderDetails
        fields = "__all__"


class HistoricalPerformance(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"
