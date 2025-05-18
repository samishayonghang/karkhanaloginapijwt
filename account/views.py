
from.serializers import RegisterSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

User=get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  
    serializer_class = RegisterSerializer

class SendPasswordResetEmailView(APIView):
    
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'detail':'password reset link sent please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'detail':'password Reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


