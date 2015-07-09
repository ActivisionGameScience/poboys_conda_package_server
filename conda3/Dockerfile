FROM phusion/baseimage
MAINTAINER Justin Shacklette "Justin.Shacklette@activision.com"

# conda needs wget & bzip2
RUN apt-get update && \
  apt-get install wget bzip2 -y && \
  rm -rf /var/lib/apt/lists/*

# grab miniconda and setup root env in /opt/anaconda
RUN wget -O miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-3.10.1-Linux-x86_64.sh && \
    /bin/bash /miniconda.sh -b -p /opt/anaconda && \
    rm miniconda.sh

# put the root env on the path
RUN echo "export PATH=/opt/anaconda/bin:$PATH" > /etc/profile.d/conda.sh
ENV PATH /opt/anaconda/bin:$PATH

# update the root env and install some key packages
RUN conda update --all -y
RUN conda install jinja2 conda-build binstar -y

# copy licenses
COPY license_accelerate.txt  /root/.continuum/license_accelerate.txt
COPY license_iopro.txt /root/.continuum/license_iopro.txt

# create bash aliases
RUN echo "alias lst='ls -lAsp'\nalias dev='source activate dev'" > /root/.bash_aliases

# create the condarc
RUN echo "channels:\n  - ActivisionGameScience\n  - defaults" > /root/.condarc
