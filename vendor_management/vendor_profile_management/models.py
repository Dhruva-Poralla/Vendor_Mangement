from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission

class VendorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        vendor = self.model(email=email, **extra_fields)
        vendor.set_password(password)
        vendor.save(using=self._db)
        return vendor

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Vendor(AbstractUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    created_Date = models.DateTimeField(auto_now_add=True)
    updated_Date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='vendor_groups', blank=True)  # Adding custom related_name
    user_permissions = models.ManyToManyField(Permission, related_name='vendor_permissions', blank=True)  # Adding custom related_name
    username = models.CharField(max_length=255,null=True,unique=False)
    
    objects = VendorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "vendor_profile"
        
        
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    created_Date = models.DateTimeField(auto_now_add=True)
    updated_Date = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "vender_performance"
