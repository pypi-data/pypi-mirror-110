================
common arguments
================

Some arguments are used in many commands. This page describe them.

.. _libervia-cli_common_profile:

profile
=======

profile arguments are really common, they allow you to select your profile.
If you don't select any, the default profile is used, which is the first
profile created or the one you have explicitly set. You can check which profile
is used by default with ``li profile default``.

The common arguments for profile are:

``-p PROFILE, --profile PROFILE``
  to select the name of your profile. It can be a profile key like ``@DEFAULT@``

``-c, --connect``
  connect the profile to the XMPP server before doing anything else. If your
  profile is already connected, nothing happen. This is specially useful in scripts.

``--start-session``
  starts a session without connecting, this can be needed if you can't connect but
  you need to access your session e.g. to change parameters.
  This is advanced used and is not need in most common cases.

``--pwd PASSWORD``
  the password of your profile, needed if the session is not started yet.

.. note::

   using the ``--pwd`` option is not secure if you are not the only user of your machine:
   the password will appear **IN CLEAR** in the list of launched processes, or in the
   history of your shell. If the profile password is needed and not specified, it will be
   prompted (with echo disabled). If you are on a shared machine or if anybody can access
   your shell history at some point, you should either connect first your profile with an
   other frontend (Primitivus for instance), or avoid the ``--pwd`` option and use the
   prompt instead.

.. _pubsub_common:

pubsub
======

pubsub arguments are used in many commands, they allow you to select a service, node and
items. Depending on the command, you may only not be able to select an item, or you may
select one or multiple items.

The common arguments for pubsub are:

``-u PUBSUB_URL, --pubsub-url PUBSUB_URL``
  retrieve pubsub information from an URL. You can use either and ``xmpp:`` scheme or an
  ``https:`` (or ``http:``) scheme. In the later case, the HTML page will be downloaded to
  retrieve the location of the XMPP node/item, if available.
  Note that you can override parts of the location in the URL if you specify service, node
  or item.

  e.g.::

    $ li blog get -u https://www.goffi.org

``-s SERVICE, --service``
  used to specifiy the JID of the pubsub service

``-n NODE, --node NODE``
  used to specifiy the pubsub node

``-i ITEM, --item ITEM``
  for commands where an item can be specified, you do it with this option. In some
  commands, multiple items can be specified, in this case just use this arguments several
  times.

``-L, --last-item``
  when an item id is needed, you can use this option to retrieve the last published item.
  e.g.::

    $ li blog edit --last-item

``-M, --max-items``
  use to specify a maxium number of items to retrieve, when it makes sense.
  Note that this is using the pubsub max (i.e. defined in
  `XEP-0060 <https://xmpp.org/extensions/xep-0060.html>`_). Modern pubsub services should
  implement `Result Set Management <https://xmpp.org/extensions/xep-0059.html>`_ (RSM) and in
  this case the ``-m, --max`` argument should be prefered. See below for RSM common
  arguments.

result set management
=====================

Result Set Management (RSM) common arguments are used to navigate into pages of results
when lot of elements may be expected. Given a result with a large number of arguments, a
*page* is set of elements which correspond to an *index* (a page number). For instance if
you have 123 elements, you can ask them 10 by 10, and *index 1* match elements from 11 to
20 included.


``-a ITEM_ID, --after ITEM_ID``
  find page after this item. You usually use the last item id of the latest page you got.

``-b ITEM_ID, --before ITEM_ID``
  find page before this item. This this usually used when you check items backwards

``--index RSM_INDEX``
  index of the page to retrieve. Note that first page has index **0**.

``-m RSM_MAX, --max RSM_MAX``
  used to specify a maxium number of items to retrieve per page. Note that the actual
  maximum number of items per page used may be lower if the service used consider that
  your request is too big.

message archive management
==========================

Message Archive Management (MAM) argument is used by some commands (related to instant message or
pubsub) to filter results.

There is currently only one argument in this group:

``-f FILTER_NAME VALUE, --filter FILTER_NAME VALUE``
  specify a MAM filter to use. Depending on the service supporting MAM, some filters can
  be used to do things like full text search. The available filters depend on the service
  you use, please check documentation of your service.

order-by
========

Order-By argument specify how the returned elements are sorted.

There is currently only one argument in this group:

``-o {creation,modification}, --order-by {creation,modification}``
  specify how result is sorted. with ``creation``, first created element is returned
  first. There is no notion of *creation* of *modification* in original
  `pubsub XEP <https://xmpp.org/extensions/xep-0060.html>`_, as publishing an item with an
  existing id will overwrite the older one, creating a new item. With this option, we use
  the terms defined in `XEP-0413 <https://xmpp.org/extensions/xep-0413.html>`_, and
  *creation* time is the time when the first item has been published, before being
  overwritten.

  In the case of ``modification``, if an item is overwritten, it reappears on top, this is
  the default pubsub sorting order.

progress
========

This single option may be used when a long operation is happening, like a file transfer.

``-P, --progress``
  Show progress bar.

verbose
=======

``--verbose, -v``
  Add a verbosity level (can be used multiple times). Use to have more concise output by
  default when it makes sense.

.. _draft_common:

draft
=====

Common arguments used when an edition is potentially long to do, and a file may be kept
until publication.


``-D, --current``
  Used when you have started to edit something (e.g. a blog post), which is not yet
  published, and you want to continue your work.

  e.g.::

    $ li blog edit -D

``-F DRAFT_PATH, --draft-path DRAFT_PATH``
  Used when you have started to edit something and want to continue your work from this
  file. In other words, it's similar to ``-D, --current`` except that you specify the file
  to use instead of using the last available draft.

.. _libervia-cli_output:

output
======

Output is used when you want to get the result of the command in a specific way. It may be
used, for instance, to retrieve the result formatted in JSON so the data can be easily
manipulated by a script, or if you want only a specific element of the result.

``-O {…}, --output {…}``
  specifiy the output to use. Available options depends of the command you are using,
  check ``li [your command] --help`` to know them.

  e.g.::

    $ li blog get -O json

``--output-option OUTPUT_OPTS, --oo OUTPUT_OPTS``
  depending of the output selected, you may have options to customise the output.
  For instance, if you use the ``template`` output, you may use an option to display the
  result in a browser.

  e.g.::

    $ li blog

  Some options expect parameters, in this case they can be specified using ``=``.

  e.g. specifiying a template to use::

    $ li blog get -O template --oo browser --oo template=/tmp/my_template.html
