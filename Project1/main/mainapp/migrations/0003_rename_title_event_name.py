# Generated by Django 5.0.2 on 2024-02-10 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='title',
            new_name='name',
        ),
    ]
