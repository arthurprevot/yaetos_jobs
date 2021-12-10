FROM docker.io/bitnami/spark:3.1.2
USER root

# Pip installs. Using local copy to tmp dir to allow checkpointing this step (no re-installs as long as requirements.txt doesn't change)
COPY conf/requirements_alt.txt /tmp/requirements.txt
WORKDIR /tmp/
RUN apt-get update && apt-get install -y git
RUN pip3 install -r requirements.txt
# TODO: remove above since it should install as dependencies of "pip3 install yaetos"
RUN pip3 install yaetos==0.9.2

# RUN mkdir -p tmp/files_to_ship/  # skipped, causes problems with permissions, whether run from root or jovyan user. Will need to be run manually once.
# ENV SPARK_HOME /usr/local/spark # already set in base docker image
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH

# Expose ports for monitoring.
# SparkContext web UI on 4040 -- only available for the duration of the application.
# Spark master’s web UI on 8080.
# Spark worker web UI on 8081.
EXPOSE 4040 8080 8081

CMD ["/bin/bash"]

# Usage: docker run -it -p 4040:4040 -p 8080:8080 -p 8081:8081 -v ~/.aws:/root/.aws -h spark <image_id>
# or update launch_env.sh and execute it.
