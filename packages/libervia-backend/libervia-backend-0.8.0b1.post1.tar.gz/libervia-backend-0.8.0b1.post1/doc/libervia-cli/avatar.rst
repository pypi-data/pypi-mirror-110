===============================
avatar: retrieve/upload avatars
===============================

Avatars are images associated to an XMPP entity. Several XMPP extensions are in use, Libervia
tries to hide the technical details so avatar are as easy as possible to manipulate for
end-user.

get
===

Retrieve the avatar of the given entity. Entity jid is specified as positional argument.

If an avatar is found, a path to its cached file is printed. Please note that this is the
cache used by all Libervia ecosystem, **do not modify the cached image**. You may use it for
read-only access, or copy it if you want to modify the image.

You may use the ``-s, --show`` argument to display the found avatar. The software used to
display the image can be specified in Libervia configuration (cf. :ref:`configuration`), in the
``[li]`` section: the ``image_cmd`` setting let you specify the path to the software. If
``image_cmd`` is not used, ``li`` will try some common software, and if none is found, it
will try to open the image in a browser (which may sometimes result in using the default
image software of the platform).

When available, cached avatar is returned by defaut. If you want to ignore the cache, use
the ``--no-cache`` option (of course this can result in more network requests).

example
-------

Get the avatar of ``louise@example.org`` and display it::

  $ li avatar get --show louise@example.org


set
===

Upload and set the given avatar for the profile. The only required argument is the path to
the image to use as avatar.

example
-------

Set the avatar of the default profile::

  $ li avatar set ~/photos/some_photo.jpg
