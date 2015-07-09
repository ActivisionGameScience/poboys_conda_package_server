==============================
 Poboy's Conda Package Server
==============================

This is a server that acts as a repository for conda packages.  It is a "poor-man's" version of
Anaconda Server.  Only use it if you are a small group sitting behind a firewall.
There is no authentication, nor logging.  Anybody can upload and delete packages!

The server requires ``conda`` and ``bottle`` to run.

After cloning, you can start the server like this::

    cd poboys_conda_package_server/src
    python poboys_conda_package_server.py --port 6969

It has a simple web interface - browse to the appropriate url and have a look::

    http://your.hostname:6969

In order for a client to recognize it, add the following line to its ``.condarc``::

    - http://your.hostname:6969/pkgs


Docker instructions
===================

First, we need to create a barebones docker image that contains ``conda``.  From
where you cloned this repository run::

    cd conda3
    vim Dockerfile   <-- make changes as necessary to match your system
    sudo docker build -t conda3 .
    cd ..
    
Now create a derived docker image for ``poboys_conda_package_server``::

    sudo docker build -t poboys_conda_package_server .

and launch it (and persist the data on the host)::

    sudo docker run -d --name poboys_conda_package_server -p 6969:6969 -v /data/dir/on/host:/opt/poboys_conda_package_server poboys_conda_package_server


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

