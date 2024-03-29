from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatfrom.objects.create(name="Netflix", about="#1 Streaming Platform",
                                                           website="https://netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatfrom.objects.create(name="Netflix", about="#1 Streaming Platform",
                                                           website="https://netflix.com")
        self.watchlist = models.Watchlist.objects.create(platform=self.stream, title="Example movie",
                                                         storyline="Example Movie", active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active": True
        }

        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.get().title, 'Example Movie')


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatfrom.objects.create(name="Netflix", about="#1 Streaming Platform",
                                                           website="https://netflix.com")
        self.watchlist = models.Watchlist.objects.create(platform=self.stream, title="Example movie",
                                                         storyline="Example Movie", active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 3,
            "description": "Not Great Movie!",
            "watchlist": self.watchlist,
            "active": False
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
