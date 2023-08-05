.. _libervia-cli_pubsub_node:

====================================
pubsub/node: PubSub nodes management
====================================

``node`` is a subcommands grouping all PubSub commands related to node management. For
details on ``pubsub`` command itself, refer to :ref:`libervia-cli_pubsub`.

info
====

Get settings of the node. Use ``-k KEYS, --key KEYS`` to select data to print.

examples
--------

Get informations on our personal microblog node::

  $ li pubsub node info -n urn:xmpp:microblog:0

Only print ``access_model`` and ``publish_model``::

  $ li pubsub node info -n urn:xmpp:microblog:0 -k access_model -k publish_model

.. _libervia-cli_pubsub_node_create:

create
======

Create a node. Node configuration can be specified using ``-f KEY VALUE, --field KEY
VALUE`` where ``KEY`` is a pubsub option. By default the ``pubsub#`` prefix will be
appended, as it is used with standard options (see `XEP-0060`_ for more details); to
change this behaviour, use the ``-F, --full-prefix`` flag.

.. _XEP-0060: https://xmpp.org/extensions/xep-0060.html

example
--------

Create a node called ``notes`` with a ``whitelist`` access model (so only you and people
you may authorize later can access it)::

  $ li pubsub node create -n notes

purge
=====

Remove all items from a node (but don't delete the node).

A confirmation is requested by default, you can override this behaviour by using ``-f, --force`` option.

example
-------

Remove all items from a blog comments node (in other words, removing all comments while
letting the node so people can add new comments)::

  $ li pubsub node purge -n "urn:xmpp:microblog:0:comments/123-456-789"

delete
======

Delete a node (note that this will delete definitively all items that where published to
this node).

A confirmation is requested by default, you can override this behaviour by using ``-f, --force`` option.

example
-------

Delete the ``temporary_notes`` node::

  $ li pubsub node delete -n temporary_notes

set
===

Update a node configuration.

Configuration options are specified using ``-f KEY VALUE, --field KEY VALUE`` argument
where ``KEY`` is a PubSub option. If ``KEY`` doesn't start with ``pubsub#`` prefix, it is
added automatically, except if ``-F, --full-prefix`` argument is used (in which case the
``KEY`` is used as specified.

example
-------

Make the ``public_notes`` node accessible to the world::

  $ li pubsub node set -n public_notes -f access_model open

import
======

Import a raw XML containing items to create in the node. The path to the XML file is used
as positional argument.

The XML file must contain full `<item>` element for each item to import. The output of ``pubsub get`` can be used directly.

If you want to change publisher of one or more items (i.e. if you want to use an other ``jid`` than the jid of the profile as publisher), you must use the ``--admin`` arguments. This needs a PubSub service supporting this feature (and you must of course be an administrator of this service). The new publisher must be allowed to publish to the node.

example
-------

Import a node backup which has previously been saved using ``li blog get -M -1 -n
some_node > some_node_backup.xml``::

  $ li pubsub node import -n some_node ~/some_node_backup.xml

.. note::

   If your node is big, -M 1 option is not adapted as it will get all items at once and
   may be blocked by your server stanza size limit. The possibility to use RSM to
   retrieve all items by pages is planned in a future version.

affiliations
============

Subcommands for node affiliations management. Please check :ref:`libervia-cli_pubsub_node_affiliations`.

subscriptions
=============

Subcommands for node subscriptions management. Please check
:ref:`libervia-cli_pubsub_node_subscriptions`.
