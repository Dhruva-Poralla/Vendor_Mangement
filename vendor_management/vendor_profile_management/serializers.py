from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from .models import Vendor


class RegisterVendorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    contact_details = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    vendor_code = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        
        if Vendor.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError('email already exists!!')
        
        return attrs
    
    def create(self, validated_data):
        
        vendor = Vendor.objects.create(name=validated_data.get('name').upper(),
                                email=validated_data.get('email'),
                                contact_details=validated_data.get('contact_details'),
                                address=validated_data.get('address'),
                                vendor_code=validated_data.get('vendor_code')                               
                                )
        
        
        vendor.set_password(validated_data.get('password'))     
        vendor.save()
        
        return validated_data
    


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    
    def validate(self, data):
        
        if not Vendor.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('account not found')
        
        return data
    
    def get_jwt_token(self, data):
        
        vendor = Vendor.objects.get(email=data.get('email'))  # Assuming email is used to identify vendor
        
        if not vendor or not check_password(data.get('password'), vendor.password):
            return {"message": "Invalid Credentials","data":{}}
        
        refresh = RefreshToken.for_user(vendor)
        
        return {"message":"login successful","data":{'refresh': str(refresh),
                                'access': str(refresh.access_token)}}
        
        

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['password','groups','user_permissions','first_name','last_name','username']
        

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']