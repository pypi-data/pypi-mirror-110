.. _libervia-cli_event_invitee:

========================================
event/invitee: event invitees management
========================================

``invitee`` groups commands to invite somebody to an event, get or set data about an invitee, and list all invitees. You can send an invitation by e-mail to people without XMPP account.

.. _libervia-cli_event_invitee_get:

get
===

Retrieve the RSVP status of one guest. Note that you must the invitees node and not the
event node. To retrieve invitees node, use :ref:`libervia-cli_event_get` with the event node.

You may specify the guest bare jid using ``-j JID, --jid JID`` (by default your own bare
jid will be used).

If no response is known yet, no data is returned.

example
-------

Get RSVP of Louise::

  $ li event invitee get -u "xmpp:pierre@example.net?;node=generic%2F876a2b99-1c90-41fa-b823-c4a467140770" -j louise@example.org


.. _libervia-cli_event_invitee_set:

set
===

Set your own RSVP data. Note that as for libervia-cli_event_invitee_get_ you must use
invitees node and not the event node.

Use ``-f KEY VALUE, --field KEY VALUE`` to specify the data to set. ``KEY`` can be one of
``attend`` (where calue can be ``yes``, ``no``, or ``maybe``) and ``guests`` where value
must be an integer.

example
-------

Indicate that you'll come to an event with 3 guests::

  $ li event invitee set -u "xmpp:pierre@example.net?;node=generic%2F876a2b99-1c90-41fa-b823-c4a467140770" -f attend yes -f guests 3

list
====

Get and format the RSVP of your invitees. Note that as for libervia-cli_event_invitee_get_ and
libervia-cli_event_invitee_set_ you must use invitees node and not the event node.

By default, only people who have answered are shown. You may use ``-m, --missing`` to show
other people which were invited, but have not answered yet. When using this option, you
can also use ``-R, --no-rsvp`` to only show people which have not answered yet.

You'll also have a small summary indicating how many people who can expect at your event.

example
-------

Get the full list of invitees (including those who didn't answered yet) with the RSVP formatted::

  $ li event invitee list -u "xmpp:pierre@example.net?;node=generic%2F876a2b99-1c90-41fa-b823-c4a467140770" -m

invite
------

Invite somebody to an event. The invitation is done by e-mail, a guest account will be
created. Contrary to other ``invitee`` commands, in this one you'll use the event node
directly.

This command is really similar to :ref:`libervia-cli_invitation_create`

E-mail address is specified using ``-e EMAIL, --email EMAIL`` and you'll need to give an
URL template (using ``-U URL_TEMPLATE, --url-template URL_TEMPLATE``)leading to your
website page handling the invitation (for Libervia default invitation page is
``<your_server>/g/<uuid>``). You can use ``{uuid}`` as a placeholder which will be
replaced by event's id.

You'll probably want to specify the name of the invitee, using ``-N NAME, --name NAME``
and your own name (as the host inviting), using ``-H HOST_NAME, --host-name HOST_NAME``.
The language spoken by your guest can be specified using ``-l LANG, --lang LANG``, it is
mainly useful if you have many invitee speaking different languages.

example
-------

Pierre is inviting Louise (whose e-mail address is ``louise_email@example.net``) to an
event he's organising::

  $ li event invitee invite -e louise_email@example.et -N "Louise" -H "Pierre" -l fr -U "https://www.example.org/g/{uuid}" -u "xmpp:pierre@example.org?;node=generic%2F61400ea7-a2a2-4ce0-9b68-3735b602f671"
