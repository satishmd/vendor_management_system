from django.urls import path, re_path
from vendors.views import VendorProfileManagement, PurchaseOrderManagement
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("vendors/", VendorProfileManagement.as_view(), name="vendors"),
    path(
        "vendors/<str:vendor_code>/",
        VendorProfileManagement.as_view(),
        name="vendor_by_id",
    ),
    path(
        "vendors/<str:vendor_code>/performance/",
        VendorProfileManagement.as_view(),
        name="vendor_performance",
    ),
    path("purchase_orders/", PurchaseOrderManagement.as_view(), name="purchase"),
    path(
        "purchase_orders/<str:po_id>/",
        PurchaseOrderManagement.as_view(),
        name="purchase_by_id",
    ),
    path(
        "purchase_orders/<str:po_id>/acknowledge",
        PurchaseOrderManagement.as_view(),
        name="purchase_by_id",
    ),
]
