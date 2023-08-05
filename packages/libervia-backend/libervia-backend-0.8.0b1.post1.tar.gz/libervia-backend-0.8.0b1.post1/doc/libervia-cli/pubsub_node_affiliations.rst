.. _libervia-cli_pubsub_node_affiliations:

=======================================================
pubsub/node/affiliations: nodes affiliations management
=======================================================

``affiliations`` is a subcommand handling the affiliations of a node (not to be confused
with ``pubsub affiliations`` which handle the affiliations of a PubSub service).

get
===

Retrieve entities affiliated to this node and their role.

example
-------

Get affiliations of a node::

  $ li pubsub node affiliations get -n some_node

set
===

Set affiliation of an entity on a node. Affiliations are specified with ``-a JID
AFFILIATION`` argument. Check `XEP-0060 affiliations`_ for allowed values for
``AFFILIATION``. Use ``none`` to remove an affiliation.

.. _XEP-0060 affiliations: https://xmpp.org/extensions/xep-0060.html#affiliations

example
-------

If we have a whitelisted node ``some_whitelisted_node``, we can allow
``louise@example.net`` to publish on it (by setting her role as ``publisher``), and
``pierre@example.net`` to access it (by setting his role as ``member``) using the
following command::

  $ li pubsub node affiliations set -n some_whitelisted_node -a louise@example.net
  publisher -a pierre@example.net member
