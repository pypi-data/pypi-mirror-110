========================================
encryption: encryption sessions handling
========================================

Libervia being an XMPP client does encryption by default between client and server. In
addition, Libervia is also capable of doing end-to-end (e2e) encryption, meaning that the
payload of messages are encrypted to be hidden from the servers (and their
administrators).  The ``encryption`` commands are here to handle those e2e encryption
sessions and algorithms.

.. note::

   For the moment, only one 2 one chat messages can be e2e encrypted

algorithms
==========

Display e2e encryption algorithms available in this instance of Libervia.

example
-------

Show available e2e algorithms::

  $ li encryption algorithms

get
===

Display which encryption session is currently active with the given entity.

The only required argument is the JID of the entity.

If not e2e encryption session exist, a message will be displayed and li will exit with a
non zero code: this means that the messages are in clear in the XMPP servers, but normal
XMPP encryption is not affected (message should still be encrypted between client and
server and between servers).

If an e2e encryption session exist, you'll see the algorithm name and its namespace. In
case of e2e encryption which only works from device to device (e.g. it's the case with
``OTR`` which doesn't support multiple devices), you'll also see the resources of the
devices where the encryption is active in ``directed_devices``

example
-------

Check if session is encrypted with Louise::

  $ li encryption get louise@example.org

start
=====

Start e2e session with an entity.

You need to specify the JID of the entity you want to start a session with as a positional
argument.

By default, Libervia will select itself the algorithm to use among those available, but you can
specify one using either its name with ``-n NAME, --name NAME`` or its namespace using
``-N NAMESPACE, --namespace``. ``NAME`` is the short name of the algorithm, e.g. ``omemo``
while the namespace is the longer (e.g. ``urn:xmpp:otr:0``).

If an encryption session is started but one with an other algorithm was already there, the
original session will be stopped and replaced by one with the new requested algorithm. You
can change this behaviour by using ``--encrypt-noreplace``: in this case the command will
fail in case of conflict (e2e encryption is requested with a new algorithm while an e2e
encryption session was already started with an other algorithm), and return a non-zero
code. If an e2e encryption session was already started with the requested algorithm, the
command will succeed in all cases and nothing will be changed.

examples
--------

Start e2e encryption with Pierre, using the algorithm selected by Libervia::

  $ li encryption start louise@example.net

Start an OMEMO session with Louise::

  $ li encryption start -n omemo louise@example.org

stop
====

Terminate an e2e session with given entity. The entity must be specified as positional
argument.

After this command is run, the messages with specified entity will not be e2e encrypted
anymore (but this won't affect encryption between Libervia and XMPP server and between XMPP
servers).

example
-------

Stop the e2e encryption session with Pierre::

  $ li encryption stop pierre@example.net

trust ui
========

Run the user interface to handle trust with given entity and given algorithm. The user
interface depends on the algorithm used, but it generally shows you the fingerprints
associated with your contact or contact devices, and asks you if you trust them or not.

The only mandatory argument is the jid of your contact.

By default the currently active encryption session algorithm is used, but you may manage
trust for another algorithm by using ``-n NAME, --name NAME`` or ``-N NAMESPACE,
--namespace NAMESPACE``.

.. note::

   Trusting a contact or a device means that you certify that this contact or device is
   the one you want to talk too. You should not trust a device if you have not verified by
   an external channel (i.e. not XMPP) the fingerprint. The best way is to verify the
   fingerprint physically if possible (i.e. in front of your contact, not with computer
   networks in the middle).

example
-------

Manage ``OMEMO`` trust with Louise devices::

  $ li encryption trust ui -n omemo louise@example.org
