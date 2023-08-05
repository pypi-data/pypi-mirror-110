.. _libervia-cli_file_share:

==================================
file/share: advanced files sharing
==================================

``share`` groups commands for listing file available on a device/service, sharing a file
or directory, and inviting people to retrieve files.

.. _libervia-cli_file_share_list:

list
====

List files available on a device or sharing service. You mainly have to specify the jid of
the device/service where the files are stored (if jid is omitted, your own jid will be
used, so you can check what you are sharing).

.. note::

   you have to use the full jid of the device if you want to list files available on a
   device.

You may specify a path using ``-d PATH, --path PATH``.

File and directories are printed with a different colour if you use default output.

examples
--------

List files shared from a device (note that we use a full jid here)::

  $ li file share list louise@example.org/some_resource

List files available on a sharing service at the path ``/photos``::

  $ li file share list -d photos files.example.org

Louise wants to list the file shared by Pierre::

  $ li file share list pierre@files.example.org

path
====

Share a local file or directory with a list of entities, or publicly. The files can then
be listed or requested using libervia-cli_file_share_list_ or :ref:`libervia-cli_file_request`.

You specify the file or directory the positional ``path`` argument. By default the name of
the file/directory is used, but you can give a different one using ``-n NAME, --name
NAME``.

You can specify entities allowed to see your files using ``-j JID, --jid JID`` as many
time as necessary. If you don't specify any entity, the file will only be accessible by
your own devices. If you want to make your file accessible to everybody, use ``--public``
(note that this means that your file is accessible to the world, i.e. also to people you
don't know, so use this option carefully).

examples
--------

Share the file ``interesting_doc.odt`` with Pierre and Louise::

  $ li file share path -j pierre@example.net -j louise@example.org interesting_doc.odt

Imagine that you have built a weather station and want to make its data public. You can
share the directory ``~/weather_station_data`` with the world, using the name ``public
weather data``::

  $ li file share path --public --name "public weather data" ~/weather_station_data

invite
======

This command send an invitation for a file sharing repository to an XMPP entity.

The invitation is a non standard (yet?) way to notify somebody of the existence of a files
repository.

Beside the positional arguments ``service`` and ``jid``, which are respectively the
service where is the files repository and the jid of the entity to invite, you mainly have
to indicate the path and namespace of your repository, using ``-P PATH, --path PATH`` and
``N NAMESPACE, --namespace NAMESPACE``.

Use the ``-t {files,photos}, --type {files,photos}`` to specify if you repository is a
generic files repository or a photo album.

Optionally, you can associate a thumbnail to the repository ``with -T THUMBNAIL,
--thumbnail THUMBNAIL``. This is recommended to have more user friendly representation of
the album in e.g. Libervia.

example
-------

Pierre wants to invite Louise to view his ``summer holidays`` photo album::

  $ li file share invite -P "photos/summer holidays" -t photos pierre@files.example.net
  louise@example.org

affiliations
============

subcommands for file sharing affiliations management. please check :ref:`libervia-cli_file_share_affiliations`.

configuration
=============

subcommands for retrieving/modifying file sharing node configuration. please check :ref:`libervia-cli_file_share_configuration`.
