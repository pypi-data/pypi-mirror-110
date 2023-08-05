=============================
shell: use Libervia with REPL
=============================

``shell`` launch a read–eval–print loop (REPL) with some helpers to launch li commands.
This is useful if you are willing to a session when you'll use several commands in a row
(for e.g. to inspect something on a PubSub service).

start the shell
===============

To start the shell, you just have to enter ``li shell``. You can eventually specify a
profile to use an other one than the default one by entering ``li shell -p
<some_profile>``.


.. _libervia-cli_shell_use:

use the shell
=============

Once in the shell, you can launch a command by entering it as usual (without having to
specify ``li``). For instance to get last 2 blog posts from your personal blog, you just
have to enter::

  > blog get -m 2

There are 2 kinds of commands in the shell:

- **shell commands** which are command to manipulate the shell itself
- **li commands** which are the classic commands that you use with li

The most important thing to remember is that you can use ``?`` (or ``help`` which is
equivalent) to get the list of commands (shell + li), and ``?<command>`` (or ``help
<command>``) to get information on a shell command. For li commands, you can use the usual
``--help`` argument.

You may move in the commands hierarchy using ``cmd`` which can be seen as something
roughly equivalent to ``cd`` for the filesystem. for instance if you know you'll work with
XMPP blogs, you can enter::

  > cmd blog

Then you'll be in the blog hierarchy, you can check that by entering ``?``. From there you
can use blog commands directly, like in this example to retrieve last 2 blog posts::

  blog> get -m 2

You can even go further, e.g. if you know that you'll do several ``get`` command (in this
can you'll only have to specify the arguments of ``get``)::

  blob> cmd get
  blog/get> -m 2

You can use ``/`` with ``cmd``, including as first character to indicate that you want to
start from root::

  blog/get> cmd /pubsub
  pubsub> cmd node/info

Similarly, you can use ``..`` to move to parent command::

  pubsub/node/info> cmd ..

One of the interesting feature of shell is that you can fix an argument, i.e. indicate
the value to use in the next commands. For instance if you're willing to work on a
specific node, you can set its value with ``use``::

  blog> use node some_interesting_node

Then you won't have to specify it anymore for each command. The name of the argument to
fix must be the long form. To check which arguments are fixed, just enter ``use`` without
argument. If an argument is fixed but not used in a command, it will be ignored.

To clear a fixed argument, you have the ``use_clear`` command. To clear the ``node``
argument set above, just enter::

  blog> use_clear node

Without argument, all fixed arguments will be cleared.


Shell commands
==============

Below is a description of shell commands.


cmd
---

Move in the command hierarchy, this avoid to type again a command if you know you'll use
it several times. See libervia-cli_shell_use_ for explanation and examples

do
--

Launch a li command. By default the command is launched if you enter directly its name and
arguments, but if a command or argument conflict with a shell command, the shell command
will be launched instead. The ``do`` command avoid such a situation by always launching a
li command::

  > do blog get -m 2

exit
----

Quit the shell (alias of ``quit``).

help (alias ``?``)
------------------

Give information on available commands or on a specific command, see libervia-cli_shell_use_ for
more explanations.

examples
^^^^^^^^

Get general help::

  > ?

Get help on ``do`` command::

  > ?do

quit
----

Quit the shell

shell (alias ``!``)
-------------------

Launch an external command.

example
^^^^^^^

Print a calendar with ``cal``::

  > !cal

use
---

Fix the value of an argument, which will then be set for all following commands, see
libervia-cli_shell_use_ for more explanations.

Without argument, show all fixed arguments

examples
^^^^^^^^

Fix the PubSub node (the long name of the argument is used, so it will go to ``--node``)::

  pubsub> use node some_intersting_node

Show all fixed arguments::

  > use

use_clear
---------

Unfix the value of an argument (i.e. use the normal default value). Without argument,
it unfixes all arguments.

examples
^^^^^^^^
Clear the node::

  pubsub> use_clear node

Clear all arguments::

  > use_clear

verbose
-------

Without argument, show if verbose mode is activated. With an argument evaluating to a
boolean, activate or deactivate this mode.

In verbose mode, the fixed arguments and the command launched are printed before launching
a li command.

examples
^^^^^^^^

Show if verbose mode is activated::

  > verbose

Activate verbose mode::

  > verbose on

version
-------

Print current version of li/Libervia.

whoami
------

Show the name of the connected profile (the one set with ``--profile`` when launching the
shell). This profile will be used as default profile.
