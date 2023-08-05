.. _libervia-cli_file_share_configuration:

=========================================================
file/share/configuration: file sharing node configuration
=========================================================

``configuration`` commands are use to check or modify settings of a file sharing node.
This is not standard and specific to Libervia file sharing component.

The configuration is similar as pubsub one.

Only ``access_model`` can be used so far, with the ``open`` or ``whitelist`` values.


get
===

Retrieve file sharing node configuration.

example
-------

Get configuration of a file sharing node::

  $ li file share configuration get -P "/some/path" louise@files.example.org

set
===

Set configuration of a file sharing node.

example
-------

Make a repository public::

  $ li file share configuration set -c files.example.net -P "/public_files" -f
  access_model open
