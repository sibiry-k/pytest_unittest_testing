import pytest
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Новость № 1',
    )


@pytest.fixture
def news_objects():
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    news_objects = News.objects.bulk_create(all_news)
    return news_objects


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comments


@pytest.fixture
def form_data():
    return {
        'news': news,
        'author': author,
        'text': 'Текст комментария из формы'
    }
