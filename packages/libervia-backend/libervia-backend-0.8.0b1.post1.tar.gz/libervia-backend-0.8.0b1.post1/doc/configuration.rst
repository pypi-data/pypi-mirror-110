.. _configuration:

=============
Configuration
=============

Libervia main configuration is set in a file named ``libervia.conf`` (which may be prefixed
by a ``.`` if you want to hide it on suitable platforms). It is a common file used both by
backend and all frontends (and even related project like Libervia Pubsub).

This file can be located in the following paths (in order of parsing):
  - ``/etc``
  - ``~`` (``$HOME`` or your home directory)
  - XDG directory for configuration (most of time it is
    ``~/.config/libervia/``)
  - the parent directory of Libervia installation path

If several configurations files are found, they are merged. In case of conflict, the
option parsed last is the one used (in other words: if you have an option set in
``/etc/libervia.conf`` and the same one set in ``~/.libervia.conf``, the one from ``~/.libervia.conf``
will be used because it is parsed after ``/etc``).

Format
======

``libervia.conf`` is using the `INI`_ file format as understood by Python's `SafeConfigParser`_
(meaning that you can use interpolation).

The ``DEFAULT`` section is used for global options, this is where you specify where are
your media.

Each frontend can have specific section with its name in lowercase (sections are case
sensitive), and some backend plugin can use specific sections too (usually named ``plugin
<plugin name>``). The ``pubsub`` section is used by ``Libervia PubSub``. A section can also
have the name of a web site used with Libervia web framework.


To recapitulate, you can have the following sections in your ``libervia.conf``:

``[DEFAULT]``
  the main, global section
frontend name (in lower case)
  frontend specific settings. Some examples:

  - ``[desktop]``
  - ``[cli]``
  - ``[tui]``
  - ``[web]``
``[plugin <plugin name>]``
  backend plugin specific settings. Some examples:

  - ``[plugin account]``
  - ``[plugin muc]``
  - ``[plugin search]``
``[pubsub]``
  Libervia PubSub settings
``[<website name>]``
  the settings of a website for Libervia web framework

.. _INI: https://en.wikipedia.org/wiki/INI_file
.. _SafeConfigParser: https://docs.python.org/2/library/configparser.html

In the section, the option names suffixes are used to identify the type of settings:

- ``_dir`` is used to indicate a path to a directory
- ``_path`` is used to indicate a path (generally to a file, ``_dir`` being used for
  directories)
- ``_int`` indicate a integer
- ``_list`` indicate a list comma-separated values
- ``_dict`` indicate a dictionary
- ``_json`` is used for complex data, represented with JSON format

Remember that if you want to span your data on several lines (which is often used with
``*_dict`` or ``*_json`` options), you need to indent the extra lines and keep the same
indentation.

Sample
======

Here is a configuration that you can use as a model to specify your own settings. Check
the comments to get the meaning of each option.

.. sourcecode:: cfg

    [DEFAULT]
    ; where Libervia media are located
    media_dir = ~/workspace/sat_media
    log_level = debug
    ; domain used for new accounts
    xmpp_domain = example.net
    ; list of profiles with admin rights
    admins_list = toto,titi
    ; settings to let the backend send emails
    email_from = NOREPLY@example.net
    email_server = localhost
    # email_port =
    # email_username =
    # email_password =
    # email_starttls = true
    # email_auth = true
    # email_admins_list = toto@example.net, titi@example.org
    ; override DNS records
    hosts_dict = {
        "example.org": {"host": "127.0.0.1"}
        }
    ; background luminance, used by terminal frontends
    ; can be "auto" (default) to autodetect, "dark" or "light"
    background = auto

    [plugin account]
    ; where a new account must be created
    new_account_server = localhost
    new_account_domain = example.net

    [plugin muc]
    ; default room to use in the "Join room" menu
    default_muc = sat@chat.jabberfr.org

    [tui]
    log_level = debug
    ; how the logs are formatted
    ; note that "%" must be doubled here
    log_fmt = %%(levelname)s: %%(message)s
    ; use bracketed paste mode
    bracketed_paste = true

    [cli]
    ; how to use xdotool to refresh Firefox when doing "li blog edit"
    blog_preview_open_cmd = firefox -new-tab {url}
    blog_preview_update_cmd = /bin/sh -c "WID=$(xdotool search --name 'Mozilla Firefox' | head -1); xdotool windowactivate $WID; xdotool key F5"
    ; and below the equivalent with Konqueror
    # blog_preview_open_cmd = konqueror {url}
    # blog_preview_update_cmd = /bin/sh -c "qdbus $(qdbus org.kde.konqueror\*) /konqueror/MainWindow_1 reload"

    [web]
    ; do we want "http", "https" or "both"?
    connection_type = both
    port = 8080
    port_https = 8443
    ; external port used for HTTPS (0 to use "port_https" value)
    port_https_ext = 443
    ; TLS public certificate or private key
    ; and public certificate combined (PEM format)
    tls_certificate = libervia.pem
    ; TLS certificate private key (PEM format)
    tls_private_key = libervia-key.pem
    ; if true (or 1), HTTP will redirect to HTTPS
    redirect_to_https = 1
    ; passphrase for libervia profile
    passphrase = something_secure
    ; here we redirect main libervia page
    ; to the blog of a profile named "some_profile"
    url_redirections_dict = {
      "/": "/u/some_profile"
      }
