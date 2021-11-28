import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.models import ImageLoad
from src.settings import MEDIA_ROOT


class Resizer:
    def __init__(self, model_object: ImageLoad = None):
        self.model_object = model_object
        self.out_name = ''

    def resize(self, width, height):
        original_name, original_ext = os.path.splitext(self.model_object.title)
        self.out_name = f'{original_name}_{width}_{height}{original_ext}'
        img = Image.open(self.model_object.image.open())
        new_im = img.resize(size=(width, height))
        buffer = BytesIO()
        new_im.save(buffer, img.format)
        image = ContentFile(buffer.getvalue())
        image_file = InMemoryUploadedFile(image, None, self.out_name, 'image/jpeg', image.tell, None)
        tmp = os.path.join(MEDIA_ROOT, "resized", self.out_name)
        default_storage.save(tmp, image_file)

    def get_out_name(self):
        return self.out_name
