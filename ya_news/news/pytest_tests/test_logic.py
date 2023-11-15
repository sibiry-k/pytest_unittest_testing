import pytest
from http import HTTPStatus

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    news = response.context['news']
    comments_count_before = news.comment_set.count()
    client.post(url, form_data)
    response = client.get(url)
    news = response.context['news']
    comments_count_after = news.comment_set.count()
    assert comments_count_before == comments_count_after


@pytest.mark.django_db
def test_author_can_create_comment(author_client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    news = response.context['news']
    comments_count_before = news.comment_set.count()
    author_client.post(url, form_data)
    response = author_client.get(url)
    news = response.context['news']
    comments_count_after = news.comment_set.count()
    assert comments_count_before + 1 == comments_count_after


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news):
    comments_count_before = news.comment_set.count()
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assert WARNING in response.context['form'].errors['text']
    comments_count_after = news.comment_set.count()
    assert comments_count_before == comments_count_after


@pytest.mark.django_db
@pytest.mark.usefixtures('comment')
def test_author_can_delete_comment(author_client, news, comment):
    url = reverse('news:delete', args=(comment.id,))
    comments_count_before = news.comment_set.count()
    author_client.delete(url)
    comments_count_after = news.comment_set.count()
    assert comments_count_after + 1 == comments_count_before


@pytest.mark.django_db
@pytest.mark.usefixtures('comment')
def test_user_cant_delete_comment(user_client, news, comment):
    url = reverse('news:delete', args=(comment.id,))
    comments_count_before = news.comment_set.count()
    user_client.delete(url)
    comments_count_after = news.comment_set.count()
    assert comments_count_after == comments_count_before


@pytest.mark.django_db
@pytest.mark.usefixtures('comment')
def test_author_can_edit_comment(author_client, comment):
    NEW_COMMENT_TEXT = 'Текст нового комментария'
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, data={'text': NEW_COMMENT_TEXT})
    response = author_client.get(url)
    assert response.context['comment'].text == NEW_COMMENT_TEXT


@pytest.mark.django_db
@pytest.mark.usefixtures('comment')
def test_user_cant_edit_comment(user_client, comment):
    NEW_COMMENT_TEXT = 'Текст нового комментария'
    url = reverse('news:edit', args=(comment.id,))
    response = user_client.post(url, data={'text': NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != NEW_COMMENT_TEXT
