import traceback
import sys
from datetime import timedelta
from simo.multimedia.controllers import BaseAudioPlayer
from simo.core.events import GatewayObjectCommand
from .models import SonosPlayer, SonosPlaylist
from .gateways import SONOSGatewayHandler
from .forms import SONOSPlayerConfigForm


class SONOSPlayer(BaseAudioPlayer):
    gateway_class = SONOSGatewayHandler
    config_form = SONOSPlayerConfigForm

    def unjoin(self):
        sonos_player = SonosPlayer.objects.filter(
            id=self.component.config['sonos_device']
        ).first()
        if not sonos_player:
            return
        try:
            sonos_player.soco.unjoin()
        except:
            print(traceback.format_exc(), file=sys.stderr)

    def play_uri(self, uri, volume=None):
        if volume:
            assert 0 <= volume <= 100
        self.send({"play_uri": uri, 'volume': volume})

    def play_alert(self, val, volume=None):
        '''Val can be sound id or uri'''
        assert type(val) in (int, str)
        if volume:
            assert 0 <= volume <= 100
        self.send({"alert": val, 'volume': volume})

    def _send_to_device(self, value):
        sonos_player = SonosPlayer.objects.get(
            id=self.component.config['sonos_device']
        )
        if value in (
            'play', 'pause', 'stop', 'next', 'previous',
        ):
            getattr(sonos_player.soco, value)()
        elif isinstance(value, dict):
            if 'seek' in value:
                sonos_player.soco.seek(timedelta(seconds=value['seek']))
            elif 'set_volume' in value:
                sonos_player.soco.volume = value['set_volume']
            elif 'shuffle' in value:
                sonos_player.soco.shuffle = value['shuffle']
            elif 'loop' in value:
                sonos_player.soco.repeat = value['loop']
            elif 'play_from_library' in value:
                if value['play_from_library'].get('type') != 'sonos_playlist':
                    return
                playlist = SonosPlaylist.objects.filter(
                    id=value['play_from_library'].get('id', 0)
                ).first()
                if not playlist:
                    return
                sonos_player.play_playlist(playlist)
            elif 'play_uri' in value:
                if value.get('volume') != None:
                    sonos_player.soco.volume = value['volume']
                sonos_player.soco.play_uri(value['play_uri'])
            elif 'alert' in value:
                GatewayObjectCommand(
                    self.component.gateway, self.component,
                    set_val=value
                ).publish()

        GatewayObjectCommand(
            self.component.gateway, self.component, set_val='check_state'
        ).publish()

    def play_playlist(self, item_id, shuffle=True):
        from simo_sonos.models import SonosPlayer
        sonos_player = SonosPlayer.objects.filter(
            id=self.component.config['sonos_device']
        ).first()
        if not sonos_player:
            return
        for plst in sonos_player.soco.get_sonos_playlists():
            if plst.item_id == item_id:
                try:
                    sonos_player.soco.clear_queue()
                    sonos_player.soco.shuffle = shuffle
                    sonos_player.soco.add_to_queue(plst)
                    sonos_player.soco.play()
                    self.component.value = 'playing'
                    self.component.save()
                except:
                    print(traceback.format_exc(), file=sys.stderr)
                return
