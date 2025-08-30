from http import HTTPStatus
import json
import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

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
def test_register_view(client):
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
def test_register_view(client):
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
    