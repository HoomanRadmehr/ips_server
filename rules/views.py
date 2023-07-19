from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from user_manager.permissions import IsAdminOnly,IsSupporterOnly,IsDeveloperOnly,IsCustomerOnly
from rest_framework import status
from ips_server.pagination import CustomPagination
from rules.serializers import ListRuleSerializer,RetrieveRuleSerializer,AdminRuleSerializer
from rules.models import Rule


class ListRuleView(generics.ListAPIView):
    
    def get_user(self):
        return self.request.user
    
    permission_classes = [IsAdminOnly|IsSupporterOnly|IsCustomerOnly|IsDeveloperOnly]
    serializer_class = ListRuleSerializer
    queryset = Rule.objects.filter(is_verified=True,is_public=True)
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['created_at','updated_at']
    search_fields = ['description']
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_developer:
            return Rule.objects.all()
        else:
            return Rule.objects.filter(is_verified=True,is_public=True)
    
    
class RetrieveRuleView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOnly|IsSupporterOnly|IsCustomerOnly|IsDeveloperOnly]
    serializer_class = RetrieveRuleSerializer
    queryset = Rule.objects.filter(is_verified=True)
    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_developer:
            return Rule.objects.all()
        else:
            return Rule.objects.filter(is_verified=True)
        
class UpdateRuleView(generics.UpdateAPIView):
    permission_classes = [IsAdminOnly|IsDeveloperOnly]
    serializer_class = RetrieveRuleSerializer
    queryset = Rule.objects.all()
    lookup_field='pk'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance,data=request.data,partial=True)
        if serializer.is_valid():
            if request.user.is_developer:
                serializer.validated_data["is_verified"]=False
            serializer.validated_data["version"] = instance.version+0.1
            serializer.save()
            return Response({"info":"updated succesfully"},status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class CreateRuleView(APIView):
    permission_classes = [IsDeveloperOnly|IsAdminOnly]
    def post(self,request):
        data = request.data
        ser_data = AdminRuleSerializer(data=data)
        if ser_data.is_valid():
            if request.user.is_developer:
                ser_data.is_verified=False
            ser_data.save()
            return Response({"info":"successfully add rule"},status=status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
class VerifiedRuleView(APIView):
    permission_classes = [IsAdminOnly]
    
    def get(self,request,rule_id):
        try:
            rule = Rule.objects.get(id=rule_id)
            rule.is_verified = True
            rule.save()
            ser_rule = RetrieveRuleSerializer(rule)
            return Response(ser_rule.data,status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"error":"invalid rule id passed"},status=status.HTTP_400_BAD_REQUEST)
