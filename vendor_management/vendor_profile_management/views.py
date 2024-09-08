#django imports
from rest_framework.response import Response
from vendor_profile_management.serializers import RegisterVendorSerializer,LoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#model imports
from .models import Vendor

#serializer imports
from .serializers import VendorSerializer,VendorPerformanceSerializer


class RegisterVendorView(APIView):
    
    def post(self,request):
        try:
            
            data = request.data 
            
            serializer = RegisterVendorSerializer(data=data)
            if not serializer.is_valid():
                return Response({'success': False,
                                'data':{},
                                 'message': 'something went wrong',
                                 'error':serializer.errors
                                 
                                 },status=status.HTTP_400_BAD_REQUEST)
                
            
            serializer.save()
            
            return Response({
                'success': True,
                'data':'',
                'message': 'your account is created successfully',
                            'error':''
                            
            },status=status.HTTP_201_CREATED)
            
        
        except Exception as ex:
            
            return Response({
                'success':False,
                'data': '',
                'message':'Error in registration',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class Login(APIView):
    
    def post(self, request):
        try:
            data = request.data
            
            serializer = LoginSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({'data':{},
                                 'message': 'something went wrong',
                                 'error':serializer.errors
                                 
                                 },status=status.HTTP_400_BAD_REQUEST)
                
            response = serializer.get_jwt_token(serializer.data)
            
            return Response(response,status=status.HTTP_200_OK)
            
        
        except Exception as ex:
            
            return Response({
                    "success":False,
                    'data': '',
                    'message':'Error in Login',
                    'error':str(ex)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorDetailView(APIView):
    """
    fetch a specific vendor.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request,vendor_id):
        try:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            if not vendor:
                return Response({"success":False,"error":"vendor details not found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as ex:
            return Response({
                    "success":False,
                    'data': '',
                    'message':'Internal Server Error',
                    'error':str(ex)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorsListView(APIView):
    """
    Fetch all vendors.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        try:
            vendors = Vendor.objects.all()
            if not vendors:
                return Response({"success": False,"message":"No records found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({
                    "success":False,
                    'data': '',
                    'message':'Internal Server Error',
                    'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class VendorDetailUpdateView(APIView):
    """
    Update a specific vendor.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def patch(self,request,vendor_id):
        try:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            if not vendor:
                return Response({"success":False,"error":"vendor details not found"},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = VendorSerializer(vendor, data=request.data, partial=True)  # partial=True allows PATCH
            if serializer.is_valid():
                serializer.save()
                response = {
                        'success': True,
                        'message': "Vendor details updated successfully",
                        'data': serializer.data
                }
                
                return Response(response, status=status.HTTP_200_OK)
            return Response({"success":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({
                    "success":False,
                    'data': '',
                    'message':'Internal Server Error',
                    'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
class VendorDeleteView(APIView):
    """
    Delete a specific vendor.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, vendor_id):
        try:
            vendor =Vendor.objects.filter(id=vendor_id).first()
            if not vendor:
                return Response({"success":False,"error":"vendor details not found"},status=status.HTTP_400_BAD_REQUEST)
            vendor.delete()  # Delete the vendor from the database
            response = {
                    'success': True,
                    'message': "Vendor details deleted successfully",
                    'data': ''
            }
            return Response(response,status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({
                    "success":False,
                    'data': '',
                    'message':'Internal Server Error',
                    'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class VendorPerformanceView(APIView):
    """
    Specific vendor performance.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            if not vendor:
                return Response({"success": False,"error":"vendor not found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = VendorPerformanceSerializer(vendor)
           
            response = {
                'success': True,
                'message': "",
                'data': serializer.data
            }
            return  Response(response,status=status.HTTP_200_OK)

        except Exception as ex:
            
            return Response({
                'success':False,
                'data': '',
                'message':'Error in fetching vendor performance',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)