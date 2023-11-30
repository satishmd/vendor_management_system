from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from vendors.models import *
from vendors.serializers import *
from uuid import uuid4
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
import datetime
from datetime import timedelta
from vendors.custom_authentication import HeaderAuthentication


class VendorProfileManagement(APIView):
    """
    Vendor Management class for maintaining vendor data.
    """

    # authentication_classes = [HeaderAuthentication]

    def __init__(self) -> None:
        pass

    def retrive_performace(self, vendor_code):
        """
        retrive performance class to retrive the performance of each vendor
        """
        data = VendorDetails.objects.get(vendor_code=vendor_code)
        serializer = VendorSerializer(data)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def get(self, request, vendor_code=None):
        """
        Get call to retrive all the vendor's or vendor by vendor_code.
        """
        data = VendorDetails.objects.all()
        serializer = VendorSerializer(data, many=True)
        if vendor_code and "performance" in request.path:
            return self.retrive_performace(vendor_code)
        if vendor_code:
            data = VendorDetails.objects.get(vendor_code=vendor_code)
            serializer = VendorSerializer(data)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Post call to create a new vendor.
        """
        data = request.data
        vendor_id = str(uuid4())
        data.update({"vendor_code": vendor_id})
        serializer = VendorSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, vendor_code=None):
        """
        Patch call to update the vendor.
        """
        vendor = VendorDetails.objects.get(vendor_code=vendor_code)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def delete(self, request, vendor_code):
        """
        Delete call to delete the vendor.
        """
        data = VendorDetails.objects.get(vendor_code=vendor_code)
        data.delete()
        return Response(
            {"status": "success", "data": "vendor deleted"}, status=status.HTTP_200_OK
        )


class PurchaseOrderManagement(APIView):
    """
    Purchase Order Management class to manage the Purchase Order's of vendors.
    """

    def __init__(self) -> None:
        pass

    def get(self, request, po_id=None):
        """
        Get call to retrive all the Purchase Orders or order based po_id.
        """
        data = purchaseOrderDetails.objects.all()
        serializer = PurchaseOrderSerializer(data, many=True)
        if po_id:
            data = purchaseOrderDetails.objects.get(po_number=po_id)
            serializer = PurchaseOrderSerializer(data)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, po_id=None):
        """
        Post call to create the Po order and to store the acknowledgement of the order.
        """
        data = request.data
        vendor = VendorDetails.objects.get(vendor_code=data.get("vendor_code"))

        # acknowledge api call handling
        if "acknowledge" in request.path:
            po = purchaseOrderDetails.objects.get(po_number=po_id)

            if po.status == "cancelled":
                return Response(
                    {"status": "error", "message": "Your order is already cancelled."}
                )

            # validation to check weather the order is issued or not.
            if not po.issue_date:
                return Response(
                    {"status": "error", "message": "Your order is not yet issued."}
                )

            ack_data = {"acknowledgment_date": datetime.datetime.now()}
            serializer = PurchaseOrderSerializer(po, data=ack_data, partial=True)
            serializer.is_valid()
            serializer.save()

            total_ack_pos = purchaseOrderDetails.objects.filter(
                vendor=vendor.pk, acknowledgment_date__isnull=False
            )
            import pdb

            pdb.set_trace()
            time_diff = [po.acknowledgment_date - po.issue_date for po in total_ack_pos]
            total_time = sum(
                (timedelta(0) + delta for delta in time_diff), timedelta(0)
            )
            avg_response_time = total_time.total_seconds() / len(total_ack_pos)

            art_data = {"average_response_time": avg_response_time}
            serializer = VendorSerializer(vendor, data=art_data, partial=True)
            serializer.is_valid()
            serializer.save()

            return Response(
                {"status": "success", "message": "Thank you for acknowledgement"}
            )

        items = data.get("items")
        po_id = str(uuid4())
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=7)
        quantity = sum([int(i) for i in list(items.values())])
        data.update(
            {
                "po_number": po_id,
                "delivery_date": delivery_date,
                "quantity": quantity,
                "vendor": vendor.pk,
            }
        )
        serializer = PurchaseOrderSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()

        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def update_performance(self, po_id):
        """
        when ever patch is called to update the order
        this will be called to check and update perfromace of vendor's
        """
        order = purchaseOrderDetails.objects.get(po_number=po_id)
        vendor = order.vendor
        vendor_code = vendor.vendor_code
        vendor_data = {}

        # if status is updating for order, updating fulfillment rate of the vendor
        if self.status:
            total_pos = purchaseOrderDetails.objects.filter(vendor=vendor.pk)
            fulfilled_pos = purchaseOrderDetails.objects.filter(
                vendor=vendor.pk, status="completed"
            )

            fulfilment_rate = len(fulfilled_pos) / len(total_pos)
            vendor_data.update({"fulfillment_rate": fulfilment_rate})

            # if status is completed updating on_time_delivery_rate of the vendor
            if self.status == "completed":
                completed_pos = purchaseOrderDetails.objects.filter(
                    status="completed",
                    issue_date__lte=models.F("delivery_date"),
                    vendor=vendor.pk,
                )
                total_completed_pos = purchaseOrderDetails.objects.filter(
                    status="completed", vendor=vendor.pk
                )

                # if quality_rating is passed , then updaing quality_rating_avg of vendor.
                if "quality_rating" in self.update_request_data:
                    ratings = [po.quality_rating for po in total_completed_pos]
                    rating_avg = sum(ratings) / len(ratings)
                    vendor_data.update({"quality_rating_avg": rating_avg})

                on_time_delivery_rate = len(completed_pos) / len(total_completed_pos)
                vendor_data.update({"on_time_delivery_rate": on_time_delivery_rate})

            serializer = VendorSerializer(vendor, data=vendor_data, partial=True)

            if not serializer.is_valid():
                return Response(
                    {"status": "error", "message": "error while updating"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()

        return {"status": "success"}

    def patch(self, request):
        """
        Patch to update the purchase order.
        """
        self.update_request_data = request.data
        self.status = self.update_request_data.get("status")

        if self.status and "completed" in self.status:
            self.update_request_data.update({"issue_date": datetime.datetime.now()})

        po_id = self.update_request_data.pop("po_number")
        order = purchaseOrderDetails.objects.get(po_number=po_id)
        serializer = PurchaseOrderSerializer(
            order, data=self.update_request_data, partial=True
        )
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        self.update_performance(po_id)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def delete(self, request, po_id):
        """
        delete to delete the purchase order.
        """
        data = purchaseOrderDetails.objects.get(po_number=po_id)
        data.delete()
        return Response(
            {"status": "success", "data": "purchase deleted"}, status=status.HTTP_200_OK
        )
