=======================
ad-hoc: Ad-Hoc commands
=======================

Ad-Hoc commands is a generic mechanism of XMPP to control an entity. They can be used
either by humans, or automated. Ad-Hoc commands can be used for administration (e.g. get
list of connected users, send a service announcement, restart parts of the server), or
execute about anything (e.g. control a physical robot with XMPP).

run
===

Run an ad-hoc command. You may specify the node to run as positional argument, or let it
empty to list available commands.

By default the commands from your server are used, but with ``-j JID, --jid JID`` you can
specify a different entity.

You can automatically execute commands by using ``-f KEY VALUE, --field KEY VALUE`` and
``-S, --submit`` as many time as needed.  ``--field`` expect a ``KEY`` which is the name
of the field to set. If you don't know which name to use, you can run the command to
automatise a first time manually with ``--verbose, -v`` flag, this will display fields
names when you have to fill them.

Once all fields of a page are specified, you may use ``-S, --submit`` to validate it, then
if suitable use again ``--field`` to set fields of next page and ``--submit`` again, and
so on as many times as you need.

Don't forget that you can use your shell substitution capabilities if necessary, for
instance if you have a pre-registered announce to send.

examples
--------

Get a list of available commands on your server to launch a command::

  $ li ad-hoc run

If your server supports `XEP-0133`_ and you're an admin on it, you can send announcements
to online users. This can be useful to notify an imminent maintenance of the server. Here
we notify online users that the server will be shutdown in 30 min, using a shell
substitution capabilities with a pre-registered message in the file
``~/announces/maintenance_30.txt``, then we submit it::

  $ li ad-hoc run "http://jabber.org/protocol/admin#announce" -f subject "Maintenance in 30 min" -f announcement "$(<~/announces/maintenance_30.txt)" -S

Get your server uptime (if supported by your server)::

  $ li ad-hoc run uptime

Run the commands available at the service with the jid ``someservice.example.org``::

  $ li ad-hoc run -s someservice.example.org

Run you server commands with verbosity so you get the name of the fields that you can fill
automatically later::

  $ li ad-hoc run -v

.. _XEP-0133: https://xmpp.org/extensions/xep-0133.html

list
====

List ad-hoc commands available at a service.

examples
--------

List ad-hoc commands available at your server::

  $ li ad-hoc list

List ad-hoc commands available at a chat service::

  $ li ad-hoc list -j conference.example.org

remote
======

Create a remote control from launched media players. Ad-hoc commands to control the media
player will be added to your device, allowing anybody allowed (including yourself from an
other device, e.g. a phone) to remotely do action like ``play``, ``pause``, etc.

To add a device, just use the name of the software (e.g. ``vlc``, ``smplayer``). You can
specify who is allowed to control this media player with the following options:

``-j [JIDS [JIDS ...]], --jids [JIDS [JIDS ...]]``
  jids of entities allowed to control the media player

``g [GROUPS [GROUPS ...]], --groups [GROUPS [GROUPS ...]]``
  groups (from your roster) allowed to control you remote

``--forbidden-groups [FORBIDDEN_GROUPS [FORBIDDEN_GROUPS ...]]``
  groups (from your roster) which are **NOT** allowed to control your media player

``--forbidden-jids [FORBIDDEN_JIDS [FORBIDDEN_JIDS ...]]``
  jids of entities which are **NOT** allowed to control your media player

If you want the commands to run repeatedly (in opposition of stopping after first action
is sent), you may use the ``-l, --loop`` option. Most of time you'll want to use it.

.. note::

   Libervia already creates automatically a remote control if it finds a media player. This
   manual way to create a remote control predate the automatic remote control, and is
   currently more flexible in that you can specify who can access the remote control
   (automatic remote control is only accessible by the jid of the profile).

examples
--------

Create a remote control for a running VLC instance::

  $ li ad-hoc remote vlc -l

Create a remote control for a running SMPlayer instance, and allowing anybody from your
``housemates`` group to use it::

  $ li ad-hoc remote smplayer -g housemates -l
