`rpush` is a little tool I wrote to automatically copy files to a remote server
folder that is accessible via web. The folder is configured to only allow access
when the user knows the precise filename.

For each file, `rpush` creates a new folder with a random name and displays the
URL under which the file is accessible.

The URL can then be send to others and only those can access the file.


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

