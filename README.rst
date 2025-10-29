=================================
Sonos integration for SIMO.io
=================================

Local‑first Sonos control on a SIMO.io hub. This app adds a SONOS
gateway and an Audio Player controller so you can discover Sonos players,
start/stop playback, control volume, shuffle and loop, seek, start
Sonos Playlists, and play one‑shot alert sounds — all from the SIMO.io app
and Django Admin.

What you get (at a glance)
--------------------------

* Gateway type: ``SONOS`` (no extra configuration).
* Component type: ``Audio player`` using the SONOS controller.
* Automatic discovery of Sonos players (group coordinators) and their
  Sonos Playlists.
* Playback controls: play, pause, stop, next, previous, seek, volume,
  shuffle, loop.
* Optional alert playback that snapshots, plays a sound, then restores.
* Entirely local on your LAN via SoCo; no cloud required.

Requirements
------------

* SIMO.io core ``>= 1.5.9`` (installed on your hub).
* Python ``>= 3.8``.
* Hub and Sonos players reachable on the same LAN or with multicast
  forwarding. Discovery relies on Sonos UPnP/SSDP; if you segment VLANs,
  ensure multicast reaches the hub or allow the SoCo network scan fallback.
* For alerts: Sonos players must be able to fetch media from the hub over
  HTTP (the hub’s LAN IP must be reachable from Sonos devices).

Install on a SIMO.io hub
------------------------

1. SSH to your hub and activate the hub’s Python environment
   (for example ``workon simo-hub``).

   .. code-block:: bash

      # On the hub
      workon simo-hub   # or activate your hub venv

2. Install the package.

   .. code-block:: bash

      pip install simo-sonos

3. Enable the app in Django settings (``/etc/SIMO/settings.py``).

   .. code-block:: python

      # /etc/SIMO/settings.py
      from simo.settings import *  # keep platform defaults

      INSTALLED_APPS += [
          'simo_sonos',
      ]

4. Apply migrations from this app.

   .. code-block:: bash

      cd /etc/SIMO/hub
      python manage.py migrate

5. Restart SIMO services so the new app and gateway type load.

   .. code-block:: bash

      # Typical: restart app and workers; adjust to your setup
      supervisorctl restart all
      # or restart selected: simo-gunicorn, worker/scheduler

Discovery runs periodically; after installation and restart, give it a
little time to find players. Only Sonos group coordinators are
registered; group member speakers follow their coordinator.

Add a Sonos audio player component
----------------------------------

Once players are discovered:

1. In the SIMO.io app: Components → Add New → Component.
2. Choose base type: ``Audio player``.
3. Choose controller: SONOS (if prompted).
4. Configure “Sonos device” — pick the discovered player (group
   coordinator) from the dropdown.
5. Save. The component’s alive/state will reflect the device.

Using it in the SIMO.io app
---------------------------

The Audio Player widget exposes playback and state:

* Play / Pause / Stop; Next / Previous.
* Seek position (seconds), if the current item supports it.
* Volume 0–100, Shuffle, Loop/Repeat toggles.
* Library: Sonos Playlists discovered on that player. Pick one to start
  playback; optional fade‑in is supported via scripts (see below).

Advanced controls (automations / scripts)
-----------------------------------------

Behind the scenes, the controller supports these calls; you can use them
from SIMO.io Python scripts or admin tooling:

* ``play_library_item(id, volume=None, fade_in=None)`` — start a Sonos
  Playlist item known to this player. The library list in the component’s
  meta tells you available IDs.
* ``play_uri(uri, volume=None)`` — replace the queue with a single URI
  (e.g., an HTTP stream) and play immediately.
* ``set_volume(0..100)``, ``set_shuffle_play(True/False)``,
  ``set_loop_play(True/False)``, ``seek(seconds)``.
* Alerts: trigger via the SIMO “Audio Alert” component — the SONOS gateway
  will snapshot, play the sound over Sonos, then restore prior playback.

Notes on discovery and grouping
-------------------------------

* Only group coordinators are listed/selectable. Members of a group play
  in lock‑step with the coordinator.
* To split a speaker from its group, ungroup it in the Sonos app. The
  controller also exposes an ``unjoin()`` method for advanced users.
* Playlists come from Sonos Playlists on the device; if you see an empty
  library, create a playlist in the Sonos app and let discovery refresh.

Django Admin
------------

This app adds a tidy, read‑only registry of discovered devices:

* ``Sonos players`` — list view shows name/UID, IP, alive state,
  last seen, and whether it’s a group master. You cannot add devices here;
  they are discovered automatically.
* Player detail page lists ``Sonos playlists`` for that player (inline).
* Your Audio Player components (base type ``audio-player``) reflect live
  state and metadata (title, position, duration, volume, shuffle, loop,
  library). The gateway instance page shows logs useful while testing.
* Gateway management lives in Django Admin. After you restart the
  supervisord processes post‑install, a ``SONOS`` gateway is created
  automatically with default settings. Open it to view live logs of
  commands and state updates.

Troubleshooting
---------------

* No players show up:
  - Ensure services were restarted after installation.
  - Check that the hub and Sonos players are on the same network or that
    multicast (SSDP) reaches the hub. Wait for the next discovery cycle.
* Library is empty: Create at least one Sonos Playlist on that player and
  wait for discovery to refresh.
* Alerts don’t play: Sonos must reach the hub over HTTP (the hub’s LAN IP).
  Confirm that the hub is reachable from the speaker’s subnet and that
  firewalls are not blocking it.
* Grouping confusion: Only group coordinators appear as selectable devices.
  Ungroup speakers in the Sonos app if you need separate components.

Upgrade
-------

.. code-block:: bash

   workon simo-hub
   pip install --upgrade simo-sonos
   python manage.py migrate
   supervisorctl restart all


License
-------

© Copyright by SIMO LT, UAB. Lithuania.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see `<https://www.gnu.org/licenses/>`_.
