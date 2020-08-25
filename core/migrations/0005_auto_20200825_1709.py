# Generated by Django 3.0.7 on 2020-08-25 07:09

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200825_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionnaireTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('questions', models.TextField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='date_completed',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='date_started',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
