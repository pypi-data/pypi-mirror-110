.. _libervia-cli_documentation:

============
Libervia CLI
============

Libervia CLI is the Command Line Interface of Libervia

``libervia-cli`` is the command to launch it.

``li`` is short alias for ``libervia-cli``, it is the command used through this
documentation.

Overview
========

``li`` is a powerful tool to work with Libervia/XMPP.
With it you can send chat messages, share files, retrieve avatars, write blog entries, etc.

Usage
=====

To get help on commands or their options, use::

   $ li --help

which can be used on any command, so if you need help on ``message send`` command, just do::

   $ li message send --help

With li, you always enter commands first, then options and arguments.

There are several levels of commands: first one is the main category (``message``,
``blog``, ``avatar``, etc.), then there are often subcommands (e.g. ``message send``).

After the commands come the options. For instance if you want to send a message, you can
get the available options with ``--help`` as explained above::

   $ li message send --help
   usage: li message send [-h] [-p PROFILE] [--pwd PASSWORD] [-c] [-l LANG] [-s]
                          [-n] [-S SUBJECT] [-L SUBJECT_LANG]
                          [-t {chat,error,groupchat,headline,normal,auto}]
                          [-e ALGORITHM] [--encrypt-noreplace] [-x | -r]
                          jid

   positional arguments:
     jid                   the destination jid

   optional arguments:
     -h, --help            show this help message and exit
     -p PROFILE, --profile PROFILE
                           Use PROFILE profile key (default: @DEFAULT@)
     --pwd PASSWORD        Password used to connect profile, if necessary
     -c, --connect         Connect the profile before doing anything else
     -l LANG, --lang LANG  language of the message
     -s, --separate        separate xmpp messages: send one message per line
                           instead of one message alone.
     -n, --new-line        add a new line at the beginning of the input (usefull
                           for ascii art ;))
     -S SUBJECT, --subject SUBJECT
                           subject of the message
     -L SUBJECT_LANG, --subject_lang SUBJECT_LANG
                           language of subject
     -t {chat,error,groupchat,headline,normal,auto}, --type {chat,error,groupchat,headline,normal,auto}
                           type of the message
     -e ALGORITHM, --encrypt ALGORITHM
                           encrypt message using given algorithm
     --encrypt-noreplace   don't replace encryption algorithm if an other one is
                           already used
     -x, --xhtml           XHTML body

If you want to send a message to, say, ``pierre@example.net``, and encrypt it with OMEMO,
just do the following::

   echo "hi, I'm writing with li" | li message send -e omemo pierre@example.net

(note that with OMEMO, you need to have previously validated fingerprint of your contact
for this to work).

The different commands are explained in dedicated sections.

.. toctree::
   :caption: li commands:
   :glob:
   :maxdepth: 2

   common_arguments
   *


Tutorial
========

You can check this third party tutorial: https://blog.agayon.be/sat_jp.html
