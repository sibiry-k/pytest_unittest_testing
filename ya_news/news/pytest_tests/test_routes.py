from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_home_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_edit_delete_comment_page_availability_author(
    author_client, name, comment
):
    url = reverse(name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment')),
    ),
)
def test_redirects(client, name, comment_object):
    login_url = settings.LOGIN_URL
    url = reverse(name, args=(comment_object.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_edit_delete_comment_page_not_availability_non_author(
    user_client, name, comment
):
    url = reverse(name, args=(comment.id,))
    response = user_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
