# Generated by Django 3.0.7 on 2020-08-30 05:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_merge_20200830_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='semester_preference',
            field=models.PositiveIntegerField(default=2020, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='year_preference',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
