# Generated by Django 3.2.9 on 2023-10-20 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simo_sonos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sonosplayer',
            old_name='master',
            new_name='slave_of',
        ),
    ]
