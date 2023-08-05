=========================================
ping: get response time of an XMPP entity
=========================================

``ping`` is more or less the equivalent of the command of the same name on most OSes, but
for XMPP. It send a `XEP-0199`_ PING and wait for the answer. When (and if) received, the
time to receive the answer is shown, else the time to receive the error message is shown.
This can be helpful to quickly test the connection with the server or a device.

If you need to get only the response time (without text around), you may use ``-d,
--delay-only``.

.. _XEP-0199: https://xmpp.org/extensions/xep-0199.html

example
-------

Get reponse time of a server::

  $ li ping example.org
