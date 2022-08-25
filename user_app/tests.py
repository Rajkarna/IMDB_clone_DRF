from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    def test_Register(self):
        data ={
            "username" : "usernametestcase",
            "email" : "usernametestcase@gmail.com",
            "password" : "password@123",
            "password2" : "password@123"
        }
        
        response = self.client.post(reverse("register"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogoutTestCase(APITestCase):
    
    def selfUp(self):
        self.user = User.objects.create_user(username="example1", password="password")
        
    def test_login(self):
        
        data = {
            "username" : "example1",
            "password" : "password"
        }
        
        response = self.client.post(reverse("login"), data, format='json')
        self.assertLogs(response.status_code, status.HTTP_200_OK)
    
    def test_logout(self):
        self.user = User.objects.create_user(username="example1", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse("logout"))
        self.assertLogs(response.status_code, status.HTTP_200_OK)