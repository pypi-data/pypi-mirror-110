
==================================
info: retrieve various information
==================================

``info`` groups subcommands used to retrieve read-only informations.

disco
=====

Display discovery information (see `XEP-0030`_ for details). This can be used to check
which features you server or a service is offering, and which items are available (items
can be services like chat room, gateways, etc).

You only have to specify the jid of the entity to check, and optionally a node.

By default both infos and items are requested, but you can restrict what to request by
using ``-t {infos,items,both}, --type {infos,items,both}``

.. _XEP-0030: https://xmpp.org/extensions/xep-0030.html


example
-------

Request infos and items from a server::

  $ li info disco example.org

version
=======

Request software version of an entity. You only need to specify the jid of the entity as
positional argument.

Depending of the software and its configuration, you have software version, software name,
and the operating system on which the software is running.

example
-------

Check version of a server::

  $ li info version example.org

session
-------

Give information about the session of the given profile. You'll get the full jid currently
used on the server, and the time when the session was started (which may not be the same
time as when the connection with the XMPP server was started).

example
-------

Get session informations::

  $ li info session

devices
-------

List known devices for an entity. You'll get resource name, and data such as presence
data, and identities (i.e. name and type of the client used).

If entity's bare jid is not specified, a list of your own devices is returned.

example
-------

List known devices of Louise::

  $ li info devices louise@example.org

Check if we have other devices connected::

  $ li info devices
