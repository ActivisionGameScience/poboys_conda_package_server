==============================
 Poboy's Conda Package Server
==============================

This is a server that acts as a repository for conda packages.  It is a "poor-man's" replacement
for Anaconda Server.  Only small groups behind a firewall should feel comfortable using this.
There is no authentication, nor logging.  Anybody can upload and delete packages!

The server requires ``conda`` and ``bottle`` to run.

After cloning, you can start the server like this::

    cd src
    python poboys_conda_package_server.py --port 6969

Optionally, you can have it sync with an s3 bucket (this assumes that you have ``boto3`` installed)::

    python poboys_conda_package_server.py --port 6969 --s3_bucket <YOURBUCKET>

(You should set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars for this to work).

It has a simple web interface - browse to the appropriate url and have a look::

    http://your.hostname:6969

In order for a client to recognize it, add the following line to its ``.condarc``::

    - http://your.hostname:6969/pkgs


Docker instructions
===================

First create a docker image for ``poboys_conda_package_server``::

    sudo docker build -t poboys_conda_package_server .

and launch it (the ``-v`` is there to persist the data on the host)::

    sudo docker run -d --name poboys_conda_package_server -p 6969:6969 -v /data/dir/on/host:/opt/poboys_conda_package_server poboys_conda_package_server

If you want to specify a different port or an S3 bucket then you can modify the ``Dockerfile`` before building to add the following env vars::

    POBOYS_PORT=6969
    POBOYS_S3_BUCKET=<YOURBUCKET>


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

