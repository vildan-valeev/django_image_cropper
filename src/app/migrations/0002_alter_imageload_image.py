# Generated by Django 3.2.3 on 2021-11-14 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageload',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/images', verbose_name='Файл'),
        ),
    ]