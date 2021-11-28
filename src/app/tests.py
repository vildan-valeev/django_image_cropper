from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import ImageLoad


class ImageLoadTestCase(TestCase):
    # def setUp(self):
    #     pass

    def test_create_image_load_instance(self):
        new_instance = ImageLoad()
        new_instance.title = 'test_image.jpg'
        image_path = 'test_image.jpg'
        new_instance.image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(),
                                                content_type='image/jpeg')
        new_instance.save()
        self.assertEqual(ImageLoad.objects.count(), 1)

