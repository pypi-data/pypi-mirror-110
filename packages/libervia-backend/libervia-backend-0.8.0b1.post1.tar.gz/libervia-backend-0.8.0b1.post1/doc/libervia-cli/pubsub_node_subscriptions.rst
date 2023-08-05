.. _libervia-cli_pubsub_node_subscriptions:

========================================================
pubsub/node/affiliations: nodes subscriptions management
========================================================

``subscriptions`` is a subcommand handling the subscription to a node.

Those commands can only be used by an owner of the node.

get
===

Retrieve subscriptions to a node.

example
-------

Get subscription from ``some_node``::

  $ li pubsub node subscriptions get -n some_node

set
===

Set subscriptions to a node. Subscriptions are specified with ``-S JID [SUSBSCRIPTION]
[JID [SUSBSCRIPTION] ...], --subscription JID [SUSBSCRIPTION] [JID [SUSBSCRIPTION] ...]``
where ``JID`` is the jid of the entity to change subscription state, and ``SUBSCRIPTION``
is a subscription state (on of ``subscribed``, ``pending``, ``none``) as specified in
`XEP-0060 Subscription State`_. If ``SUBSCRIPTION`` is not specified, it default to
``subscribed``.

.. _XEP-0060 Subscription State: https://xmpp.org/extensions/xep-0060.html#substates

example
-------

Subscribe Louise with her new address at ``louise@example.org`` and remove her
subscription from old ``louise@example.com``::

  $ li pubsub node subscriptions set -n some_node -S louise@example.org subscribed louise@example.com none


