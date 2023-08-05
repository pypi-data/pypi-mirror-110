.. highlight:: sh

================================
blog: (micro)blogging management
================================

Blog commands are high level tools to handle an XMPP blog.
They are using the generic pubsub arguments

set
===

publish a blog item.

:ref:`pubsub_common` commands are used to specify the destination item.

``stdin`` is used to get the body of the blog post.

examples
--------

Create a blog post with a body, a subject, 2 tags, and with comments allowed::

  $ echo "This is post body" | li blog set -T "This is a test message" -t test -t li -C

Create a blog post with rich content using `markdown` syntax, and no subject::

  $ echo "This is a **rich** body" | li blog set -S markdown

get
===

get command retrieves one or more blog post(s) from specified location (by default the
personal blog of the profile).

output can be customised to only retrieve some keys, or to use a specific template. For
instance, the following command retrieves only the title and publication date of the
personal blog of the profile::

  $ li blog get -k title -k published

:ref:`pubsub_common` commands are used to specify the blog location.

examples
--------

Retrieve personal blog of the profile using `fancy` output with a verbosity of 1 (to show
publication date)::

  $ li blog get -O fancy -v

Retrieve *title* and *publication date* of last 3 blog posts from the blog at
https://www.goffi.org::

  $ li blog get -m 3 -u https://www.goffi.org -k title -k published

Retrieve last 2 posts of personal blog, and output them in browser using default
template::

  $ li blog get -m 2 -O template --oo browser

.. _libervia-cli_blog_edit:

edit
====

With edit command you can create a new blog post or modify an existing one using your
local editor (the one set in ``$EDITOR``). You'll edit 2 things: the body of the post, and
the metadata which contain things like title, comments infos, or tags.

For some common editors (like **vim** or **Emacs**), the editor will be automatially
opened using a split screen with *body* in one side, and metadata on the other. If the
editor is not supported or doesn't support split screen, you'll edit first the *body*, then
the *metadata*. You can also specify editor and arguments in ``libervia.conf``, see
`configuration <edit_conf_>`_ below

If you don't change anything or publish an empty blog post, the edition will be cancelled.

In the metadata (see `below <edit_metadata_>`_ for details), you can use ``"publish":
false`` to forbid the publication (or set it with ``--no-publish argument``). In this
case, when you'll save your modification and quit your editor, the blog post will not be
published but saved locally in a draft. To continue your work later, just start your
edition with the ``-D, --current`` option like this::

  $ li blog edit -D

Note that item location must be re-specified if it has been used to create the draft, so
you'll have to reproduce the arguments to specify service, node or item (or the URL),
other data like tags will be restored from draft file of metadata.

You can specify the syntax by using ``-S SYNTAX, --syntax SYNTAX``. If not specified, the
syntax set in your parameters will be used.

When you edit a blog post, it is often useful to activate the ``-P, --preview`` option,
this will launch a web browser and refresh the page each time you save a modification in
your editor. By default, the browser registered as default in your system will be used,
and a new tab will be opened on each modification. This is not ideal, and we recommand to
set you configuration to activate automatic refreshing of the page instead, see `preview
configuration <edit_preview_>`_ below to see how to do.

.. note::

   If --preview doesn't work, use ``li blog preview`` (see below) to get error messages.
   On GNU/Linux, Be sure that inotify Python module is installed correctly.

examples
--------

Edit a new blog post with comments on your personal blog, using default syntax and preview::

  $ li blog edit -P --comments

Modifiy a draft previously saved using the ``"publish": false`` metadata::

  $ li blog edit -D

Correct a typo in your last published blog post::

  $ li blog edit --last-item

Edit the blog item at an HTTPS URL using XHTML syntax::

  $ li blog edit -u https://www.example.net/some_xmpp_blog_article.html -S xhtml

Create a new blog post on a XMPP blog node using its HTTPS URL (supposing here that
https://example.net is a XMPP blog node)::

  $ li blog edit -u https://www.example.net

.. _edit_metadata:

metadata
--------

Metadata is set using a JSON object. The key you can use are:

publish
  boolean indicating if item can be published. Set to ``false`` if you want to work on a
  draft and to avoid accidental publication.

atom_id
  atom entry identifier. This should not be modified manually.

published
  time of initial publication (unix time). This should not be modified manually.

language
  language of the content

comments
  array of URIs to the comments node, if any.

tag
  array of tags, if any

author
  human readable name of the entry author

author_jid
  jid of the author. This should notbe modified manually.

author_jid_verified
  true if the pubsub service confirmed that author_jid is the one of the publisher. It is
  useless to modify this variable.

title
  the title of the message

title_rich
  the rich title of the message, in current text syntax. It will be automatically
  converted to xhtml.

.. _edit_conf:

configuration
-------------

editor
^^^^^^

Local editor used is by default the one set in ``$EDITOR`` environment variable, but you
can specify one in ``libervia.conf``. To do so, you have to set the name of an editor
executable in  the ``editor`` option in ``[li]`` section.

You can specify the args to use by using ``blog_editor_args`` option. Use
``{content_file}`` to get the path of the main content file (the body of the blog post),
and ``{metadata_file}`` to get the path of the json metadata.

.. sourcecode:: cfg

   [li]
   editor = kate
   blog_editor_args = {content_file} {metadata_file}

.. _edit_preview:

preview
^^^^^^^

To set the preview, you can use the options ``blog_preview_open_cmd`` and
``blog_preview_update_cmd`` in your ``[li]`` section. the former is the command to use to
open your browser when edition starts, and the later is the command to use when a
modification is saved. In both cases you may use ``{url}`` to set the location of local HTML file.

This can be used to activate automatic refreshing of the page.

For **Konqueror**, you can use its D-Bus API to do refreshing. Ensure that ``qdbus`` is
installed on your system, and enter the following lines in your ``libervia.conf``:

.. sourcecode:: cfg

    [li]
    blog_preview_open_cmd = konqueror {url}
    blog_preview_update_cmd = /bin/sh -c "qdbus $(qdbus org.kde.konqueror\*) /konqueror/MainWindow_1 reload"

For **Firefox**, you may use ``xdotool`` on X11. Once you have installed this tool, enter the
following lines in your ``libervia.conf``:

.. sourcecode:: cfg

    [li]
    blog_preview_open_cmd = firefox -new-tab {url}
    blog_preview_update_cmd = /bin/sh -c "WID=$(xdotool search --name 'Mozilla Firefox' | head -1); xdotool windowactivate $WID; xdotool key F5"

This *xdotool* technique can be adapted to other browsers.

syntax extensions
^^^^^^^^^^^^^^^^^^

A dictionary with a mapping from syntax name to file extension can be used. This can be
useful to activate the right syntax highlighting in your editor. There is a default
mapping which can be overriden.

The mapping is set in the ``syntax_ext_dict`` option of the ``[li]`` section of your
``libervia.conf`` file. For instance, if your prefer do your ``.markdown`` for temp files
instead of the default ``.md``, you can use this:

.. sourcecode:: cfg

   [li]
   syntax_ext_dict = {"markdown": "markdown"}

the first ``markdown`` is the name of the syntax (could be an other syntax like ``xhtml``),
while the second if the file extension.

rename
======

Move a item to a new ID. This works the same as :ref:`li-pubsub_rename`, the only
difference is that node defaults to microblog default namespace.

example
-------

After a typo, a use want to rename the blog item with ID ``my_great_tittle_123a`` to
``my_great_title_123a``::

  $ li blog rename -i my_great_tittle_123a my_great_title_123a

preview
=======

This command will show the specified file in browser, and refresh it when changes are
detected. Configuration is the same as for `edit preview <edit_preview_>`_. This can be
used if you have already started an edition with ``li blog edit`` but forgot to use the ``-P, --preview`` arguments.

example
-------

Preview the draft at ``~/.local/share/libervia/blog/some_name/blog_something.md``::

  $ li blog preview ~/.local/share/libervia/blog/some_name/blog_something.md

.. _libervia-cli_blog_import:

import
======

With this command you can import an external blog in a XMPP blog at the specified pubsub
location.

The import is done using an *importer* name and a *location* which depends of the importer
(it can be a path to a file, an URL to a blog, or something else). Let empty to get list
of importers, and specify only importer name to get its description.

By default, found images are re-uploaded to XMPP server, if you want to keep original
URLs, use the ``--no-images-upload`` option.

Alternatively, you can re-upload images except for a specific host with ``--upload-ignore-host UPLOAD_IGNORE_HOST``. The images for the specified host will keep there original URLs while other will be uploaded to XMPP server.

You shoud specify original blog host using ``--host HOST`` argument, this is used notably
to reconstruct relative URLs of media.

Importers may have specific options, you can set them using the ``-o NAME VALUE, --option NAME VALUE`` argument. Check the importer description for details.

examples:
---------

List available importers::

  $ li blog import

Get description of ``dotclear`` importer::

  $ li blog import dotclear

Import a Dotclear blog::

  $ li blog import dotclear /path/to/dotclear.dump

Import a Dotclear blog without uploading images::

  $ li blog import --no-images-upload dotclear /path/to/dotclear.dump
