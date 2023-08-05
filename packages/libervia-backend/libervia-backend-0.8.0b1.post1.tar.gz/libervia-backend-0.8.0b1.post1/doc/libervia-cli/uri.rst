================================
uri: XMPP URI parsing/generation
================================

URI commands are helper to easily parse/build XMPP URIs.

parse
=====

Parse an XMPP URI, and print different parts.

When possible, the ``type`` of URI is shown (e.g. ``pubsub``) and the ``sub_type`` (e.g.
``microblog``).

The ``path`` is always displayed (see `RFC 5122 Path section`_ for details).

If suitable, you'll also get data like ``node`` (for a PubSub URI).

.. _RFC 5122 Path section: https://tools.ietf.org/html/rfc5122#section-2.4

examples
--------

Parse a blog URI::

  $ li uri parse "xmpp:somebody@example.org?;node=urn%3Axmpp%3Amicroblog%3A0"

build
======

Build an XMPP URI according to arguments. 2 positional arguments are expected: ``type``
and ``path``. For now, only ``pubsub`` type is supported.

examples
--------

Build XMPP URI for a blog::

  $ li uri build pubsub somebody@example.org -f node urn:xmpp:microblog:0
