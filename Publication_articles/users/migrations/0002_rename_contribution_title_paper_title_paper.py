# Generated by Django 4.2.1 on 2023-11-27 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='contribution_title',
            new_name='title_paper',
        ),
    ]
