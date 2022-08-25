from django.contrib.auth.models import User
from .models import StreamPlatform, WatchList, Review
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = "example2", email = "example2@example.com")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = StreamPlatform.objects.create(name="netflix",about="A number 1 platform",
                                                        website="http://www.netflix.com")
    
    def test_stream_create(self):
        
        data = {
            "name": "Netflix",
            "about": "A number 1 platform",
            "website":"https//:www.netflix.com"
        }
        
        response = self.client.post(reverse('stream-platform-list'), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_stream_list(self):
        response = self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_stream_detail(self):
        response = self.client.get(reverse('stream-platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
         self.user = User.objects.create_user(username = "example2", email = "example2@example.com")
         self.token = Token.objects.get(user__username=self.user)
         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
         self.stream = StreamPlatform.objects.create(name="netflix",about="A number 1 platform",
                                                        website="http://www.netflix.com")
         
         self.watch = WatchList.objects.create(title="raj",storyline="A number 1 story",
                                               platform=self.stream, active=True)
    
    def test_watchlist_create(self):
        
        
        data = {
            "platform":self.stream,
            "title":"raj",
            "storyline":"A boy story",
            "active":True
        }
        
        response = self.client.post(reverse('movies-list'), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist(self):
        response = self.client.get(reverse('movies-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_watchdetail(self):
        response = self.client.get(reverse('movie-detail', args=(self.watch.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class ReviewTestcase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = "example2", email = "example2@example.com")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            
        self.stream = StreamPlatform.objects.create(name="netflix",about="A number 1 platform",
                                                            website="http://www.netflix.com")
            
        self.watch = WatchList.objects.create(title="raj",storyline="A number 1 story",
                                               platform=self.stream, active=True)
        self.watch2 = WatchList.objects.create(title="rajk",storyline="A number 1 jj story",
                                               platform=self.stream, active=True)
        
        self.review = Review.objects.create(review_user = self.user, rating = 3, description="A number 1 review",
                                                watchlist = self.watch2, active=True)
        
    def test_review_create(self):
        
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"A good movie",
            "watchlist":self.watch,
            "active":True
        }
        
        response = self.client.post(reverse('review-create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        
        # if user send second request it throws error
        response = self.client.post(reverse('review-create', args=(self.watch.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
         data = {
            "review_user":self.user,
            "rating":5,
            "description":"A good movie",
            "watchlist":self.watch,
            "active":True
        }
         
         self.client.force_authenticate(user=None)
         response = self.client.post(reverse('review-create', args=(self.watch.id,)), data)
         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
         
    def test_review_put(self):
        data = {
            "review_user":self.user,
            "rating":2,
            "description":"A good movie --updated",
            "watchlist":self.watch2,
            "active":False
        }
        
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 2)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watch.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         
         
       
        