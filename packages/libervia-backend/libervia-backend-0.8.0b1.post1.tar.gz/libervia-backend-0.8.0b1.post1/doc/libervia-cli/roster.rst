================================
roster: manager an entity roster
================================

"Roster" is the name used in XMPP for the contact list. In addition to list of contacts,
you have also data like subscription information or groups associated to a contact.

Groups are simple strings associated to one or more contacts (e.g. "friends" or "family").

Subscription is the mechanism to get presence information of an entity. When you add a
contact to your roster, most XMPP clients also do a presence subscription request, than
the entity may accept or deny. If a presence subscription is accepted, the subscribed user
can see when the other entity is online, and its presence status.

get
===

Show the current roster. By default only a display name and JIDs are displayed, but you
can increase verbosity to also display groups, or all other metadata.

The short name shown next to jid is either the ``name`` specified in roster, or the node
part of the jid. If none of them exist, only the entity JID is shown.

The following metadata may be displayed:

groups
  group the entity belong too
ask
  true if a presence subscription request has been sent (but not answered yet)
from
  the contact has a subscription to user presence (i.e. your contact can see when you're
  online and your presence status)
to
  the user has a subscription to the contact presence (i.e. you can see when you're
  contact is online and his/her presence status)

examples
--------

Get roster of default profile and display groups::

  $ li roster get -v

Get roster of default profile and display all metadata::

  $ li roster get -vv

Get roster or default profile and show the result in JSON::

  $ li roster get -O json

set
===

Set metadata for a roster entity. Only ``name`` and ``groups`` can be set, ``name`` being
the user chosed name to use with a contact.

By default, values are appended, i.e. if ``name`` is not set it won't delete existing one,
and ``groups`` are appended to existing one. However, if you use the ``-R, --replace``
option, former values will be entirely replaced by given ones (i.e. if you don't use ``-n
NAME, --name NAME`` option, the former one will be deleted, and any former group no added
using ``-g GROUP, --group GROUP`` will be removed).

examples
--------

Set a name used to privately identify your contact Louise::

  $ li roster set -n Enjolras louise@example.net

Replace all groups of Pierre, to add him only to ``friends`` and ``housemates``::

  $ li roster set --replace -g friends -g housemates pierre@example.net

delete
======

Remove an entity from roster.

examples
--------

Remove John from your roster::

  $ li roster delete john@example.net

stats
=====

Show some statistics about the profile roster. The number of contacts per server is shown,
with a percentage of contacts on this server compared to the total number of contacts.
This can notably be helpful to see if there is a concentration of your contacts in a
specific server or gateway.

Other more or less useful numbers are shown, they are self explaining.

example
-------

Get statistic for the default profile::

  $ li roster stats

purge
=====

This command is used to remove from the roster all contacts which have no subscription or
only partial subscription.

By default, only contacts without subscription at all are removed. With ``--no-from`` you
also remove contacts which have no subscription to you (but you have a subscription to
them), and with ``--no-to`` you also remove contacts that you are not subscribed to (but
who are subscribed to you).

example
-------

Remove all contacts from default profile which have no subscription at all or from which
the default profile is not subscribed to::

  $ li roster purge --no-to

resync
======

Libervia uses `roster versioning`_ to optimize the synchronisation of roster with server on
client connection. This means that once the roster has been retrieved, on each following
connection, only the difference of contacts (i.e. which new or removed contacts) is
received.

This command does a full resynchronisation of the roster, or in other words it requests
the whole roster and save it, replacing the list built with versioning. ``resync`` is
mostly useful for developers and end-user should not need this command, as roster
versioning is supposed to work fine and the roster should be synchronised correctly on
startup. But if for any reason you suspect that your current roster list is corrupted, you
may use it to be sure that a full resynchronisation is done.

.. _roster versioning: https://tools.ietf.org/html/rfc6121#section-2.6

exemple
-------

Do a full resynchronisation of default profile's roster::

  $ li roster resync
