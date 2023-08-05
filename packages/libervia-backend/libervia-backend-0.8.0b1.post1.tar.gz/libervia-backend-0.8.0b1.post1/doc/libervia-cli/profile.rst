==================================
profile: Libervia profile handling
==================================

Profiles are the names associated with accounts in Libervia, for more informations you can
check :ref:`glossary`. The `profile` commands help you create/delete/modify and manage
profiles.


connect
=======

Unsurprisingly this command connects your profile, i.e. log-in your XMPP account. This
command uses :ref:`libervia-cli_common_profile` common commands, so you can use either ``-c,
--connect`` to connect to XMPP server, or ``--start-session`` if you want to start Libervia
profile session without connecting to XMPP server (for instance if you want to modify
parameters without connecting to XMPP server).

Note that :ref:`libervia-cli_common_profile` common commands are available in commands needing a
connected profile, ``li profile connect`` is interesting if you only want to connect your
profile/start a session.

example
-------

Connect the default profile::

  $ li profile connect -c


disconnect
==========

Disconnect your profile from XMPP server. There is no option beside the
:ref:`libervia-cli_common_profile` common options.

example
-------

Disconnect the profile ``pierre``::

  $ li profile disconnect -p pierre


create
======

Create a new Libervia profile. The only mandatory argument is the profile name, but you'll
probably want to associate an XMPP jid with ``-j JID, --jid JID`` and a profile password
with ``-p PASSWORD, --password PASSWORD``. By default, profile password will be used for
XMPP password (see note below), but you may specify XMPP password with ``-x PASSWORD,
--xmpp-password PASSWORD``.

Libervia is also capable to manage components, which can be seen as XMPP server independent
plugins. To create a component profile, you'll have to use ``-C COMPONENT, --component
COMPONENT`` where ``COMPONENT`` is the component entry point (check the documentation of
the component that you want to use to get its entry point).

If you want a profile to connect automatically on backend startup (notably useful for
components), you can use the ``-A [{true,false}], --autoconnect [{true,false}]`` argument.

.. note::

   profile password and XMPP password are not the same: the profile password is the
   password of your Libervia profile, while the XMPP password is the one checked by your XMPP
   server. If specify a jid with ``--jid`` and you don't specify an XMPP password, the
   profile password will be used by default.

   The reason to have distinct password is that you may use a different password for
   profile, including an empty one if you want Libervia to connect your profile without
   having to enter a password. Also the XMPP password is encrypted in database using the
   profile password (which is not stored in database, only a hash is kept).


.. note::

   passwords in li are currently specified directly on the command-line and not prompted,
   this is not safe from a security point of view as people can see it on the screen, it
   may stay in your shell history, or visible on process list. Keep that in mind if you're
   in a public environment or on a public machine. This will be improved for Libervia 0.8.

examples
--------

Nestor wants to create a profile for its account on ``example.org``, he specifies a
profile password only, so it will also be used as the XMPP password::

  $ li profile create nestor -j nestor@example.org -p some_password

Create a component profile for the file sharing component (whose entry point is
``file_sharing``). The jid of the service is specified with ``--jid`` (note that we don't
use a node as it is a jid of a component) and the ``--xmpp-password`` is the shared
secret. Here the profile password is kept empty to not have to enter manually the XMPP
password each time we connect the service. We use the ``-A`` option to set
autoconnection::

  $ li profile create file_sharing -j files.example.org -p "" --xmpp-password
  some_shared_secret -C file_sharing -A


default
=======

This command simply prints the default profile (i.e. the profile used when none is
specified with ``-p PROFILE, --profile PROFILE``). The default profile is either the first
one that you've created, or the one you have explicitly set as default.

example
-------

Print default profile::

  $ li profile default


delete
======

Delete a profile and all its associated data. This delete the Libervia profile and associated
data (i.e. local data), but doesn't request the XMPP server to delete anything.

By default a confirmation is requested, use ``-f, --force`` to avoid it (be cautious with
this option).

example
-------

Delete the profile of Pierre::

  $ li profile delete pierre


info
====

Display information on a profile. For now, only the registered jid is shown, and
optionally the XMPP password. To display the XMPP password, use ``--show-password`` but be
careful that nobody can see your screen, as **this password will be shown in clear text**.

example
-------

Show jid and XMPP password for default profile::

  $ li profile info --show-password


list
====

Show all profiles. You can use ``-c, --clients`` to show only client profiles, and ``-C,
--components`` to show only component profiles.

example
-------

Show all profiles::

  $ li profile list


modify
======

Update an existing profile. You can use this command to change profile password (with ``-w
PASSWORD, --password PASSWORD``) or even disable it (with ``--disable-password``, this is
equivalent to using an empty profile password ; be cautious with this option, see the note
below).

With ``-j JID, --jid JID`` and ``-x PASSWORD, --xmpp-password PASSWORD`` you can change
XMPP jid and password.

This command can also be used to select the default password, use the ``-D, --default``
flag for that.

.. note::

   Be cautious with ``--disable-password`` that means that no password will be needed with
   any frontend of Libervia to use this profile, and that XMPP password will be easy to
   retrieve for anybody having an access to the machine where Libervia is installed

examples
--------

Pierre has changed server, he can update his jid and password like this::

  $ li profile modify -p pierre -j pierre@example.org -x new_password

Use ``louise`` as default profile::

  $ li profile modify -p louise -D

Disable profile password for default profile (be cautious, see the note above)::

  $ li profile modify --disable-password
