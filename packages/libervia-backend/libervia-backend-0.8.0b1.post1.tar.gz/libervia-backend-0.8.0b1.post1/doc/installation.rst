.. _installation:

============
Installation
============

This are the instructions to install Libervia using Python.
Note that if you are using GNU/Linux, Libervia may already be present on your distribution.

Libervia is made of one backend, and several frontends. To use it, the first thing to do is to install the backend.

We recommand to use development version for now, until the release of 0.8.

Development version
-------------------

*Note for Arch users: a pkgbuild is available for your distribution on
AUR, check sat-xmpp-hg (as well as other sat-\* packages).*

You can install the latest development version using pip. You need to
have the following dependencies installed first:

-  Python 3 with development headers
-  Python 3 "venv", which may already be installed with Python 3
-  Mercurial
-  libcairo 2 with development header
-  libjpeg with development headers
-  libgirepository 1.0 with development headers
-  libdbus-1 with development headers
-  libdbus-glib-1 with development headers
-  libxml2 with development headers
-  libxlt2 with development headers
-  D-Bus x11 tools (this doesn't needs X11, it is just needed for dbus-launch)
-  cmake

On Debian and derivatives, you can get all this with following command::

  $ sudo apt-get install python3-dev python3-venv python3-wheel mercurial libxml2-dev libxslt-dev libcairo2-dev libjpeg-dev libgirepository1.0-dev libdbus-1-dev libdbus-glib-1-dev dbus-x11 cmake

Now go in a location where you can install Libervia, for
instance your home directory::

  $ cd

And enter the following commands (here we install Libervia with SVG support, which is needed to
display SVG avatars on some frontends)::

  $ python3 -m venv libervia
  $ source libervia/bin/activate
  $ pip install -U pip wheel
  $ pip install -r requirements.txt

Don't worry if you see the following message, Libervia should work anyway::

  Failed building wheel for pygobject

After installing Libervia, you need to install the media::

  $ cd
  $ hg clone https://repos.goffi.org/sat_media

then, create the directory ``~/.config/libervia``::

  $ mkdir -p ~/.config/libervia

and the file ``~/.config/libervia/libervia.conf`` containing:

.. sourcecode:: cfg

  [DEFAULT]
  media_dir = ~/sat_media

Of course, replace ``~/sat_media`` with the actual path you have used.

You can check :ref:`configuration` for details

Usage
=====

To launch the Libervia backend, enter::

  $ libervia-backend

…or, if you want to launch it in foreground::

  $ libervia-backend fg

You can stop it with::

  $ libervia-backend stop

To know if backend is launched or not::

  $ libervia-backend status

**NOTE**: if ``misc/org.libervia.Libervia.service`` is installed correctly (which should
be done by during the installation), the backend is automatically launched when a frontend
needs it.

You can check that Libervia is installed correctly by trying jp (the backend need to be
launched first, check below)::

  $ li --version
  Libervia CLI 0.8.0D « La Cecília » (rev 184c66256bbc [M] (default 2021-06-09 11:35 +0200) +524) Copyright (C) 2009-2021 Jérôme Poisson, Adrien Cossa
  This program comes with ABSOLUTELY NO WARRANTY;
  This is free software, and you are welcome to redistribute it under certain conditions.

If you have a similar output, Libervia is working.

.. note::

  if you have the message ``/!\ D-Bus is not launched, please see README to see
  instructions on how to launch it`` that mean that the D-Bus service is not launched, this
  usually happens when launching Libervia on a server, without graphic interface like X.org or
  Wayland (in which case D-Bus service should be launcher automatically).

  As the message states, instructions on how to launch the service are given in the README
  file of Libervia.

Frontends
=========

So far, the following frontends exist and are actively maintained:

Libervia Desktop (aka Cagou)
  desktop/mobile (Android) frontend

Libervia Web
  the web frontend

Libervia TUI (aka Primitivus)
  Text User Interface

Libervia CLI (aka jp or li)
  Command Line Interface

To launch Libervia TUI, just type::

  $ libervia-tui

then create a profile (XMPP account must already exist).

To use Libervia CLI, follow its help (``li`` is a shortcut for ``libervia-cli``)::

  $ li --help


There are some other frontends:

Bellaciao
  based on Qt, a rich desktop frontend (currently on hold)

Wix
  former desktop frontend based on WxWidgets (deprecated with version 0.6.0)

Sententia
  Emacs frontend developed by a third party (development is currently stalled)
