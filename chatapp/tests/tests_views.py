from http import HTTPStatus
import json
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from chatapp.models import ChatSala, ChatUser, Message
from django.contrib.auth.models import Permission

User = get_user_model()

@pytest.mark.django_db
def test_register_view(client):
    response = client.post(
        '/api/register/', data={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'message': 'User registered successfully.'}

@pytest.mark.django_db
def test_login_view(client):
    user = client.post(
        '/api/register/', data={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        }
    )

    response = client.post(
        '/api/login/', data={
            'email': 'alice@example.com',
            'password': 'secret',
        }
    )

    token = response.json()
    print(token['token_type'])
    assert response.status_code == HTTPStatus.OK
    assert 'access' in token
    assert 'refresh' in token
    

@pytest.mark.django_db
def test_criar_sala_view(client):
    user = User.objects.create_user(
        email='alice@example.com',
        password='secret'
    )


    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

    response = client.post(
        '/api/criar_sala/', data={
            'name': 'sala1',
            'private': False,
        }
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['message'] == "sala created successfully."
    assert data['name'] == 'sala1'
    assert data['private'] == False
    assert 'id' in data
    assert 'created_at' in data

''''
@pytest.mark.django_db
def test_adicionar_usuario_na_sala_view(client):
    user_admin = User.objects.create_user(
        email='alice@example.com',
        password='secret'
    )

    perm = Permission.objects.get(codename="IsChatAdmin")  
    user_admin.user_permissions.add(perm)
    user_admin.save()

    refresh = RefreshToken.for_user(user_admin)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

    sala = ChatSala.objects.create(name="Sala Teste", private=False)

    user  = User.objects.create_user(
        email='bob@example.com',
        password='secret'
    )


    response = client.post(
        '/api/adicionar_usuario/', data={
            'user': user.id,
            'sala': sala.id,
            'is_admin': False
        }
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['message'] == f"user added to the room {sala.name}."
    assert data['user'] == sala.id
    assert data['sala'] == user.id
    assert 'joined_at' in data
 '''


@pytest.mark.django_db
def test_adicionar_usuario_na_sala_view(client):
    user_admin = User.objects.create_user(
        email='alice@example.com',
        password='secret'
    )
    sala = ChatSala.objects.create(name="Sala Teste", private=False)
    ChatUser.objects.create(user=user_admin, sala=sala, is_admin=True)

    refresh = RefreshToken.for_user(user_admin)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {str(refresh.access_token)}'

    user = User.objects.create_user(email='bob@example.com', password='secret')

    response = client.post(
        f"/api/adicionar_usuario/",
        data={
            "user": user.id,
            "sala": sala.id,
            "is_admin": False
        }
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['message'] == "user added to the room"
    assert data['user'] == user.id
    assert data['sala'] == sala.id
    assert data['is_admin'] == False
    assert 'joined_at' in data


@pytest.mark.django_db
def test_listar_mensagens_view(client, user):
    sala1 = ChatSala.objects.create(name='Sala 1')

    msg1 = Message.objects.create(sala=sala1, sender=user, content='Oi')
    msg2 = Message.objects.create(sala=sala1, sender=user, content='Tudo bem?')

    response = client.get(f'/api/sala/{sala1.id}/mensagens/')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data) == 2
    assert Message.objects.filter(sala=sala1, sender=user, content='Oi').exists()
    assert Message.objects.filter(sala=sala1, sender=user, content='Tudo bem?').exists()
   

@pytest.mark.django_db
def test_listar_salas_retorna_salas(client):
        sala1 = ChatSala.objects.create(name='Sala 1', private=False)
        sala2 = ChatSala.objects.create(name='Sala 2', private=True)

        response = client.get('/api/salas/')
        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert len(data) == 2
        assert ChatSala.objects.filter(name='Sala 1', private=False).exists()
        assert ChatSala.objects.filter(name='Sala 2', private=True).exists()