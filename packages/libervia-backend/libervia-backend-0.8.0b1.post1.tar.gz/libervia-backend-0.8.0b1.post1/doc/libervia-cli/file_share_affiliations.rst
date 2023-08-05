.. _libervia-cli_file_share_affiliations:

=============================================================
file/share/affiliations: file sharing affiliations management
=============================================================

``affiliations`` let you manage access permission to your shared files repository, in a
way similar as for pubsub.

Affiliations with file sharing are not standard and will only work with the Libervia file
sharing component.

Affiliations are similar to pubsub ones:

``owner``
  Has full permissions on the node, including changing affiliations. Owner can't be
  changed at the moment.

``publisher``
  Can read, upload and delete files

``member``
  Can access file but can't modify them or add new ones

``none``
  Is not a member of this node, use it to remove an existing affiliation.


get
===

Retrieve entities affiliated to this file sharing node, and their role

example
-------

Get affiliations of a file sharing node::

  $ li file share affiliations get -P "/some/path" louise@files.example.org

set
===

Set affiliations of an entity to a file sharing node.

examples
--------

Allow read access to a photo album to Louise::

  $ li file share affiliations set -c files.example.net -P "/albums/holidays" -a louise@tazar2.int member

Remove access to a directory from an old address of Pierre, and give it to the new one::

  $ li file share affiliations set -c files.example.net -N "some_namespace" -P
  "/interesting/directory" -a pierre@example.com none -a pierre@example.org member
