# Generated by Django 4.0.1 on 2022-02-13 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_studentprofile_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='rfid',
        ),
    ]
