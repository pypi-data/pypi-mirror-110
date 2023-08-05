=================================
param: manage Libervia parameters
=================================

``param`` commands allows to retrieve or set parameters as well as to export/import them
to a XML file.

Parameters are retrieve using a ``category`` and a ``name``, they are both case sensitive.

``category`` is the name of the tabs that you see when you set parameters in a frontend
like Cagou or Libervia.

.. note::

   You need to have your session started to retrieve of modify parameters. If you can't
   or are not willing to connect for any reason (e.g. no internet connection), you can
   use the ``--start-session`` option to start the profile session without connecting it
   to the XMPP server.

get
===

Retrieve list of categories, parameters or a specific parameter value:

- without argument, you'll get the list of categories
- with only a category specified, you'll get a list of parameters and their values
- with a category and a name, you'll get the value or requested attribute of the specified
  parameters

By default you'll get the value of the parameters, but you can request an other attribute
(for instance its ``type`` or ``constraint``) using the ``-a ATTRIBUTE, --attribute
ATTRIBUTE`` argument.

You can set a security limit to retrieve only parameters allowed with this limit.
Security limit is an integer used in some frontends (like Libervia), to restrict
parameters modifiable by non privileged users. You can set it using ``--security-limit
SECURITY_LIMIT``, by default it is disabled (i.e. all parameters are returned).

examples
--------

Get list of categories::

  $ li param get

Get list of parameters in ``General`` category::

  $ li param get General

Get JID set for default profile. It is set in ``Connection`` category, with the parameters
named ``JabberID`` (be careful with the case)::

  $ li param get Connection JabberID

Get the type of the ``check_certificate`` parameters in ``Connection`` category::

  $ li param get Connection check_certificate -a type

Get the constraint of the ``Priority`` parameters in ``Connection`` category::

  $ li param get Connection Priority -a constraint

set
===

As expected, this command set a Libervia parameter. The ``category``, ``name`` and ``value``
are needed as positional arguments.

``--security-limit SECURITY_LIMIT`` can be used if you want an update to be rejected if
the parameter is not modifiable with this limit. This can be useful if you use ``li`` from
an external tool and you want to limit damage risks, or for testing purpose.

examples
--------

Use Markdown_ syntax for composition (e.g. for editing blog posts)::

  $ li param set Composition Syntax markdown

Try to change jid of the profile with a low security limit, this command should fail::

  $ li param set --security-limit 0 Connection JabberID some_random_jid@example.org

.. _Markdown: https://daringfireball.net/projects/markdown/

.. _libervia-cli_param_save:

save
====

Save the parameters structure to an external files. The parameters are saved as XML. The only
expected argument is the path to the destination file.

.. note::

   it's the parameters structure and not the parameters values which are saved. This is
   low level method and most end users won't probably need it

example
-------

Save parameters structure to ``~/parameters.xml``::

  $ li param save ~/parameters.xml

.. _libervia-cli_param_load:

load
====

Load and merge the parameters structure from external XML files. The only expected
argument is the path to the source file.

.. note::

   it's the parameters structure and not the parameters values which is loaded and merged.
   This is low level method and most end users won't probably need it

example
-------

Load and merge parameters structure from ``~/parameters.xml``::

  $ li param load ~/parameters.xml
