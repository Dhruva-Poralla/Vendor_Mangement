from django.urls import path
from .views import PurchaseOrderCreateView, PurchaseOrderListView, PurchaseOrderDetailView, PurchaseOrderAcknowledgeView

urlpatterns = [
    path('create_order/', PurchaseOrderCreateView.as_view(),name="create_order"),
    path('orders_list/', PurchaseOrderListView.as_view(),name="list-purchase-orders"),
    path('purchase_details/<int:po_id>/', PurchaseOrderDetailView.as_view(),name="order-details"),
    path('<int:po_id>/acknowledge',PurchaseOrderAcknowledgeView.as_view())
]