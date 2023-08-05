.. highlight:: sh

================================
message: chat message management
================================

Message commands let you send chat messages or manage your server message archives.

.. _libervia-cli_message_send:

send
====

Send a message to a contact or a chat room.
``stdin`` is used as message source.
You can encrypt your message using ``--encrypt [ALGORITHM]`` argument, this will create an encrypted session and replace existing one if needed.
You can manage your encrypted session using ``encryption`` command.

examples
--------

Send a message to a contact::

  $ echo 'Salut à Toi!' | li message send louise@example.net

Send a message encrypted with OMEMO::

  $ echo 'pssst, this message is encrypted' | li message send -e omemo louise@example.net

.. note::

  Fingerprints of your destinee must have been accepted before using OMEMO, else message can't be encrypted

Send a ``normal`` message marked as French with a subject::

  $ echo 'Bonjour, je vous écris avec « Libervia »' | li message send -l fr -t normal -S 'Ceci est un message de test'

mam
===

Query archives using MAM.
This command allows you to check message archive kept on the server (i.e. not the local copy).
You usually want to specify a starting point, and a number of message to retrieve. If too many messages
are available, you'll have to use RSM commands to navigate through the results.

examples
--------

Retrieve messages from last 2 days::

  $ li message mam -S "2 days ago"

Retrieve messages from last 5 hours on Libervia official chat room::

  $ li message mam -S "5 hours ago" -s sat@chat.jabberfr.org

Retrieve 2 first messages of 2019 on Libervia official chat room::

  $ li message mam -S 2019-01-01 -s sat@chat.jabberfr.org -m 2
