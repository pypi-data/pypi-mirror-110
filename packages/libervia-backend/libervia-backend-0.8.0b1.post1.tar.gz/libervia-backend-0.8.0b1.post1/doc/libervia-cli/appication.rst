=============================================
application: external applications management
=============================================

Libervia can launch and manage external applications. This is useful to integrate external
services, notably in the web frontend. The command can be used either with ``application``
or the shortcut ``app``.

list
====

List available applications. This command can show either the list of available
application (which could be launched) and/or the list of running application.

By default both available and running application are shown, this can be filtered by using
``-f {available,running}, --filter {available,running}``

example
-------

List available applications::

  $ li app list -f available

start
=====

Start an application. Depending on the application and its availability locally, this make
take some time (resources may have to be downloaded).

example
-------

Start Weblate::

  $ li app start weblate

.. _li_app_stop:

stop
=====

Stop an application. If several instances of the same application are running, ``-i ID,
--id ID`` can be used to specify which one must be stopped.

example
-------

Stop Weblate::

  $ li app stop weblate


exposed
=======

List exposed values from a running application. Exposed values may be the port used,
passwords automatically generated, or fields useful for web integration.

As for :ref:`li_app_stop`, if several instances of the same application are running, one
can be specified using ``-i ID, --id ID``.

example
-------

Show exposed values of a running Weblate::

  $ li account application exposed weblate
