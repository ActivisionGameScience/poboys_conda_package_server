==============================
 Poboy's Conda Package Server
==============================

This is a repository for conda packages.  It is a "poor-man's" version of
Anaconda Server + Onsite Binstar, but only for small groups that are sitting behind a firewall
and don't worry about authentication.  Upload and delete packages at will!

You can start it like this::

    cd poboys_conda_package_server/
    python poboy_conda_package_server.py --port 6969

Then you can browse to the url and have a look::

    http://your.hostname:6969

In order for ``conda`` to see it, add the following line to your ``.condarc``::

    - http://your.hostname:6969/pkgs
