.. _primitivus-documentation:

==========
Primitivus
==========

``Primitivus`` is the TUI (Terminal User Interface) frontend of Libervia

Overview
========

``Primitivus`` is a text based frontend. It is specially adapted for systems without
graphical environments (e.g. servers), for low bandwidth remote shells (e.g. ssh) or for
people who like straightforward interfaces without distracting images or animations.

For the moment, Primitivus implements one 2 one chat, group chat (also called *MUC* for
Multi-Users Chat), and some related features (end 2 end encryption, bookmarks, gateways
interaction, file sending, etc.).

Usage
=====

Primitivus is modal (vi-like), one can switch from one mode to another
in the same way as in vi/vim:

-  From any mode, press ``[Esc]`` to switch to normal mode.
-  From normal mode, press ``:`` to switch to command mode.
-  From normal mode, press ``i`` to switch to insert mode – the one you
   use to write messages to your contacts.

Primitivus can be handled either with the mouse, in a very intuitive way, or with the
keyboard. Below, the keyboard shortcuts are explained.

Keyboard handling
-----------------

- ``+`` means that 2 keys must be pressed at the same time. Example: ``CTRL + N`` means that
   you must press Control key and ``N`` at the same time
- ``,`` means that a key must be pressed after the previous combination. Example:
  ``CTRL + F, M`` means that you must press control key and ``F`` at the same time, release
  them, then press ``M``
- keys with ``SHIFT`` also work without ``SHIFT`` if ``[CapsLock]`` is set.

Main keys
~~~~~~~~~

``[Tab]`` and/or ``CTRL + up/down arrows``
  change focus
``CTRL + X``
  quit Primitivus
``CTRL + F, 1`` or ``CTRL + F, M``
  focus on the menu
``CTRL + F, 2`` or ``CTRL + F, B``
  focus on the roster or the chat window
``CTRL + F, 3`` or ``CTRL + F, E``
  focus on the edition line
``ALT + M``
  display/hide the menu
``CTRL + N``
  show the next notification
``CTRL + S``
  hide/redisplay a pop-up window temporarily
``CTRL + D``
  enter debug mode (development versions only)
``F2``
  hide/display the roster
``CTRL + L``
  refresh the screen

Chat rooms
~~~~~~~~~~

To use those keyboard shortcuts, your cursor must be in a chat room.

``ALT + J``
  join a chat room
``ALT + P``
  hide/display the list of participants
``ALT + T``
  hide/display timestamps
``ALT + N``
  use/don't use short nicks
``ALT + L``
  hide/display frame decorations
``ALT + S``
  change the room's topic appearance by switching between:
    - one single line (the topic is cut if it's too long)
    - the full topic
    - topic hidden
``SHIFT + G``
  go to the end (bottom) of your history (note that this is UPPERCASE ``G``)


Edition line
~~~~~~~~~~~~

``CTRL + A`` or ``[Home]``
  move the cursor at the beginning of the line
``CTRL + E`` or ``[End]``
  move the cursor at the end of the line
``CTRL + K``
  erase the line, starting at the cursor's position
``CTRL + W``
  erase the last word
``S + [Tab]``
  invoke completion (dependent on the context)
``up/down arrows``
  browse sent messages history

Contacts
~~~~~~~~

``ALT + D``
  hide/display offline contacts
``ALT + S``
  hide/display contacts' status messages

Card game
~~~~~~~~~

``[space]``
  select a card

Commands
~~~~~~~~

The following commands must be typed in command mode (type ``[Esc]`` to switch to normal
mode, then the ``:`` at the beginning of the command will switch to command mode).

``:quit``
  quit Primitivus
``:messages``
  display log messages (see also the logging configuration)

..
  FIXME: :presence and :status are currently disabled in Primitivus
  ``:presence [status]``
    set your presence status. Invoked without argument, a pop-up will allow you to choose your presence status; otherwise, you can use the following arguments:
    - ``online``
    - ``chat`` (free to chat)
    - ``away`` (away from keyboard)
    - ``dnd`` (do not disturb)
    - ``xa`` (extended away)
  ``:status [message]``
    set your status message. Invoked without argument, a pop-up will allow you to enter a message.

``:history <size>``
  set the number of lines of history to display in the chat window (``:history 0`` to clear the window)
``:search <filter>``
  do a full text search in this conversation/room. The room will be cleared an only
  messages corresponding to ``<filter>`` will be show. Use ``:history <size>`` to
  restore normal history

