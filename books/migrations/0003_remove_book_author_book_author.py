# Generated by Django 4.0.1 on 2022-02-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookcopies_is_book_available_bookcopies_is_book_lost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
