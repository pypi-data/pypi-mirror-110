========================
event: events management
========================

Event commands allows you to create/modify or get data about an event, and to manage your
invitees.

list
====

List events available on a service

example
-------

Retrieve events of profile::

  $ li event list

.. _libervia-cli_event_get:

get
===

Get metadata about a specific event.

example
-------

Retrieve an event metadata::

  $ li event get  -n org.salut-a-toi.event:0__BsyCsXpcrRh44CQhSVTUMi -i 'org.salut-a-toi.event:0'

.. _libervia-cli_event_create:

create
======

Create a new event. You can specify the date of the event with ``-d DATE, --date DATE``,
and an id with ``-i ID, --id ID`` (default id is used if omitted).

Configuration options are specified using ``-f KEY VALUE, --field KEY VALUE`` where key
can be a custom data or one of:

name
  name of the event
description
  details of the event
image
  URL of the main picture of the event
background-image
  URL of image to use as background
register
  a boolean value, set to ``true`` if you want to register the event in your local list

example
-------

Create an event about to celebrate New Year::

  $ li event create -d 2019-12-31 -f name "New Year's Eve" -f description "Party to celebrate new year" -f register true -f image https://example.net/some_image.jpg


modify
======

This command in the same way as libervia-cli_event_create_ but modify an existing event. You need to
specify the node of the event to modify using ``-n NODE, --node NODE``.

example
-------

Add a background image to the New Year event created above::

  $ li event modify -n org.salut-a-toi.event:0__d8QQLJvbcpDXxK66UBXKfT -f background-image https://example.net/some_background_image.jpg


invitee
=======

Subcommands to handle guests. Please check :ref:`libervia-cli_event_invitee`.
