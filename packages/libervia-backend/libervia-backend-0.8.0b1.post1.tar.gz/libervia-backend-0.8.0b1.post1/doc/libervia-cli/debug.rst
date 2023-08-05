=====================================================
debug: tools to help debugging/monitoring Libervia
=====================================================

``debug`` groups commands to monitor or manipulate Libervia and XMPP stream.

.. _libervia-cli_debug_bridge_method:

bridge method
=============

Call a method of the bridge. You have to provide the name of the method and the arguments
as positional arguments. Arguments are evaluated as Python code (using ``eval``), so you
need to properly escape them (for your shell **and** Python). You can either split your
Python arguments as many shell arguments, or put them in a single shell argument.

You profile is automatically set if the method requires it (using the value of ``-p
PROFILE, --profile PROFILE``), so you must not specify it as an extra argument.

You can refer to `Bridge API documentation`_ to get core methods signatures

.. _Bridge API documentation: https://wiki.goffi.org/wiki/Bridge_API


examples
--------

Send a message using a single shell arguments for all Python arguments. We
use first the method name (``messageSend``), then the required arguments (see `Bridge
API documentation`_ for details), without the profile as it is automatically set. We
specify them as Python in one shell argument, so we use single quote (``\```)first for
s hell string, and inside it we use double quote (``"``) for Python strings::

  $ li debug bridge method messageSend '"louise@example.org", {"": "test message"}, {}, "auto", {}'

.. note::

  This is for debugging only, if you want to send message with li, use :ref:`libervia-cli_message_send`.

Get version string of Libervia::

  $ li debug bridge method getVersion


bridge signal
=============

Send a fake signal. This is specially useful to test behaviour of a frontend when a
specific event happens. To use is you just need to specify the name of the signal and the
arguments to use (using Python eval in the same way as for libervia-cli_debug_bridge_method_).

example
-------

Send a note with ``info`` level and hand written XMLUI. Here me use a shell variable to
store the level, so we can easily change it if we want to use an other level for tests.
Note the use of quotes (to escape both for shell and Python)::

  $ LEVEL='info'; li debug bridge signal -c actionNew '{"xmlui": '"'"'<?xml version="1.0" ?><sat_xmlui title="test title" type="dialog"><dialog level="'$LEVEL'" type="note"><message>test message\non\nseveral\nlines</message></dialog></sat_xmlui>'"'"'}' '""' -1


monitor
=======

Show raw XML stream. By default, output is pretty formatted/highlighted and you get all
streams in both direction. You can filter the direction using ``-d {in,out,both},
--direction {in,out,both}``.

For this to work, you need to set the option ``Activate XML log`` in the ``Debug`` section
of your parameters.

Verbosity is used, to print details on the direction of a stanza, use ``--verbose, -v``

example
-------

Monitor raw XML stream::

  $ li debug monitor -v

theme
=====

Show the colour constants in their respective colour, according to background (``light``
or ``dark``). If backround option is not set in ``libervia.conf``, it will be autodetected, and
colour theme will be modified accordingly.

example
-------

Show colours with the set background::

  $ li debug theme
