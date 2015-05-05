FROM conda3

# create a conda env for weapontool
RUN conda create -n dev bottle -y

# copy to /opt
COPY poboys_conda_package_server /opt/poboys_conda_package_server
RUN chown -R root:root /opt/poboys_conda_package_server
WORKDIR /opt/poboys_conda_package_server

# run 
EXPOSE 6969
CMD ["/bin/bash", "start_from_docker.sh"]
