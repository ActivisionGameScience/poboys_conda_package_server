FROM conda3

# create a conda env 
RUN conda create -n dev bottle -y

# copy to /opt
COPY src /opt/poboys_staging
RUN chown -R root:root /opt/poboys_staging
WORKDIR /opt/poboys_staging

# run 
EXPOSE 6969
CMD ["/bin/bash", "start_from_docker.sh"]
