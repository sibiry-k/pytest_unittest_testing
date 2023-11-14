from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Лев Гумилёв')
        cls.NOTE_OBJECTS_COUNT = 10
        cls.NOTE_OBJECTS_COUNT_READER = 0
        all_news = []
        for index in range(cls.NOTE_OBJECTS_COUNT):
            notes = Note(
                title=f'Замтека{index}',
                text='Просто текст.',
                author=cls.author,
                slug=f'slug{index}'
            )
            all_news.append(notes)
        Note.objects.bulk_create(all_news)

    def test_list_page_notes_count(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(
            response.context['object_list'].count(),
            self.NOTE_OBJECTS_COUNT
        )

    def test_list_page_get_notes_only_unique_user(self):
        users_notes = (
            (self.author, self.NOTE_OBJECTS_COUNT),
            (self.reader, self.NOTE_OBJECTS_COUNT_READER),
        )
        url = reverse('notes:list')
        for user, notes in users_notes:
            self.client.force_login(user)
            response = self.client.get(url)
            self.assertEqual(
                response.context['object_list'].count(),
                notes
            )

    def test_add_edit_pages_has_form(self):
        self.client.force_login(self.author)
        note = Note.objects.first()
        urls = (
            ('notes:add', None),
            ('notes:edit', (note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            response = self.client.get(reverse(name, args=args))
            self.assertIn('form', response.context)
