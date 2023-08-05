========================================
file: files sending/receiving/management
========================================

``file`` group all commands related to file management, and allows you to send easily a
file to a contact or device from the command line.

send
====

Send a file to a contact.

The file will be sent using best available method (which is Jingle File Transfer when
available), and will try to send the file in P2P when possible.  If P2P is possible, the
signal is sent through the server (metadata, negotiation, etc.), while the file itself
goes directly from the source device to the target device. When P2P is not possible, the
file may go through the server or an other one (if a proxy is used for instance).

When sending a file, you specify one or more file(s) to send, and the either the bare jid
or the full jid of the target device. If bare jid is specified, the main resource will be
used.

You'll usually want to see the progression of the transfer, use ``-P, --progress`` for
that.

If you send several files at once, you may want to use ``-b, --bz2`` to group them in a
single compressed ``tar.bz2`` archive (the client receiving the files will then receive a
single file, than the user can then decompress).

By default the name of the source file is used, but you use ``-n NAME, --name NAME`` to
specify another one.

The path and namespace (set with ``-d PATH, --path PATH`` and ``-N NAMESPACE, --namespace
NAMESPACE``) are non-standard metadata used by Libervia to organise files (``PATH`` being like
a file path on locale file system, and ``NAMESPACE`` being a name to associate to a group
of files, for instance for a photo album).

examples
--------

Send a file to Louise, with a progress bar::

  $ li file send -P some_file.ext louise@example.org

Send a picture to a file sharing component, putting it in the ``holidays`` namespace, in
the ``/some/path`` path::

  $ li file send -P -N holidays -d /some/path some_photo.jpg files.example.org

.. _libervia-cli_file_request:

request
=======

Ask to get a file from a device/sharing service. A file is requested using one or more
metadata, which can be the file name (with ``-n NAME, --name NAME``), its hash (with ``-H
HASH, --hash HASH`` and the algorithm may be specified with ``-a HASH_ALGO, --hash-algo
HASH_ALGO``), its path (with ``-d PATH, --path PATH``) and its namespace (with ``-N
NAMESPACE, --namespace NAMESPACE``). Note that ``PATH`` and ``NAMESPACE`` are Libervia specific
and not (yet?) XMPP standards.

If you already know the hash, it's the most efficient and recommended way to retrieve a
file.

You need to specify the full jid of the device or the sharing service as a positional
argument.

By default the file is downloaded in current directory, but you can specify an other one
(and an other filename) with ``-D DEST, --dest DEST``.

If you want to see progression of the transfer, use ``-P, --progress``.

examples
--------

Request a file names ``some_file.jpg`` in path ``/photos/demo_album`` at service
``files.example.org``, with a progress bar::

  $ li file request -P -d photos/demo_album -n some_file.jpg files.example.org

Request file with given ``sha-256`` hash (which is default hash algorithm, so we don't
specify it), and save it to file ``dest_file.txt``::

  $ li file request -H f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2 -D dest_file.txt files.example.org

receive
=======

Wait for a file (or several ones) to be received, and accept it if it match criteria.

You should specify which jid you are expecting a file from, using the positional
arguments. If you don't, all files will be accepted, which can be dangerous if some
malicious user send you a file at this moment.

To see progression (this is recommended), you can use the ``-P, --progress`` options.

By default, if a file with the same name as the proposed one exists, the transfer will be
denied. You can override this behaviour with ``-f, --force``, but be sure to absolutely
trust the sender in this case, as the name is chosen by her, and could be malicious, or it
could override an important file.

If you expect several files, you can use the ``-m, --multiple``, in this case the command
won't stop after the file received file, and you'll have to manually stop it with
``Ctrl-C`` or by sending a ``SIGTERM``.

File(s) will be written in the current directory, but you may specify an other destination
with ``--path DIR``.

examples
--------

Accept and receive the next file, save it to local directory and show a progress bar::

  $ li file receive --progress

Several files are expected from Louise, accept them and store them do
``~/Downloads/Louise``::

  $ li file receive --multiple --path ~/Downloads/Louise louise@example.org

get
===

Download a file from an URI. This commands handle URI scheme common with XMPP, so in
addition to ``http`` and ``https``, you can use it with ``aesgcm`` scheme (encrypted files
with key in URL, this is notably used with OMEMO encryption).

As usual, you can use ``-P, --progress`` to see a progress bar.

example
-------

Download an encrypted file with a progress bar, and save it to current working directory
with the same name as in the URL (``some_image.jpg``). The URL fragment part (after ``#``)
is used for decryption, so be sure to not leak the URL when you manipulate one::

  $ li file get -P "aesgcm://upload.example.org/wvgSUlURU_UPspAv/some_image.jpg#7d8509c43479591f8d8492f84369875ca983db58f43225c40229eb06d05b2037c841b2346c9642a88ba4a91aa96a0e8f"

upload
======

Upload a file to your XMPP server (or an other entity if specified). The upload will be
done using `XEP-0363 (HTTP File Upload)`_, and the public URL to retrieve the file will be
printed. Note that anybody knowing this URL can download the file you've uploaded.

The path to the file to upload is expected as first argument, then optionally the entity
of the service to upload too (by default, this is autodetected if your server offers this
feature).

As usual, you can use ``-P, --progress`` to see a progress bar.

You can encrypt the file using ``AES GCM`` with the ``-e, --encrypt`` argument. You will
then get an ``aesgcm://`` link instead of the usual ``https``, this link contains the
decryption key (in the fragment part) so be sure to not leak it and to transmit it only
over encrypted communication channels.

.. _XEP-0363 (HTTP File Upload): XEP-0363: HTTP File Upload

example
-------

Upload a document to a server::

  $ li file upload -P ~/Documents/something_interesting.odt

Encrypt and upload a document to server::

  $ li file upload -P -e ~/Documents/something_secret.odt

share
=====

Subcommands for advanced file sharing. Please check :ref:`libervia-cli_file_share`.
