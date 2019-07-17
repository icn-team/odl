FROM ubuntu:18.04

WORKDIR /hicn
ENV ODL_VERSION=opendaylight-0.9.2.zip
ENV ODL_URL=https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/opendaylight/0.9.2/${ODL_VERSION}

# Use bash shell
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y curl
RUN curl -OL ${ODL_URL} &&  apt-get install unzip &&  unzip ${ODL_VERSION} && rm -r ${ODL_VERSION}
RUN apt-get update && apt-get install openjdk-8-jre -y

RUN sed -i 's|exec "${KARAF_HOME}/bin/karaf" server "$@" >> "${KARAF_REDIRECT}" 2>\&1 &|exec "${KARAF_HOME}/bin/karaf" server "$@" >> "${KARAF_REDIRECT}" 2>\&1|' \
    /hicn/opendaylight-0.9.2/bin/start

WORKDIR /hicn

COPY init.sh .
