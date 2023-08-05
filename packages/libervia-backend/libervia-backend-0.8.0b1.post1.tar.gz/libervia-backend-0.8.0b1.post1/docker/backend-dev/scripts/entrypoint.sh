#!/bin/sh

eval $(dbus-launch --sh-syntax)

# default, backend is launched in foreground
if [ $# -eq 0 ]
then
	exec libervia-backend fg
fi

# backend is launched with an explicit subcommand
if [ $1 = fg -o $1 = bg -o $1 = debug -o $1 = stop -o $1 = status ]
then
	exec libervia-backend "$@"
fi

# a whole command is specified
libervia-backend bg
exec "$@"
