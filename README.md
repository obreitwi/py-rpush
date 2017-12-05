# RPush

`rpush` is a little tool I wrote to automatically copy files to a remote server
folder that is accessible via web. The folder is configured to only allow access
when the user knows the precise filename.

For each file, `rpush` creates a new folder with a random name and displays the
URL under which the file is accessible.

The URL can then be send to others and only those can access the file.

    Usage:
        rpush [-v] [--config <cfg>] [-H <host>] [-u] list [<num> ...]
        rpush [-v] [--config <cfg>] [-H <host>] clean (all|<num> ...)
        rpush [-v] [--config <cfg>] [-H <host>] [--push] (<file> | --alias <file_in> <file_out>) ...
        rpush [-v] --help

    Options:
        --config <cfg>  Specify config file to read. [default: ~/.config/rpushrc]

        --push          Force pushing of whatever follows

        --version       Show version.

        -H <host>       Host to use.

        -a --alias      Indicate that the file should be renamed at remote site
        <file_in>       Input file (local)
        <file_out>      Filename of the pushed file on the server

        -h --help       Show this screen.

        -u --url-only   Only list the remote URLs (useful for copying).

        -v --verbose    Enable verbose output

        <file>          File to push to remote

        clean           Clean specfic (i.e., indices returned by list) / all remote
                        files

        list            List all remote files.
