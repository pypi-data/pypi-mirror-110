================================
account: XMPP account management
================================

``account`` command help you to create or manage the XMPP account of a server, using
In-Band Registration (`XEP-0077`_).

.. _XEP-0077: https://xmpp.org/extensions/xep-0077.html

create
======

Create a XMPP account. You have to specify your jid and password as positional arguments.
By default the registration is done on ``localhost`` with default XMPP Client 2 Server
port (i.e. 5222), but you can specify other host/port using ``-H HOST, --host HOST`` and
``-P PORT, --port PORT``. You may also specify an e-mail address using ``-e EMAIL, --email
EMAIL`` (use of this data depend of the server implementation).

By default, no Libervia profile is created and associated to this new XMPP account, but you can
use ``-p PROFILE, --profile PROFILE`` if you are willing to have one.

example
-------

Create account for the new user Nestor at ``nestor@example.org`` and associate it with the
Libervia profile ``nestor``::

  $ li account create nestor@example.org some_password -p nestor


modify
======

Modify an existing XMPP account password. This will modify the XMPP account linked to the
given profile.

.. note::

   Only the XMPP password on the server is changed, not the one registered in the
   parameter of Libervia. You may have to update the parameter of your profile if the new
   password doesn't correspond to your parameters one (you can do that with li param set
   or with most Libervia frontends in parameters).

example
-------

Change the XMPP password of the XMPP account of the default profile::

  $ li account modify new_password


delete
======

Delete the XMPP account linked to the given profile from the XMPP server. Before using
this command, please be sure to understand well that **THIS WILL REMOVE THE WHOLE XMPP
ACCOUNT AND DATA FROM THE XMPP SERVER**.

By default a confirmation is requested, you can do this without confirmation by using
``-f, --force``, however this is **NOT RECOMMENDED**, be sure to understand what you're
doing if you use this option (and be sure to spell correctly the profile, if you forget
the ``-p PROFILE, --profile`` argument for instance, this would delete entirely the
default profile).

.. note::

   Be extra careful with this command, as it will remove the whole account from the
   server, and the associated data.

example
-------

Delete the XMPP account of Pierre, which is not on the local server anymore::

  $ li account delete -p pierre
