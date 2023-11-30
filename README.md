# vendor_management_system


## Setup Instructions
1. python 3.9 or above required
2. create python virtualenv
    ```python -m venv venv```
3. activate the python virtualenv
    ```source env/scripts/activate```
4. install the requirements.txt
    ```pip install -r requirements.txt```
5. run the server
    ```python manage.py runserver```

# Explanation
Vendor Management system is built with django and django rest framework for manageing vendor's and their purchase orders.

we have used the built in db of django which is sqlite.

## Api Details

### for vendor Handling

1. POST /api/vendors/: Create a new vendor.
2. GET /api/vendors/: List all vendors.
3. GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
4. PUT /api/vendors/{vendor_id}/: Update a vendor's details.
5. DELETE /api/vendors/{vendor_id}/: Delete a vendor.
6. GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.

### for Purchase Order Handling

1. POST /api/purchase_orders/: Create a purchase order.
2. GET /api/purchase_orders/: List all purchase orders.
3. GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
4. PUT /api/purchase_orders/{po_id}/: Update a purchase order.
5. DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
6. POST /api/purchase_orders/{po_id}/acknowledge : for purchase order acknowledgement by vendor.

### Authorization

for every post call we would require a token in the headers.

To create a token you need to run the below command
```
python auth.py <username>
```
the above command will give the token and you need to pass the username and token separated by space in request.

There is a postman collection for the payload to be used for each payload , use that postman collection to call the api's.