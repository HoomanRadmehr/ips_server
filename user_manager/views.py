from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from user_manager.serializers import *
from user_manager.permissions import IsSupporterOnly,IsInstallerOnly,IsOwnerOnly,IsAdminOnly
from user_manager.models import Users
from utils.send_mail import send_email
import logging
import datetime
import traceback


class EmailVerificationView(APIView):
    def get(self,request):
        pass


class CreateUserView(APIView):
    permission_classes = [IsAdminOnly|IsInstallerOnly]
    
    def post(self,request):
        data = request.data
        ser_data = get_user_serializer(request,data=data)
        if ser_data.is_valid():
            ser_data.validated_data['is_verified']=False
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.validated_data)
            # try:
            #     user = Users.objects.get(email=ser_data.validated_data['email'])
            #     token = str(RefreshToken.for_user(user).access_token)
            #     current_site = get_current_site(request).domain
            #     relative_link = reverse('users:email_verification')
            #     abs_url = "http://"+current_site+relative_link+"token="+token
            #     email_body = f"wellcome to {current_site} to verify your email click the link bellow \n {abs_url}"
            #     data = {
            #         "subject":"EMAIL VERIFICATION",
            #         "body":email_body,
            #         "to":ser_data.validated_data['email']
            #         }
            #     send_email(data)
            #     logging.info(f'new user cre ated by user id {request.user.id}')
            #     return Response({"info":"user created"},status=status.HTTP_201_CREATED)
            # except:
            #     logging.error(traceback.format_exc())
            #     return Response({"error":"somthing wrong happen"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        # data = {
        #             "subject":"EMAIL VERIFICATION",
        #             "body":"HI",
        #             "to":"hooman.radmehr.dev@gmail.com"
        #         }
        # send_email(data)
        # print("send")
        # return Response({"send"})
    
    
class RetrieveUserView(APIView):
    permission_classes = [IsAdminOnly|IsSupporterOnly|IsOwnerOnly]
    
    def get(self,request,user_id):
        try:
            user = Users.objects.get(id=user_id)
            ser_user = get_user_serializer(request,instance=user)
            return Response(ser_user.data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"invalid user_id"},status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUserView(APIView):
    permission_classes = [IsAdminOnly|IsSupporterOnly|IsOwnerOnly]
    
    def put(self,request,user_id):
        try:
            user = Users.objects.get(id=user_id)
            data = request.data
            ser_data = get_user_serializer(request=request,instance=user,data=data)
            if ser_data.is_valid():
                ser_data.save()
                return Response({"info":"updated successfully"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error":"invalid user id"})
    
    
class DeleteUserView(APIView):
    permission_classes = [IsOwnerOnly|IsAdminOnly]
    
    def delete(self,request,user_id):
        try:
            user = Users.objects.get(id=user_id)
            user.is_deleted = True
            user.deleted_at = datetime.datetime.now()
            user.save()
            logging.info(f"user id {user_id} deleted by user id {request.user.id}")
            return Response({"info":"deleted successfully"})
        except:
            return Response({"error":"invalid user id"})

class ListUsersView(generics.ListAPIView):
    permission_classes = [IsAdminOnly|IsSupporterOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username','phonenumber','is_verified','deleted_at']
    
    def get_serializer(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return AdminUserSerializer(*args,**kwargs)
        elif self.request.user.is_installer:
            return InstallerUserSerializer(*args,**kwargs)
        elif self.request.user.is_supporter:
            return SupporterUserSerializer(*args,**kwargs)
        elif self.request.user.is_customer:
            return CustomerUserSerializer(*args,**kwargs)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Users.objects.all()
        else:
            return Users.objects.filter(is_customer=True)
    