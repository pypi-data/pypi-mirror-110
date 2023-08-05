.. _libervia-cli_pubsub:

=========================
pubsub: PubSub management
=========================

PubSub commands are low level command to handle a PubSub Service.
They are using the generic pubsub arguments

For most of those commands, :ref:`pubsub_common` commands are used to specify the
destination item.

set
===

Publish a pubsub item.

``stdin`` is used to get the raw XML of the payload of the item to publish.

``-f KEY VALUE, --field KEY VALUE`` can be used to specify publish options, i.e. option
which must be set if the node already exists, or used if the node is to be created, see
`XEP-0060 §7.1.5`_ for details.

In the same way as for :ref:`libervia-cli_pubsub_node_create`, ``-F, --full-prefix`` can be used if
you need to specify the full option name.

.. _XEP-0060 §7.1.5: https://xmpp.org/extensions/xep-0060.html#publisher-publish-options

example
-------

Create an item with a custom note XML::

  $ echo '<note xmlns="http://example.net/mynotes">this is a note</note>' | li pubsub set -n "notes"

get
===

Retrieve items from specified node. Default output is prettified and highlighted XML.

example
-------

Retrieve the last 5 notes from our custom notes node::

  $ li pubsub get -n notes -m 5

.. _li_pubsub_delete:

delete
======

Delete an item from a node. If ``-N, --notify`` is specified, subscribers will be notified
of the item retraction.

By default a confirmation is requested before deletion is requested to the PubSub service,
but you can override this behaviour by using ``-f, --force`` option.

example
-------

Delete item with id ``123456`` from a node::

  $ li pubsub delete -n test_node -i 123456

edit
====

Edit the raw XML of an item payload using your local editor (the one set in ``$EDITOR``).

If you don't change anything or publish an empty blog post, the edition will be cancelled.

:ref:`draft_common` commands can be used.

example
-------

Edit the last note in our custom node::

  $ li pubsub edit -n notes -L

.. _li-pubsub_rename:

rename
======

Move a item to a new ID. As there is currently no "rename" or "move" operation in XMPP
PubSub, this is done by republishing the item with the new ID, then deleting the old item
if the publication succeed.

This is notably useful when user friendly URL based on ID are used, and one need to fix a
typo or something else.

example
-------

Rename a PubSub item with ID ``123`` to ``456``::

  $ li pubsub rename -n some_node -i 123 456

subscribe
=========

Subscribe to a node.

Subscription is used to get notifications from the node in case of new/updated item or
deletion.

example
-------

Subscribe to an information blog::

  $ li pubsub subscribe -n informations -s pubsub.example.net

unsubscribe
===========

Unsubscribe from a node.

example
-------

Unsubscribe from an information blog::

  $ li pubsub unsubscribe -n informations -s pubsub.example.net

subscriptions
=============

Retrieve subscriptions for all nodes on a service.

``-n NODE, --node NODE`` can be used to request subscriptions for a specific node (e.g. if
it has subscription with multiple subIDs).

example
-------

Retrieve all subscriptions on a pubsub service::

  $ li pubsub subscriptions -s pubsub@example.net

affiliations
=============

Retrieve affiliations for all nodes at a service.

``-n NODE, --node NODE`` can be used to request affiliation for a specific node.

examples
--------

Retrieve all affiliations at a pubsub service::

  $ li pubsub affiliations -s pubsub@example.net

Retrieve affiliation for the ``notes`` node::

  $ li pubsub affiliations -s pubsub@example.net -n notes

search
======

Search items corresponding to one or more filter(s).

``search`` will check all items (or some of them according to options used) from one or
several nodes (several nodes can be checked if recursion is used, see below). For each
item the given filters will be checked, and all corresponding items will be returned.

This is a resource intensive method (both for server and client), use with caution, and
use MAM to do searching when suitable.

filters
-------

To do a search you one or more filters. Filters are checked in the order in which they are
specified. You can use 4 kinds of filters:

``-t TEXT, --text TEXT``
  do a full-text search. If *TEXT* is appearing anywhere in the item (including in XML
  tags or arguments), the item is selected

``-r EXPRESSION, --regex EXPRESSION``
  do a regular expression search. `Python standard re module`_ is used internally, so you
  can use its syntax.

``-x XPATH, --xpath XPATH``
  use an `XPath version 1.0`_ expression to filter the query. You can have a look at
  `Wikipedia XPath page`_ for a user friendly introduction.

``-P PYTHON_CODE, --python PYTHON_CODE``
  use a Python expression to do a test. The expression must return a boolean (``True`` to
  keep item, ``False`` otherwise). From within the Python expression 3 variables are
  defined: ``item`` which contain the raw item as a string, and ``item_xml`` which is the
  parsed XML as an lxml ``etree.Element`` and ``etree`` which is the ``lxml.etree`` module.

.. _Python standard re module: https://docs.python.org/3.7/library/re.html
.. _XPath version 1.0: https://www.w3.org/TR/1999/REC-xpath-19991116/
.. _Wikipedia XPath page: https://en.wikipedia.org/wiki/XPath

filter modifiers
----------------

Before each filter you can specify one or more filter modifiers. A modifier will change
filter behaviour, it's a flag which can be used either without argument (then it will
activate the flag), or with an explicit boolean value (i.e. ``true`` or ``false``).

The available filters are:

``-C [BOOLEAN], --ignore-case [BOOLEAN]``
  (don't) ignore case. Filters are normally case sensitive, this modifier change this
  behaviour.

``-I [BOOLEAN], --invert [BOOLEAN]``
  (don't) invert effect of following filters. This is applying a logical ``NOT`` to the
  filter. This means that instead of keeping item matching the filter, it will keep the
  items which are **not** matching the filter.

``-A [BOOLEAN], --dot-all [BOOLEAN]``
  (don't) use `DOTALL`_ option for regex. This filter only makes sense before a
  ``--regex`` expression.

``-k [BOOLEAN], --only-matching [BOOLEAN]``
  (don't) keep only the matching part of the item. Normally the whole item is returned,
  with this flag, only the part matching the filters are kept.

.. _DOTALL: https://docs.python.org/3.7/library/re.html#re.DOTALL

actions
-------

Once filters are set, you may indicate what do to with the found items. By default they
are printed, but you can also use an other li command, or even an external tool.

The following actions are available:

``print`` (default)
  pretty print the found items.

``exec``
  use the given li command on each found item. Everything after the ``exec`` is used to
  indicate the command and arguments to use (you must not specify ``li``, use the command
  directly). The service, node and item will be set to match the found item.

``external``
  pipe the raw XML of each item to the given command. Everything after the ``external``
  action is used to indicate the command and arguments to use.

recursive search
----------------

By default, only items in the given node will be filtered, but if you specify a recursion
depth > 0 (using ``-D MAX_DEPTH, --max-depth MAX_DEPTH``), every node linked in item will
be checked too, then node linked in linked item and so on until depth level is reached.

For instance, if you want to find all comments of a blog node containing an http(s) link,
you can do that::

  $ li pubsub search -n urn:xmpp:microblog:0 -s user@example.net -D 1 -r 'https?://'

examples
--------

Finding all items containing the text "something interesting" in personal blog::

  $ li pubsub search -n urn:xmpp:microblog:0 -M -1 -t "something interesting"

Find which blog items in the last 20 have a body with less than 200 characters (note that
body can be either ``<title>`` or ``<content>``, see `XEP-0277`_ for details). Here we use
a python expression on the text of the body to count the number of characters::

  $ li pubsub search -n urn:xmpp:microblog:0 -M 20 --python "len((item_xml.find('.//{http://www.w3.org/2005/Atom}content[@type=\"text\"]') or item_xml.find('.//{http://www.w3.org/2005/Atom}title[@type=\"text\"]')).text) < 200"

Find items published by ``toto@example.net`` among last 30 on a blog node, and use
``pubsub blog`` command to retrieve id and title. We use ``-N`` to specify the ``pubsub``
namespace which is used in the XPath expression, then we use ``exec`` to run ``blog get -k
title -k id`` on found items::

  $ li pubsub search -n some_blog_node -s pubsub.example.net -M 30 -N pubsub http://jabber.org/protocol/pubsub -x '/pubsub:item[starts-with(@publisher, "toto@example.net")]' exec blog get -k title -k id

Find items which have **NOT** a title among last 30 items in our personal blog. As
explained in `XEP-0277`_ Atom's ``<title>`` is always used (even if there is only a body
and no title), so we actually look for items without ``<content>``. We do that with an
XPath looking for this ``atom:content`` element, then we use the ``-I [BOOLEAN], --invert
[BOOLEAN]`` to filter out elements which match.::

  $ li pubsub search -n urn:xmpp:microblog:0 -M 30 -I -x //atom:content -N atom http://www.w3.org/2005/Atom

Display authors names from last 10 items and their comments, using the ``-k [BOOLEAN],
--only-matching [BOOLEAN]`` modifier to only display the data we need. We use ``-D 1`` to
do a recursive search of level 1, which will also look into comments nodes (using last 10
items there too)::

  $ li pubsub search -n urn:xmpp:microblog:0 -M 10 --only-matching -x //atom:author/atom:name -N atom http://www.w3.org/2005/Atom -D 1

.. _XEP-0277: https://xmpp.org/extensions/xep-0277.html

transform
=========

Modify items using an external command.

``transform`` will retrieve requested items, and will send each of them to the standard
input (stdin) of the specified command. The output of the command will be used, it can be
3 things:

- a raw XML of the modified item, in which case the item will be republished
- the string ``SKIP``, in which case the item will be ignored
- the string ``DELETE``, in which case the item will be retracted

By default a dry run is done, which means that no item is modified or deleted. To actually
do the transformation, you have to use ``--apply`` argument.

If you have to modify the ``publisher`` of an item, you need specific privileges. The
``--admin`` allows you do to that, but it must be supported by your PubSub service
(currently only ``Libervia PubSub`` supports this non standard feature).

To modify all items of a node, use the ``-A, --all`` option. This will use `RSM`_
repetitively until all items are treated. Of course that means that your PubSub service
must support RSM. The items being republished, they will reappear on top of your node,
that's why it is recommended to use ``--order-by creation`` option when supported by the
service, to keep consistent order and avoid transforming the same items several times.

If the command you're using exit with a non zero code, the process will stop. Use ``-I,
--ignore_errors`` if you want to continue transformation even if an non zero code is
returned.

.. _RSM: https://xmpp.org/extensions/xep-0059.html

example
-------

Imagine that you want to replace all occurrences of "sàt" by "Libervia" in your personal blog. You first create a Python script like this:

.. sourcecode:: python

   #!/usr/bin/env python3

   import sys
   item_raw = sys.stdin.read()
   if not "sàt" in item_raw:
       print("SKIP")
   else:
       print(item_raw.replace("sàt", "Libervia"))

And save it a some location, e.g. ``~/expand_sat.py`` (don't forget to make is executable
with ``chmod +x ~/expand_sat.py``).

To be sure it's safe, you can first do a dry-run and check the result::

  $ li pubsub transform -n urn:xmpp:microblog:0 -A -o creation ~/expand_sat.py

Once you have checked that you have the expected behaviour, you can apply the
transformations::

  $ li pubsub transform -n urn:xmpp:microblog:0 -A -o creation --apply ~/expand_sat.py

And that's it. You can use the same technique for more complex transformations, including
modifying the XML (with Python, you can easily do that with standard
``xml.etree.ElementTree`` module or with ``lxml.etree``).

uri
===

Build an XMPP URI linking to a PubSub node or item.

example
-------

Build a link to personal blog::

  $ li pubsub uri -n urn:xmpp:microblog:0

node
====

Subcommands for node management. Please check :ref:`libervia-cli_pubsub_node`.

hook
====

Subcommands for hooks management. Please check :ref:`libervia-cli_pubsub_hook`.
