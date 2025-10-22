import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db, django_user_model):
    user = User.objects.create_user(email='bob@example.com', password='123')
    return user