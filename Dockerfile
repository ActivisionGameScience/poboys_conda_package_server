FROM phusion/baseimage

# Need wget and ca-certificates to grab miniconda
# Conda itself needs bzip2
RUN apt-get update && apt-get -y install wget bzip2 ca-certificates

# grab miniconda and setup root env in /opt/anaconda
RUN wget -O miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/sh miniconda.sh -b -p /opt/anaconda && \
    rm miniconda.sh

# put the root env on the path
ENV PATH /opt/anaconda/bin:$PATH

# create the condarc
RUN echo "channels:\n  - ActivisionGameScience\n  - defaults" > /root/.condarc#

# update the root env and install some key packages
# then create a conda env
RUN conda update --all -y && \
    conda install jinja2 conda-build -y && \
    conda create -n poboys_env python=3.6 -y && \
    /bin/bash -c "source activate poboys_env && pip install bottle boto3 awscli"

# copy to /opt
COPY src /opt/poboys_staging
RUN chown -R root:root /opt/poboys_staging
WORKDIR /opt/poboys_staging

# run 
EXPOSE 6969
CMD ["/bin/bash", "start_from_docker.sh"]
