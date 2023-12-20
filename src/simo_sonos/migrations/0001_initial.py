# Generated by Django 3.2.9 on 2023-10-20 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SonosPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(db_index=True, max_length=200, unique=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('ip', models.GenericIPAddressField()),
                ('last_seen', models.DateTimeField(auto_now_add=True)),
                ('is_alive', models.BooleanField(default=True)),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slaves', to='simo_sonos.sonosplayer')),
            ],
        ),
        migrations.CreateModel(
            name='SonosPlaylist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('item_id', models.CharField(max_length=200, unique=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simo_sonos.sonosplayer')),
            ],
            options={
                'unique_together': {('player', 'item_id')},
            },
        ),
    ]
