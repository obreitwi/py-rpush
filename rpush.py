#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2013 Oliver Breitwieser
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
Usage:
    rpush [--config <cfg> ] list
    rpush [--config <cfg> ] clean (all|<num> ...)
    rpush [--config <cfg> ] [--push] (<file> | --alias <file_in> <file_out>) ...
    rpush -h | --help

Options:
    -h --help       Show this screen.
    --version       Show version.

    --push          Force pushing of whatever follows

    <file>          File to push to remote

    -a --alias      Indicate that the file should be renamed at remote site
    <file_in>       Input file (local)
    <file_out>      Filename of the pushed file on the server
    list            List all remote files.
    clean           Clean all remote files

    --config <cfg>  Specify config file to read. [default: ~/.rpushrc]

"""

from __future__ import print_function

__version__ = "0.1.1"

import os
import sys
import subprocess as sp

import random
import string

import itertools

import logging
logging.basicConfig(
        format='%(asctime)s | %(funcName)s: %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level = logging.INFO)

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser

# much inspiration taken from:
# http://code.activestate.com/recipes/576810-copy-files-over-ssh-using-paramiko/

from docopt import docopt

def random_string(
        size=24,
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return "".join([random.choice(chars) for i in range(size)])


class RPushHandler(object):
    def __init__(self, args):
        self.args = args
        self.extra_handling()

        cfg = configparser.ConfigParser()
        cfg.read( os.path.expanduser(self.args[ "--config" ]))

        self.ssh_args = "ssh -x".split()

        section = "RPush"
        self.host       = cfg.get(section, "host")
        self.basefolder = cfg.get(section, "folder")
        self.url        = cfg.get(section, "url")
        self.www_group  = cfg.get(section, "www-group")

        self.ssh_args.append(self.host)

        if self.args["list"]:
            self.cmd_list()

        elif self.args["clean"]:
            self.cmd_clean()

        else:
            self.cmd_push()


    def extra_handling(self):
        if not self.args["--push"] and "clean" in self.args[ "<file>" ]:
            print("Please specify all or the filenumber you want to clean.")
            print("If you want to push file \"clean\" please specify push.")
            sys.exit(1)

    def cmd_push(self):
        for f_in, f_out in itertools.chain(zip(self.args[ "<file>" ], self.args[ "<file>" ]),
                                zip(self.args[ "<file_in>" ], self.args[ "<file_out>" ])):
            rfolder = random_string()
            self.run_ssh_command("mkdir "+ rfolder)
            path = "{0}/{1}".format(rfolder, os.path.basename( f_out ))
            self.run_scp_command(f_in, path)
            self.run_ssh_command("chown :{1} {0} && chmod g+r {0}".format( path, self.www_group ))

            print( "{0}/{1}".format(self.url, path))


    def cmd_list(self):
        # for i,f in enumerate(self.list_complete_directory()):
        for i,f in enumerate(self.get_complete_remote_content()):
            print("[{0}]\t{1}\t{2}/{1}".format(i, f, self.url))


    def cmd_clean(self):
        complete_content = self.get_complete_remote_content()

        if not self.args[ "all" ]:
            to_delete = [complete_content[int(i)] for i in set(self.args["<num>"])]
        else:
            to_delete = complete_content

        for path in to_delete:
            self.remove_remote(path)


    def remove_remote(self, path):
        folder, file = path.split("/")

        self.run_ssh_command("rm " + path)
        self.run_ssh_command("rmdir " + folder)


    def run_ssh_command(self, command):
        logging.debug(command)
        proc = sp.Popen(self.ssh_args + ["cd {0} && ".format(self.basefolder) + command],
                stdout = sp.PIPE, stderr = sp.PIPE)
        rc = proc.wait()
        contents, warnings = proc.communicate()

        if rc != 0:
            logging.warn(warnings)

        return contents

    def run_scp_command(self, path_from, path_to):
        logging.debug( "SCP: {0} -> {1}".format(path_from, path_to))
        proc = sp.Popen(["scp", path_from, "{0}:{1}/{2}".format(self.host, self.basefolder, path_to)],
                stdout = sp.PIPE, stderr = sp.PIPE)
        rc = proc.wait()
        contents, warnings = proc.communicate()

        if rc != 0:
            logging.warn(warnings)

        return contents


    def get_complete_remote_content(self):
        return self.list_directory("*/*")


    def list_directory(self, path):
        contents = self.run_ssh_command("ls -rt {0}".format(path))

        if sys.version_info >= (3, 0):
            contents = contents.decode()

        contents = [line for line in contents.split("\n") if len(line) > 0]
        logging.debug(contents)
        return contents


if __name__ == "__main__":
    random.seed()
    arguments = docopt(__doc__, version=__version__)
    # print(arguments)
    RPushHandler(arguments)


