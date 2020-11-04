FROM python:3.6

WORKDIR /
ADD src/ /src/

RUN apt-get update
RUN apt-get install -y wget supervisor vim

# Install python packages
RUN pip3 install --no-cache-dir -r /src/requirements.txt

# Install gsutil
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

ADD key.json /src/
RUN gcloud auth activate-service-account --key-file=/src/key.json

ADD supervisor/conf.d/api/supervisord.conf /etc/supervisor/conf.d/api/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/api/supervisord.conf"]
