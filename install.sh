#!/bin/sh

# very basic install script

DIR=$(dirname $(readlink -f $0))

ln -sfv $DIR/rpush.py ~/.local/bin/rpush
ln -sfv $DIR/rpushrc  ~/.config/rpushrc

