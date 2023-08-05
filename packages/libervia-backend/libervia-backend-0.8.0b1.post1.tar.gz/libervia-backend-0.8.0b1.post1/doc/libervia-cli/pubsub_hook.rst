.. _libervia-cli_pubsub_hook:

====================================
pubsub/hook: PubSub hooks management
====================================

``hook`` is a subcommands grouping all PubSub commands related to hooks management. Hooks
are user actions launched on specific events.

3 types of hooks can be used:

``python``
  A Python module is expected as argument. The module must be available in Python path,
  and it must have a ``hook`` function.

``python_file``
  A path to a Python script is expected as argument. The script must contain a ``hook``
  function.

``python_code``
  Python code which will be directly executed. 3 variables will be set: ``host`` which
  contain the main Libervia instance, ``client`` which contain the session attached to the
  profile, and ``item`` which contain the item attached to the event.

.. note::

   Hooks are executed in Libervia context, and must be asynchronous. If they block, the whole
   Libervia execution will be blocked. They have access to everything, so don't run a code that
   you don't absolutely trust.

.. note::

   Only ``python_file`` type is currently implemented

.. note::
   Hook is an experimental feature, the way to use it may change in the future.

create
======

Create a hook of given type. Type is specified with ``-t {python,python_file,python_code},
--type {python,python_file,python_code}`` and a positional arguments is expected, which
depends on the chosen type.

By default the hook is temporary (it will be lost if the profile is disconnected), but you
can make is persistent accross reconnexions if you use the ``-P, --persistent`` argument.

example
-------

Install a persistent hook on blog node, using the Python script named
``do_something_neat.py`` in ``$HOME`` directory::

  $ li pubsub node hook create -n urn:xmpp:microblog:0 -t python_file --persistent ~/do_something_neat.py

delete
======

Delete one hook or all of them. To delete a hook, specify its type and argument (the that
you have used with ``create``). If you use empty ``--type`` and ``--arg`` all hooks will
be removed.

example
-------

Delete the ``do_something_neat.py`` hook::

  $ li pubsub node hook delete -n urn:xmpp:microblog:0 -t python_file --arg ~/do_something_neat.py

list
====

List registered hooks. The output will give the following informations:

service
  PubSub service on which the hook is attached.

node
  PubSub node on which the hook is attached.

type
  hook type

arg
  hook arguments (dependant of hook type)

persistent
  boolean indicating is the hook persist accross sessions.

example
-------

Get PubSub hooks registered for this profile in JSON::

  $ li pubsub hook list -O json

