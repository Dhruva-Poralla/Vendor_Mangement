from django.apps import AppConfig


class VendorProfileManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor_profile_management'

    def ready(self):
        from purchase_orders import signals