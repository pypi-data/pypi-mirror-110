==============================
forums: forums topics handling
==============================

Forums are internally a way to organise blog nodes open to many publishers. The ``forums``
commands let you manage the structure of topics. You may have several different structures
in one PubSub forums node, this can be useful if you have multi-lingual forums.

.. _libervia-cli_forums_get:

get
===

Get and print the structure of forums. Beside the classic PubSub node arguments, you may
specify the ``KEY`` of the forum with ``-k KEY, --key KEY``. This can be used to have
several structures of forums, for instance one per language.

If you use the default output, the verbosity is used to retrieve details of topics.

examples
--------

Get structure of default forum with details::

  $ li forums get -v

Get structure of French forums in JSON::

  $ li forums get -k fr -O json


edit
====

Edit the structure of XMPP forums. As for libervia-cli_forums_get_ you may specify the key beside
the classic PubSub node arguments. The edition works the same as for :ref:`libervia-cli_blog_edit`.

To edit the structure you'll get a JSON file which is a list of object where the topic
metadata are set. You can use the following metadata:

``main-language``
  a language code, using `ISO 639`_
``name``
  short name of the forum
``title``
  title of the topic/category in the given language
``short-desc``
  small description of the topic/category
``desc``
  long description of the topic/category
``uri``
  URI to the PubSub node containing the messages of the topic (it's actually a blog node
  with suitable permissions). URI must only be set for topic, not for categories.
``sub-forums``
  list of object with the same metadata (i.e. other topics or categories)

Here is a small example of a forum structure:

.. sourcecode:: json

   [
       {
           "main-language": "en",
           "name": "short-name",
           "title": "This is a category",
           "short-desc": "short description about the category",
           "desc": "this is a an example of a long description"
           "sub-forums": [
               {
                   "uri": "xmpp:pubsub.example.org?;node=org.salut-a-toi.forums%3A0_L5SaR5WYafXmUyD46R2avf",
                   "title": "some intereting topic",
                   "short-desc": "This is a description explaining what the topic is about"
               },
               {
                   "uri": "xmpp:pubsub.example.org?;node=org.salut-a-toi.forums%3A0_L5SaR5WYafXmUyD46R2avf",
                   "title": "a second topic",
                   "short-desc": "This topic is about bla bla bla"
               },
           ],
       },
       {
           "main-language": "en",
           "title": "An other category",
           "sub-forums": [
               {
                   "uri": "xmpp:pubsub.example.org?;node=org.salut-a-toi.forums%3A0_L5SaR5WYafXmUyD46R2avf",
                   "title": "yet another topic",
                   "short-desc": "This is a demo topic, made for an example"
               },
           ]
       }
   ]


.. _ISO 639: https://www.iso.org/iso-639-language-codes.html

example
-------

Edit structure of forums on a PubSub service::

  $ li forums edit -s pubsub.example.org
