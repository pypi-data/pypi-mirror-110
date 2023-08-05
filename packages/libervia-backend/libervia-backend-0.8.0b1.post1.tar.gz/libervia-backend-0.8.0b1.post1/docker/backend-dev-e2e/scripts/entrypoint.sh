#!/bin/sh

eval $(dbus-launch --sh-syntax)

nohup /usr/bin/Xtigervnc -geometry 1024x768 -desktop "Libervia e2e test" -rfbport 5900 -SecurityTypes None :0 &
nohup openbox &
exec libervia-backend fg
