============================
bookmarks: get/set bookmarks
============================

Bookmarks are links to MUC rooms or URLs with a few metadata. Due to historical reasons,
XMPP has several ways to handle bookmarks, and Libervia handle them as transparently as
possible.

With Libervia there are 3 places where you can get/store your bookmarks:

local
  the bookmarks is stored only locally in the database of Libervia. It won't be available to
  other devices.
private
  the bookmarks use the old private XML storage (`XEP-0049`_). It is not recommended to
  use this if PubSub storage is available
pubsub
  the bookmarks use PEP storage (`XEP-0223`_), this is the currently recommended way to
  store bookmarks.

When possible, you can specify ``auto`` to let Libervia choose the best location (i.e.
``pubsub`` if available, then ``private`` then ``local`` if nothing else is possible).

.. _XEP-0049: https://xmpp.org/extensions/xep-0049.html
.. _XEP-0223: https://xmpp.org/extensions/xep-0223.html


list
====

Get and print available bookmarks. You specify the location of the bookmarks to print
using ``-l {all,local,private,pubsub}, --location {all,local,private,pubsub``, by default
all bookmarks from all locations are printed.

Use ``-t {muc,url}, --type {muc,url}`` to indicate if you want to print MUC bookmarks or
URLs.

After printing the bookmarks location, the bookmarks will show the name and location (jid
for MUC or URL). For MUC bookmarks you'll also see nickname, and a star (``*``) if
autojoin is set.


examples
--------

Retrieve all MUC bookmarks::

  $ li bookmarks list

Retrieve all bookmarked URL stored in PubSub::

  $ li bookmarks list -l pubsub -t url


remove
======

Delete a bookmark. You need to specify the jid of the MUC room or the URL to remove as
positional argument. If you are deleting an URL, you need to specify it with ``-t url``

By default a confirmation is requested, use ``-f, --force`` if you don't want it (with
usual caution).

examples
--------

Delete the bookmark of a MUC room that you are not following anymore::

  $ li bookmarks remove some_old_room@conference.example.net

Delete the bookmark of a URL without requesting confirmation::

  $ li bookmarks remove -t url https://unused_url.example.net


add
===

Create or update a bookmark. The bookmark itself (URL or JID of the MUC) is specified as
positional argument. If you are bookmarking an URL, you need to specify it with ``-t
url``. A name is often helpful, use ``-n NAME, --name NAME`` to specify it.

For MUC only, you can specify the nick to use on the room with ``-N NICK, --nick NICK``,
and the flag ``-a, --autojoin`` indicates if you want to join the chat room automatically
when you're connecting.

If you're using add on a jid/URL which already exists, the metadata will be updated.

examples
--------

Add a bookmark to Libervia official chat room::

  $ li bookmarks add sat@chat.jabberfr.org -a

Add a link to Libervia official website::

  $ li bookmarks add -t url https://www.salut-a-toi.org -n "Libervia officiel"
