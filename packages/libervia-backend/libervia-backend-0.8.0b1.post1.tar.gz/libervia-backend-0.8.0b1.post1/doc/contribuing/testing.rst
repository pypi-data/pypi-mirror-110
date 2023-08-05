=======
testing
=======

You'll find here the documentation to run tests on Libervia. If you plan to contribute
to the ecosystem, you should use them to check that your modification is not breaking
anything, and if possible you should extend them to cover any new feature.

.. _contributing-overview:

overview
========

Tests are run using `pytest`_ and are located in the ``tests`` directory.
You'll also find legacy tests in ``sat/test`` but those one are old, not maintained and
only kept there temporarily until they are ported to the new system.

For now, emphasis is put on end-2-end tests, as they are covering the whole ecosystem, and
are quite easy to write. The downside is that they are quite long to run.

Several `fixtures`_ are available in the various ``conftest.py`` files, it's a good idea
to have an overview of them if you're willing to write your own tests.

.. _pytest: https://www.pytest.org
.. _fixtures: https://docs.pytest.org/en/latest/fixture.html

end-to-end tests
================

End-to-end tests are located in ``tests/e2e``. They are launched in a well defined
environment managed through Docker. The ``docker/docker-compose_e2e.yml`` is used to
create the suitable containers.

A script is available at ``tests/e2e/run_e2e.py`` to launch the tests. It will create the
containers, bind the current code to them, and set environment variables according to
arguments.

The arguments set to this script are the ``pytest`` options, thus you can have a verbose
mode with ``-v`` and select specific test with ``-k EXPRESSION`` (see ``pytest --help`` for
details).

In addition to pytest option, some flags can be set with the following arguments:

``--visual``
  Launch a VNC viewer to see in real time browser based tests. You must have ``vncviewer``
  executable available in your path (this is part of `TigerVNC`_)

``--keep-containers``
  Do no remove Docker container after the end of tests.

``--keep-profiles``
  Do not delete test profiles after the end of tests

``--keep-vnc``
  Do not stop VNC viewer after the end of tests. This argument implies ``--visual``.

``--keep-browser``
  Do not kill the browser inside the container after tests are done. This argument implies
  ``--keep-container`` and ``--keep-vnc``.

``--dev-mode``
  Shortcut for ``--keep-containers``, ``--keep-profiles`` and ``--keep-vnc``. This is
  useful, as you guess with its names, for development of tests. User can then log-in into
  the ``backend`` container, launch a Python console, and work with the automated browser in
  real-time. Basic commands to launch a browser and log-in with test account are printed
  at the end of the tests. Note that if you want to have profiles created, or extra tools
  like the fake SMTP server, you'll have to launch at least one test which require them.
  To log-in into the ``backend`` container, you can use the following command, from
  ``/docker`` directory::

  $ docker-compose -f docker-compose_e2e.yml exec backend /bin/bash

  Then run a python console with given instructions

It's also good to know that in the e2e test environment, the following pytest plugins are
installed and used:

`pytest-timeout`_
  To avoid having test stuck, it's good to terminate them after a while. A timeout of 60s
  is set by default for each test (lower value can give false negatives, as some e2e tests
  can be long, notably with Selenium).

`pytest-dependency`_
  Even if good testing practice normally means that tests can be run independently, in the
  case of e2e tests we are using a real environment, and some tests do create files,
  PubSub nodes, accounts, etc. It would be resource consuming to delete then recreate them
  only to have standalone tests, thus to keep tests short and simple, some of them must be
  run in order. The *dependecy* plugin is used to manage that, and will skip tests if one
  of their dependencies is failing. The markup help also to document the tests order.

.. _TigerVNC: https://tigervnc.org
.. _pytest-timeout: https://github.com/pytest-dev/pytest-timeout
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency

common fixtures
---------------

Here are the fixture common to all e2e tests which are good to know:

``test_profiles``
  Creates a bunch of test accounts which are available during the whole test session.
  Those account are destroyed once all the tests are finished (successful or not), except
  if you set the ``LIBERVIA_TEST_E2E_KEEP_PROFILES`` environment variable (or use the
  ``--keep-profiles`` flag in ``run_e2e.py``.

  The profiles created are in the form ``accountX`` for account on the ``server1.test``,
  or ``accountX_sY`` for account on other servers (see the docstring for details).

  This fixture should be used on top of each e2e test module.

``pubsub_nodes``
  Create 2 pubsub nodes with ``open`` access model and named ``test`` (one on ``account1``
  PEP service, and the other one on ``pubsub.server1.test``, created with the same
  account).

  Those node are created for the scope of the class.

``fake_file``
  Create files filled with random bytes, and check them.

  A file is created by calling ``fake_file.size(size)``, and by default files of the same
  size are re-used (set ``use_cache=False`` to create new files). This method returns a
  ``pathlib.Path``. SHA-256 hash of the created file can be retrieved using
  ``fake_file.get_source_hash(source_file_path)`` with the file path as argument.

  ``fake_file.new_dest_file()`` will return a Path to a randomly named destination file,
  and ``fake_file.get_dest_hash(dest_file_path)`` will generate its hash once written.

``sent_emails``
  When used, a fake SMTP server (already configured in container's ``libervia.conf``) will be
  launched if it's not already, and all messages sent to it since the beginning of the test
  will be available in the given list. Message are subclasses of
  ``email.message.EmailMessage`` with the extra properties ``from_``, ``to``, ``subject``
  and ``body`` available for easy access to their content.

  The SMTP server is terminated at the end of the test session.

libervia-cli e2e tests
----------------------

End-to-end tests for ``libervia-cli`` are a good way to tests backend features without having to
deal with frontends UI. Those tests use extensively the ``sh`` module, which helps
writing ``libervia-cli`` commands like if they where methods.

Among the helping fixture (check the various ``conftest.py`` files for details), the
following are specially good to know:

``li_json``
  Set the ``json_raw`` output are parse it. When you use this instead of the normal ``libervia-cli``,
  you'll get a Python object that you can manipulate easily.

``li_elt``
  Set the ``xml_raw`` output and parse it as a Twisted ``domish.Element``. When you use a
  command which can return XML, it is useful to get this object which is easy to
  manipulate in Python.

``editor``
  Create a fake editor (replacing the one normally set in ``EDITOR`` environment
  variable), to automatically modify and/or check the text sent by a command. You can
  specify Python code to execute to modify the received text with the ``set_filter``
  method (this code is in a string which will be executed by Python interpreter, where the
  ``content`` variable is the received text). By default, the text is kept unmodified.

  After ``editor`` has been used by the ``libervia-cli`` command, you can check its
  ``original_content`` property to see the text that it received, and ``new_content``
  property to see the text that has been written after updating the original content with
  the code set in ``set_filter``.

Libervia e2e tests
------------------

E2e tests for Libervia are executed, as it is common in web world, with `Selenium`_: user
actions are simulated in automated browser, and results are checked.

To make the tests as easy to write as possible, and as natural to read as possible, the
higher level `Helium`_ Python module is used. Thanks to it, the tests can read pretty much
like instructions we would give to a human user. Helium makes also easy to do some tasks
more complicated with Selenium alone, like dropping a file to an element.

If a test is failing, a screenshot of the browser is taken. If you run the tests though
the ``run_e2e.py`` command (which you should), you'll find the screenshots in the
``report_*`` directory which is created in working dir in case of failure.

Here are the helping fixtures which are notably good to know, you should always use either
``log_in_account1`` or ``nobody_logged_in``:

``log_in_account1``
  Start the test with the main test account logged.

``nobody_logged_in``
  Start the test without anybody logged (this is done by clearing all cookies).

.. _Selenium: https://www.selenium.dev
.. _Helium: https://github.com/mherrmann/selenium-python-helium

examples
--------

Following examples have to be run from ``tests/e2e`` directory.

Run all tests for ``Libervia CLI``::

  $ ./run_e2e.py -k libervia-cli

Run all tests for ``Libervia Web`` with real-time visual feedback (note that you need to have
``vncviewer`` installed and available in path, see above)::

  $ ./run_e2e.py -k libervia-web --visual


Run all tests with verbose mode (useful to know which test is currently running)::

  $ ./run_e2e.py -v

Run pubsub tests in verbose mode::

  $ ./run_e2e.py -k pubsub -v

Run in dev mode, to work on new tests, note that we run the ``user_can_create_account``
test to be sure to have test profiles created and fake SMTP server run…::

  $ ./run_e2e.py -k user_can_create_account --dev-mode

…then to go into the ``backend`` container and work with the browser (to be run in ``docker``
directory)…::

  $ docker-compose -f docker-compose_e2e.yml exec backend /bin/bash

…and, inside the container, you can now run ``python3`` and enter instruction prints at
the end of the test session.
