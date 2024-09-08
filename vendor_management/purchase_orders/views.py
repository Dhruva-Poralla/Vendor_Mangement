from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from rest_framework import status
from django.db.models.signals import post_save


from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from .utils import calculate_average_response_time

class PurchaseOrderCreateView(APIView):
    """_summary_

    Args:
        PurchaseOrderCreateView (POST): Creates a new purchase order
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        try:
            serializer = PurchaseOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                            'success': True,
                            'message': "Purchase Orders list",
                            'data': serializer.data
                }
                return Response(response,status=status.HTTP_201_CREATED)
            
            return Response({"success":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return Response({
                'success':False,
                'data': '',
                'message':'Error in creating order',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PurchaseOrderListView(APIView):
    """_summary_

    Args:
        PurchaseOrderListView (GET): Fetches a list of all purchase orders

    Returns:
        List: returns a list of all purchase orders
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            purchase_orders = PurchaseOrder.objects.all()
            if not purchase_orders:
                return Response({"success": False,"message":"No records found"},status=status.HTTP_400_BAD_REQUEST)
            
            if 'vendor' in request.GET:
                purchase_orders = purchase_orders.filter(vendor_id=request.GET['vendor'])
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            response = {
                        'success': True,
                        'message': "Purchase Orders list",
                        'data': serializer.data
                }
            return Response(response,status=status.HTTP_200_OK)
        
        except Exception as ex:
            
            return Response({
                'success':False,
                'data': '',
                'message':'Error in fetching orders list',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class PurchaseOrderDetailView(APIView):
    """
        PurchaseOrderDetailView (GET/PATCH/DELETE): Performs update and delete operations
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
            if not purchase_order:
                return Response({"success":False, "error": "Purchase order not found"},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PurchaseOrderSerializer(purchase_order)
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
                'message':'Error in fetching order for a specific purchase order',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
            if not purchase_order:
                return Response({"success":False, "error": "Purchase order not found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                # Manually trigger the post_save signal
                post_save.send(sender=PurchaseOrder, instance=purchase_order)
                
                response = {
                    'success': True,
                    'message': "",
                    'data': serializer.data
                }
                
                return  Response(response,status=status.HTTP_200_OK)
            return Response({"success":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            
            return Response({
                'success':False,
                'data': '',
                'message':'Error in fetching order for a specific purchase order',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.filter(id=po_id).first()
            if not purchase_order:
                return Response({"success":False, "error": "Purchase order not found"},status=status.HTTP_400_BAD_REQUEST)
            
            purchase_order.delete()
            return Response({'success':True,'message': 'Purchase order deleted'}, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({
                'success':False,
                'data': '',
                'message':'Error in deleting a specific purchase order',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PurchaseOrderAcknowledgeView(APIView):
    """_summary_

    Args:
        PurchaseOrderAcknowledgeView (post): update the acknowledgment of a purchase order
    """
    def post(self, request, po_id):
        try:
            po = PurchaseOrder.objects.filter(id=po_id).first()
            if not po:
                return Response({"success":False, "error": "Purchase order not found"},status=status.HTTP_400_BAD_REQUEST)
            po.acknowledgment_date = datetime.now()
            po.save()
            # Trigger recalculation of average_response_time
            vendor = po.vendor
            vendor.average_response_time = calculate_average_response_time(vendor)
            vendor.save()
            return Response({'success':True,'message': 'Acknowledgment successful'},status=status.HTTP_200_OK)
    
        except Exception as ex:
            return Response({
                'success':False,
                'data': '',
                'message':'Error in purchase order acknowledgement',
                'error':str(ex)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)