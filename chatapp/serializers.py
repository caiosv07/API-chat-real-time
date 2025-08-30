from rest_framework import serializers
from .models import ChatSala, ChatUser, Message, CustomUser
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSala
        fields = ['name', 'private', 'created_at', 'id']
        

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['sala', 'user', 'joined_at']
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sala', 'sender', 'content', 'message_type', 'file', 'created_at']
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username']


    def validate(self, attrs):
        
        email_exists = CustomUser.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('Este endereço de email já está sendo usado')

        return super().validate(attrs)

    def create(self, validated_data):
        user = CustomUser(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user