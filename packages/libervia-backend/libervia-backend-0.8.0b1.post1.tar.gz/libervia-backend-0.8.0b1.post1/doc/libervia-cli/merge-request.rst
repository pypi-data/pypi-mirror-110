===============================================
merge-request: create and manage merge requests
===============================================

Merge-request are used to propose some modifications to a project. They are generic and
are made to be used with several backends, but only Mercurial is implemented so far.

To prepare a merge request with Mercurial, you just need to have a clone of the project,
and do your modifications (either directly, or in a bookmark, a branch, or a MQ patch).

set
===

Create and publish a merge request. Once the modification on the project are done, simply
run the command from the repository (or specify its path with ``-r PATH, --repository
PATH``). If the project has set metadata (it can be done with a magic string in README),
you don't have to specify any service or node, it will be set automatically (but you still
can specify them if needed).

You may associate one or more labels to your request using ``-l LABELS, --label LABELS``.

By default, a confirmation is requested before publishing the request, you can publish
without confirmation by using the ``-f, --force`` flag.

If you have already done a merge request and you just want to update it, check its id and
specify it with ``-i ITEM, --item ITEM``, this will override the previous request with the
new updated one.

examples
--------

Publish a merge request (to be executed from the repository of the project you have
modified)::

  $ li merge-request set

Update an existing merge request, which has the id ``123`` (to be executed from the
reposiroty of the project you have modified)::

  $ li merge-request set -i 123

Do a merge request for repository at path ``~/some_project``, specifying a label
indicating it's work in progress (WIP)::

  $ li merge-request set -r ~/some_project --label WIP


get
===

Get and print one or more merge requests. By default only some metadata are shown (without
the patches), but you can use ``--verbose, -v`` to show details.

examples
--------

Show some metadata of last 5 merge requests::

  $ li merge-request get -M 5

Display details for merge request with id 456::

  $ li merge-request get -v -i 456


import
======

Import a merge request into your project. You mainly have to be in the project repository
(or specify it using ``-r PATH, --repository PATH``) and to specify the id of the patch to
import (using ``-i ITEM, --item ITEM``). The behaviour depends of the type of the patch,
for Mercurial, the patch will be imported as `MQ`_ patch.

.. _MQ: https://www.mercurial-scm.org/wiki/MqExtension

example
-------

Import the merge request with id 321::

  $ li merge-request import -i 321
