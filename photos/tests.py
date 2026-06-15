import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Photo


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PhotoViewTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def make_photo(self, **kwargs):
        defaults = {
            'title': 'Morning Light',
            'alt_text': 'Sunlight over a quiet street',
            'description': 'A local test photo.',
            'image': SimpleUploadedFile(
                'photo.jpg',
                b'test image content',
                content_type='image/jpeg',
            ),
        }
        defaults.update(kwargs)
        return Photo.objects.create(**defaults)

    def test_photo_list_shows_only_published_photos(self):
        published = self.make_photo(title='Published Photo')
        self.make_photo(title='Draft Photo', is_published=False)

        response = self.client.get(reverse('photos_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published.title)
        self.assertNotContains(response, 'Draft Photo')

    def test_photo_detail_requires_published_photo(self):
        draft = self.make_photo(title='Hidden Photo', is_published=False)

        response = self.client.get(reverse('photo_detail', args=[draft.id]))

        self.assertEqual(response.status_code, 404)

    def test_photo_detail_renders_metadata(self):
        photo = self.make_photo(
            title='Harbour Walk',
            location='Qingdao',
            camera='Fujifilm X-T30',
        )

        response = self.client.get(photo.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harbour Walk')
        self.assertContains(response, 'Qingdao')
        self.assertContains(response, 'Fujifilm X-T30')

    def test_homepage_includes_published_photos_context(self):
        self.make_photo(title='Homepage Photo')
        self.make_photo(title='Hidden Homepage Photo', is_published=False)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Homepage Photo')
        self.assertNotContains(response, 'Hidden Homepage Photo')
