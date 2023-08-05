==============================================
invitation: invite people without XMPP account
==============================================

Invitations allows you to invite people without XMPP account, so they can participate e.g.
to a discussion by using a specially generated link. This is a Libervia specific
feature and those commands are rather low lever.

.. _libervia-cli_invitation_create:

create
======

Invite somebody to participate. This will create a guest account and a link with an
identifier to access this account, and send an invitation to the given email.

The email is specified using ``-e EMAIL, --email EMAIL``, which can be used multiple times
to send the invitation to more than one address.

You'll usually want to specify the name of the person you're inviting, using ``-n NAME,
--name NAME``, it may later be used in email sent or in the web page where your guest will
land.

``-N HOST_NAME, --host-name HOST_NAME`` is used to specify the name of yourself (i.e. the
person which is inviting), it may be used in invitation message.

You'll most of time have to specify the URL template using ``-u URL, --url URL``. This
will be used in the invitation email to construct the URL where your invitee will click.
You may use the string ``{{uuid}}`` in this template which will be replaced by the id
associated to the invitation. With Libervia, default invitation page is
``<your_server>/g/<uuid>``.

The language of your guest can be specified using ``-l LANG, --lang LANG``, this is
notably useful if you have multilingual blog posts (e.g. for an event where people
speaking different languages are invited).

The ``-x KEY VALUE, --extra KEY VALUE`` is used for extra data which depend on what you
are inviting your guests for.


example
-------

Invite Louise, which is speaking French, to an event. The invitation is sent to her email
address ``louise_email@example.net``, is sent by Piotr, and must link to the Libervia
instance at ``https://www.example.org/g/<id>``. We use here the ``event_uri`` extra key::

  $ li invitation create -n Louise -N Pierre -e louise_email@example.net -l fr -u "https://www.example.org/g/{uuid}" -x event_uri xmpp:pierre@example.org?;node=MnXe4ic2X8RUz6JAJuw4f9;item=org.salut-a-toi.event%3A0


get
===

Get metadata for one specific invitation. You only have to specify the invitation id, and
you may use the option ``-j, --with-jid`` to also get the jid used for the invitation
(this will start the session of the invitee).

example
-------

Get invitation data for invitation with id ``okFec4gDz75My7iQAVTmsc``::

  $ li invitation get okFec4gDz75My7iQAVTmsc -j


modify
======

This work the same way as  libervia-cli_invitation_create_, you only have to specify the ``id`` of the
invitation.

If you use the ``--replace`` argument, all the invitation data will be replaced by the
ones you're specifying.

example
-------

Change the language of the invitee for the invitation ``okFec4gDz75My7iQAVTmsc`` for
Slovak::

  $ li invitation modify -l sk okFec4gDz75My7iQAVTmsc


delete
======

Delete XMPP account created for an invitation and invitation data

example
-------

Delete invitation with id ``okFec4gDz75My7iQAVTmsc``::

  $ li invitation delete okFec4gDz75My7iQAVTmsc


list
====

List registered invitations. You may filter by the profile who made the invitation using
``-p PROFILE, --profile PROFILE``.
The invitations are shown by default using id as main data, and metadata below.

example
-------

List invitations::

  $ li invitation list
