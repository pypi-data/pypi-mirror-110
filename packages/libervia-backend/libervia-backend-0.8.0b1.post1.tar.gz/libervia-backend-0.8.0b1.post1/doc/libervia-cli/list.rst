=================================
list: create and manage lists
=================================

list is a generic tools to create items with metadata and states (where state can be
``queued``, ``done``, etc). This can be used for many things, from TODO list to bugs
management.

get
===

Retrieve one or more lists and display them. A project may use magic string in README to
indicate PubSub service and node to use, in which case use just need to be in the
directory of the project.

examples
--------

Retrieve last 5 lists (ordered by creation) from a project using magic string in README::

  $ li list get -m 5 -o creation

Retrieve the list with id ``123`` on service ``pubsub.example.org``::

  $ li list get -s pubsub.example.org -i 123


set
===

Create/replace or update a list item. You can specify fields using the ``-f NAME [VALUES
...], --field NAME [VALUES ...]``, several values can be set. For ``text-multi`` (multiple
lines of text), each line is set in distinct value.

The ``-U {auto,true,false}, --update {auto,true,false}`` indicates if the item must be
updated (non specified values are kept) or fully replaced (non specified values would then
be default, even if they were previously set in the item). If ``auto`` is used (this is
the default), ``--update=true`` is used when ``item_id`` is specified, otherwise a new
item is created.

If ``-n NODE, --node NODE`` is not specified, it uses tickets default namespace.

examples
--------

Modify priority of a ticket with id ``123`` to ``major`` (the ticket is updated and not
replaced due to the default ``--update auto``)::

  $ li list set -s pubsub.example.org -i 123 -f priority major

Set ``body`` for a new item when its schemas makes it a ``text-multi``::

  $ li list set -s pubsub.example.org -f body "line 1" "line 2" "line 3"

delete
======

Delete an item from a list. The options are the same as for :ref:`li_pubsub_delete`, the
only different is that ``-n NODE, --node NODE`` defaults to tickets namespace.

example
-------

Delete item with id ``456`` from tickets on PubSub service ``pubsub.example.org``::

  $ li pubsub delete -s pubsub.example.org -i 456

import
======

Import lists from an external source. This works in the same way as
:ref:`libervia-cli_blog_import`: you need to specify an importer and a data location. If you let
both positional argument empty, you'll get list of importers, if you specify importer but
not data location, you'll get a description on how the importer works.

If you want to see a progress bar for the import, use the ``-P, --progress`` option, this
is recommended for most imports.

Some importers may have specific option (check description for details), you can specify
them with ``o NAME VALUE, --option NAME VALUE``

When you import a list, the list will be created according to the schema of the PubSub
node. By default, the metadata of the original list will be put to the one of the same
name in the dest PubSub item. But of course the schema of your destination PubSub node may
differ from the original metadata. In this case, you can use ``-m IMPORTED_FIELD
DEST_FIELD, --map IMPORTED_FIELD DEST_FIELD`` to specify how the mapping mus be done
(``IMPORTED_FIELD is the name of the field in the original list, while ``DEST_FIELD`` if
the name of the field in your node schema).


examples
--------

Get list of list importers::

  $ li list import

Get description of list importer for Bugzilla::

  $ li list import bugzilla

Import lists from a Bugzilla XML export file at ``~/bugzilla_export.xml`` to the
``pubsub.example.org`` PubSub service. We use default lists node and want a progression
bar::

  $ li list import -P -s pubsub.example.org ~/bugzilla_export.xml

Same import, but this time we want to map the field ``assigned_to_name`` from Bugzilla to
the field ``assigned_to`` in our schema::

  $ li list import -P -s pubsub.example.org -m assigned_to_name assigned_to ~/bugzilla_export.xml
