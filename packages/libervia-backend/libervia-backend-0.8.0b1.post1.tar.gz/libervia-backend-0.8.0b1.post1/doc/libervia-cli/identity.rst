=============================
identity: identity management
=============================

Identity use several XMPP extensions (like vcards) to retrieve or set informations about
an entity. For now it's really basic and only nickname and avatar are managed.

get
===

Retrieve informations about the identity behind an XMPP entity. You only have to specify
the jid of the entity, and you'll get (if set) his/her/its nickname and data about the
avatar.

When available, cached values are returned by defaut. If you want to ignore the cache, use
the ``--no-cache`` option (of course this can result in more network requests).

example
--------

Get identity information about an entity::

  $ li identity get somebody@example.org

set
===

Set identity data to the server, using various XMPP extensions. So far, you can only
change the nickname of an entity using ``-n, --nick`` or or more times

example
-------

Set 2 nicknames for default profile::

  $ li identity set -n toto -n titi
