==============================
 Poboy's Conda Package Server
==============================

This is a server that acts as a repository for conda packages.  It is a "poor-man's" version of
Anaconda Server + Onsite Binstar, but only for small groups that are sitting behind a firewall
and don't worry about authentication.  Upload and delete packages at will!

You must have ``conda`` and ``bottle`` installed (and in your path).

You can start it like this::

    cd poboys_conda_package_server/
    python poboy_conda_package_server.py --port 6969

Then you can browse to the url and have a look::

    http://your.hostname:6969

For ``conda`` to see it, add the following line to your ``.condarc``::

    - http://your.hostname:6969/pkgs


Docker instructions
===================

From where you cloned it is easy to build a ``docker`` image::

    sudo docker build -t poboys_conda_package_server .

Then it is easy to launch it (and persist the data on the host)::

    sudo docker run -d --name poboys_conda_package_server -v /data/dir/on/host:/opt/poboys_conda_package_server poboys_conda_package_server


License
=======

All files are licensed under the BSD 3-Clause License as follows:
 
| Copyright (c) 2015, Activision Publishing, Inc.  
| All rights reserved.
| 
| Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
| 
| 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
|  
| 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
|  
| 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
|  
| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

