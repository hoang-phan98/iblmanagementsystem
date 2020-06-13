# Generated by Django 3.0.7 on 2020-06-13 05:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
                ('role', models.CharField(max_length=256)),
                ('department', models.CharField(max_length=256)),
                ('student_id', models.IntegerField()),
                ('company_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=256)),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Placement')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='placement',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.Placement'),
        ),
    ]
