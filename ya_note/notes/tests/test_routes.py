from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )

    def test_anonymous_available(self):
        urls = (
            ('notes:home'),
            ('users:login'),
            ('users:logout'),
            ('users:signup'),
        )
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anonymous_non_available(self):
        login_url = settings.LOGIN_URL
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
            ('notes:success', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_authenticated_user_page_available(self):
        self.client.force_login(self.reader)
        urls = (
            ('notes:add'),
            ('notes:success'),
            ('notes:list'),
        )
        for name in urls:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_author_and_reader(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name, args in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
