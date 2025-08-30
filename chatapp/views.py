from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SalaSerializer, ChatUserSerializer, MessageSerializer
from .models import Message, ChatSala
from .permissions import IsChatAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(email=email)
    user.set_password(password)
    user.save()

    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'token_type': str(refresh.token_type)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Criar_Sala(request):
    serializer = SalaSerializer(data=request.data)
    if serializer.is_valid():
        sala = serializer.save()
        return Response({
            "message": "sala created successfully.",
            "id": sala.id,
            "name": sala.name,
            "private": sala.private,
            "created_at": sala.created_at
        }, 
        status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsChatAdmin])
def adicionar_usuario_na_sala(request):
    serializer = ChatUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def enviar_mensagem(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_mensagens(request, sala_id):
    mensagens = Message.objects.filter(sala_id=sala_id).order_by('created_at')
    serializer = MessageSerializer(mensagens, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_salas(request):
    sala = ChatSala.objects.all().order_by('created_at')
    serializer = SalaSerializer(sala, many=True)
    return Response(serializer.data)