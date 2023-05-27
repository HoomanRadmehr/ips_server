from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rules.models import Rule
from products.models import Category,Brand,Device,DeviceSerial
from products.serializers import CategorySerializer,BrandSerializer,DeviceCreateSerializer,SerialSerializer,DeviceSerializer,AssignRuleSerializer,SellerSerialSerializer,AssignOwnerSerializer
from user_manager.permissions import IsAdminOrReadOnly,IsAdminOnly,IsSellerOnly,IsInstallerOnly,IsSupporterOnly,IsCustomerOnly
from django_filters import rest_framework as filters
from products.filters import CategoryFilter,BrandFilter,DeviceFilter,SerialFilter
from rest_framework import filters as rest_filters
import logging
import traceback

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter
    
class BrandView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BrandFilter
    
class DeviceView(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,rest_filters.SearchFilter)
    search_fields = ['description',]
    filterset_class = DeviceFilter
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            ser_data = DeviceCreateSerializer(data=data)
            if ser_data.is_valid():
                validated_data = ser_data.validated_data
                brand_id = str(validated_data['brand_id'])
                category_id = str(validated_data['category_id'])
                Brand.objects.get(id=brand_id)
                Category.objects.get(id=category_id)
                ser_data.save()
                return Response({"info":"successfully created"},status=status.HTTP_201_CREATED)
            else:
                return Response(ser_data.errors,status=status.HTTP_201_CREATED)
        except:
            return Response({"error":"invalid id for brand or category or duplication"},status=status.HTTP_400_BAD_REQUEST)
    

class SerialView(ModelViewSet):
    queryset = DeviceSerial.objects.all()
    serializer_class = SerialSerializer
    permission_classes = [IsAdminOnly|IsSellerOnly|IsCustomerOnly]
    http_method_names = ['get','post','head']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SerialFilter
    
    def get_serializer_class(self):
        if self.request.user.is_seller:
            return SellerSerialSerializer
        return self.serializer_class
    
    def get_queryset(self):
        if not self.request.user.is_customer:
            queryset = DeviceSerial.objects.all()
        else:
            queryset = DeviceSerial.objects.filter(owner_id=self.request.user.id)
        queryset = queryset.prefetch_related("recommended_rules")
        return queryset
    
    def create(self, request, *args, **kwargs):
        from user_manager.models import Users
        
        try:
            data = request.data
            ser_data = SerialSerializer(data=data)
            if ser_data.is_valid():
                validated_data = request.data
                creator = request.user
                device = Device.objects.get(id=validated_data['device'])
                serial = DeviceSerial(device=device,creator=creator)
                serial.save()
                return Response({"id":serial.id},status=status.HTTP_201_CREATED)
            else:
                return Response(ser_data.errors,status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({"error":"invalid device id or user id"},status=status.HTTP_400_BAD_REQUEST)
        
class AssignOwnerView(APIView):
    permission_classes = [IsCustomerOnly]
    
    def post(self, request):
        try:
            data = request.data
            ser_data = AssignOwnerSerializer(data=data)
            if ser_data.is_valid():
                serial_id = str(ser_data.validated_data['serial'])
                device_serial = DeviceSerial.objects.get(id=serial_id)
                device_serial.owner = request.user
                device_serial.save()
                return Response(ser_data.data,status.HTTP_200_OK)
            else:
                return Response(ser_data.errors,status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({"error":"invalid device id or user id"},status=status.HTTP_400_BAD_REQUEST)


class AssignRuleView(APIView):
    permission_classes = [IsAdminOnly]
    
    def post(self,request):
        try:
            data = request.data
            ser_data = AssignRuleSerializer(data=data)
            if ser_data.is_valid():
                serial_id = str(ser_data.validated_data['serial_id'])
                rule_id = str(ser_data.validated_data['rule_id'])
                serial = DeviceSerial.objects.get(id=serial_id)
                rule = Rule.objects.get(id=rule_id)
                serial.recommended_rules.add(rule)
                serial.save()
                return Response(ser_data.data,status=status.HTTP_201_CREATED)
            else:
                return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({'error':'something wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            data = request.data
            ser_data = AssignRuleSerializer(data=data)
            if ser_data.is_valid():
                serial_id = str(ser_data.validated_data['serial_id'])
                rule_id = str(ser_data.validated_data['rule_id'])
                serial = DeviceSerial.objects.get(id=serial_id)
                rule = Rule.objects.get(id=rule_id)
                serial.recommended_rules.delete(rule)
                serial.save()
                return Response(ser_data.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({'error':'something wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        