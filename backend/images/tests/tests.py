import tempfile

import pytest
from django.contrib.auth import get_user_model
from images.models import UploadedImage
from PIL import Image

User = get_user_model()


@pytest.fixture
def temporary_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return tmp_file


@pytest.fixture
def user():
    return User.objects.get_or_create(username='test_user')[0]


@pytest.fixture
def superuser():
    return User.objects.get_or_create(username='test_user2', is_superuser=True)[0]


@pytest.mark.django_db
def test_post_create_img(client, user, temporary_image):
    data = {
        'name': 'How to tame the T-rex',
        'user': user.id,
        'img': temporary_image,
    }
    client.force_login(user)
    response = client.post('/api/img/', data)

    assert response.status_code == 201
    assert UploadedImage.objects.count() == 1


@pytest.mark.django_db
def test_post_no_overwrite_user(client, user, superuser, temporary_image):
    data = {
        'name': 'How to tame the T-rex',
        'user': superuser.id,
        'img': temporary_image,
    }
    client.force_login(user)
    response = client.post('/api/img/', data)

    assert response.status_code == 201
    assert UploadedImage.objects.count() == 1
    assert UploadedImage.objects.first().user == user


@pytest.mark.django_db
def test_list_display_img(client, user, superuser):
    UploadedImage.objects.create(name='test', user=user, img=None)
    UploadedImage.objects.create(name='test2', user=user, img=None)
    UploadedImage.objects.create(name='test2', user=superuser, img=None)
    client.force_login(user)
    response_user = client.get('/api/img/')

    client.force_login(superuser)
    response_su = client.get('/api/img/')

    assert response_user.status_code == 200
    assert len(response_user.data) == 2
    assert response_su.status_code == 200
    assert len(response_su.data) == 3
