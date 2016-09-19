#!/bin/sh

DIR=$(dirname $(readlink -f $0))

ln -sv $DIR/rpush.py ~/.local/bin/rpush
ln -sv $DIR/rpushrc  ~/.config/rpushrc

