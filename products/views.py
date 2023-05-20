from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Category,Brand,Device,DeviceSerial
from products.serializers import CategorySerializer,BrandSerializer,DeviceCreateSerializer,SerialSerializer,DeviceSerializer
from user_manager.permissions import IsAdminOrReadOnly,IsAdminOnly,IsSellerOnly,IsInstallerOnly,IsSupporterOnly
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
    permission_classes = [IsAdminOnly|IsSellerOnly|IsSupporterOnly|IsInstallerOnly]
    http_method_names = ['get','post','head','put','patch']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SerialFilter
    
    def create(self, request, *args, **kwargs):
        from user_manager.models import Users
        
        try:
            data = request.data
            ser_data = SerialSerializer(data=data)
            if ser_data.is_valid():
                validated_data = request.data
                creator = request.user
                device = Device.objects.get(id=validated_data['device'])
                if validated_data['owner']:
                    owner = Users.objects.get(id=validated_data["owner"])
                    serial = DeviceSerial(device=device,creator=creator,owner=owner)
                else:
                    serial = DeviceSerial(device=device,creator=creator)
                serial.save()
                return Response({"id":serial.id},status=status.HTTP_201_CREATED)
            else:
                return Response(ser_data.errors,status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({"error":"invalid device id or user id"},status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request,pk,*args, **kwargs):
        from user_manager.models import Users
        try:
            data = request.data
            ser_data = SerialSerializer(data=data)
            if ser_data.is_valid():
                validated_data = request.data
                owner = Users.objects.get(id=validated_data["owner"])
                serial = DeviceSerial.objects.get(id=pk)
                serial.owner=owner
                serial.save()
                return Response(ser_data.data,status.HTTP_200_OK)
            else:
                return Response(ser_data.errors,status.HTTP_400_BAD_REQUEST)
        except:
            logging.error(traceback.format_exc())
            return Response({"error":"invalid device id or user id"},status=status.HTTP_400_BAD_REQUEST)
        