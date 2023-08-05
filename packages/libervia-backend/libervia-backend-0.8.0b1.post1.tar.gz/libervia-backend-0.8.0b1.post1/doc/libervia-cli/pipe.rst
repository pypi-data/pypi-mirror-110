==================================================
pipe: send/receive data stream through shell pipes
==================================================

``pipe`` commands allow you to send or receive data stream through a Unix shell pipe.
Libervia will create a network connection (using XMPP and Jingle) between you an your
contact.

in
==

Receive data stream. Data will be send to stdout, so it can be piped out or simply print
to the screen. You can specify bare jids of entities to accept stream for, by default all
streams are accepted.

example
-------

Receive a video stream, and redirect it to mpv_ so show the video::

  $ li pipe in | mpv -

.. _mpv: https://mpv.io/

out
===

Send data stream. Data comes from stdin, so you may use pipe in something or just write
some text.

The only expected argument is the full jid of the device where the stream must be piped
out.

example
-------

Send a video to louise::

 $ li pipe out louise@example.org/libervia.123 < some_video.webm

Send output from ``cal`` command to louise::

 $ cal | li pipe out louise@example.org/libervia.123
