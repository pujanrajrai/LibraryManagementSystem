# Generated by Django 4.0.1 on 2022-04-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profiles_rf_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
