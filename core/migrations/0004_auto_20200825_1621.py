# Generated by Django 3.0.7 on 2020-08-25 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_studentresponse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentresponse',
            old_name='questions',
            new_name='response',
        ),
    ]