import inspect
from django.db import models
from django.contrib import admin
from soco import SoCo


class SonosPlayer(models.Model):
    slave_of = models.ForeignKey(
        'SonosPlayer', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='slaves'
    )
    uid = models.CharField(max_length=200, db_index=True, unique=True)
    name = models.CharField(max_length=200, db_index=True)
    ip = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now_add=True)
    is_alive = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soco = SoCo(self.ip)

    def __str__(self):
        return self.name


class SonosPlaylist(models.Model):
    player = models.ForeignKey(SonosPlayer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    item_id = models.CharField(max_length=200)

    class Meta:
        unique_together = 'player', 'item_id'

    def __str__(self):
        return f"{self.title} on {self.player}"
