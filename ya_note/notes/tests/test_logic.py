from http import HTTPStatus

from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestLogic(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Пользователь')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author = User.objects.create(username='Лев Толстой')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.slug = 'slug'
        cls.note = Note.objects.create(
            title='Заголовок',
            text=cls.NOTE_TEXT,
            author=cls.author,
            slug=cls.slug,
        )
        cls.form_data = {
            'title': 'Заголовок',
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.slug,
        }
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')

    def test_not_unique_slug_warning(self):
        url = reverse('notes:add')
        response = self.auth_client.post(url, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{self.slug}{WARNING}',
        )

    def test_anonymous_can_not_create_note(self):
        form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
        }
        notes_count_before = Note.objects.count()
        url = reverse('notes:add')
        self.client.post(url, data=form_data)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_before, notes_count_after)

    def test_author_can_create_note(self):
        form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
        }
        notes_count_before = Note.objects.count()
        url = reverse('notes:add')
        self.auth_client.post(url, data=form_data)
        notes_count_after = Note.objects.count()
        self.assertNotEqual(notes_count_before, notes_count_after)

    def test_user_cant_delete_note_another_user(self):
        notes_count_before = Note.objects.count()
        response = self.user_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_before, notes_count_after)

    def test_author_can_delete_note(self):
        notes_count_before = Note.objects.count()
        response = self.auth_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count_after = Note.objects.count()
        self.assertNotEqual(notes_count_before, notes_count_after)

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_another_user(self):
        response = self.user_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)


class TestLogicSlug(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )

    def test_empty_slug_field_use_slugify(self):
        note_slug = self.note.slug
        slugify_slug = slugify(self.note.title)
        self.assertEqual(note_slug, slugify_slug)
