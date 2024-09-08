from django.urls import path,include
from .views import RegisterVendorView, Login, VendorDetailView, VendorsListView, VendorDetailUpdateView, VendorDeleteView, VendorPerformanceView

urlpatterns = [
    
    path('register/',RegisterVendorView.as_view(),name='register-vendor'),
    path('login/',Login.as_view()),
    path('vendors_list/',VendorsListView.as_view(),name="vendor-list"),
    path('get_vendor/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('update_vendor/<int:vendor_id>/',VendorDetailUpdateView.as_view(),name='update-vendor'),
    path('delete_vendor/<int:vendor_id>/',VendorDeleteView.as_view(),name='delete-vendor'),
    path('<int:vendor_id>/performance',VendorPerformanceView.as_view(),name='vendor-performance'),
]