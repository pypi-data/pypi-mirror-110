.. _libervia-cli_pubsub_node_schema:

=========================================
pubsub/node/schema: nodes schema handling
=========================================

``node schema`` is an experimental feature to associate a data form with a PubSub node, and
reject items not following this form. This feature is currently only available with Libervia
PubSub.

Those commands can only be used by an owner of the node.

set
===

Set the schema of a node. The raw schema is written directly as positional argument.

example
-------

Set the schema for tickets node using the file ``tickets_schema.xml`` from ``$HOME``
directory. Shell substition is used here to put the content of the file in the positional
argument::

  $ li pubsub node schema set -n org.salut-a-toi.tickets:0 -s pubsub.example.org "$(<~/test_schema.xml)"


edit
====

Edit the schema of a node using your local editor (the one set in ``$EDITOR``).

If you don't change anything or publish an empty schema, the edition will be cancelled.

:ref:`draft_common` commands can be used.

example
-------

Edit the tickets node schema::

  $ li pubsub node schema edit -n org.salut-a-toi.tickets:0 -s pubsub.example.org


example
-------

get
===

Retrieve schema of a node.

example
-------

Get schema of tickets and save it to a file named ``tickets_schema.xml`` in ``$HOME``
directory::

  $ li pubsub node schema get -n org.salut-a-toi.tickets:0 -s pubsub.example.org > ~/tickets_schema.xml
