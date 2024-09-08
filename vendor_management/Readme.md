# Vendor Management System

Overview
The Vendor Management System is a Django-based application designed to manage vendors and track their performance metrics. The system allows administrators to create, update, and delete vendor profiles, as well as track purchase orders and calculate vendor performance metrics.

### 1. Vendor Profile Management
- Create, retrieve, update, and delete vendor profiles.
- Each vendor has a unique vendor code along with contact information and address.

### 2. Purchase Order Tracking
- Create, retrieve, update, and delete purchase orders (POs).
- Purchase orders include details like PO number, vendor reference, order date, items, quantity, and status.

### 3. Vendor Performance Evaluation
- Metrics such as on-time delivery rate, quality rating, response time, and fulfillment rate are calculated and tracked for each vendor.


Installation
Clone the repository: git clone https://github.com/your-username/vendor-management-system.git
Install dependencies: pip install -r requirements.txt
Create a database: python manage.py migrate
Run the development server: python manage.py runserver

## API Endpoints

### Vendor API
- **GET /api/vendors/vendors_list/**: Retrieve a list of all vendors
- **GET /api/vendors/get_vendor/{vendor_id}/**: Retrieve a specific vendor's profile
- **POST /api/vendors/register/**: Create a new vendor profile
- **PATCH /api/vendors/update_vendor/{vendor_id}/**: Update a vendor profile
- **DELETE /api/vendors/delete_vendor/{vendor_id}/**: Delete a vendor profile
- **GET /api/vendors/{vendor_id}/performance/**: Retrieve a vendor's performance metrics

### Purchase Order API
- **POST /api/purchase_orders/create_order**: Create a new purchase order.
- **GET /api/purchase_orders/orders_list**: List all purchase orders (filterable by vendor).
- **GET /api/purchase_orders/purchase_details/{po_id}/**: Retrieve a specific purchase order’s details.
- **PUT /api/purchase_orders/purchase_details/{po_id}/**: Update a purchase order.
- **DELETE /api/purchase_orders/purchase_details/{po_id}/**: Delete a purchase order.


## Data Models

### Vendor Model
- **Fields**: `name`, `contact_details`, `address`, `vendor_code`, `on_time_delivery_rate`, `quality_rating_avg`, `average_response_time`, `fulfillment_rate`.

### Purchase Order Model
- **Fields**: `po_number`, `vendor`, `order_date`, `delivery_date`, `items`, `quantity`, `status`, `quality_rating`, `issue_date`, `acknowledgment_date`.

### Historical Performance Model
- Tracks historical performance metrics for vendors.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone [<repostory_url>](https://github.com/Dhruva-Poralla/Vendor_Mangement/tree/main/vendor_management)
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the API via:
    - Vendors: `http://localhost:8000/api/vendors/`
    - Purchase Orders: `http://localhost:8000/api/purchase_orders/`
    - Vendor Performance: `http://localhost:8000/api/vendors/{vendor_id}/performance/`


## Authentication
- The API is secured with token-based authentication. You can obtain a token by registering a vendor and logging in.

## Running Tests
To run the test suite:
```bash
python manage.py test