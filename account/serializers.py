from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from.utils import Util
User=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','password','confirm_password']
    
    
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already reigistered")
        return value

    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]',value):
            raise serializers.ValidationError("password must containt at least one uppercase letter")
        if not re.search(r'[a-z]',value):
            raise serializers.ValidationError("password must contain at least one lowercase letter")
        if not re.search(r'\d',value):
            raise serializers.ValidationError("password must contain at least one digit ")
        if not re.search(r'[!@#%^&*(),.?:{}|<>]',value):
            raise serializers.ValidationError("password must contain at least one special character")
        return value
    
    def validate(self,data):
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError("your two password doesnot match")
        return data
        
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create_user(
           
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']

    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/account/user/reset/'+uid+'/'+token
            
            data={
                'subject':'Reset your password',
                'body': f'Click the following link to reset your password:\n{link}',

                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
            
        else:
            raise ValidationError('you are not registered user')
        

class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,write_only=True)
    password2=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model=User
        fields=['password','password2']

    def validate(self,attrs):
       try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("password and confirm password does not match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            
            
       except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not valid or expired")
       return attrs


