FROM python:3.8-slim-buster

ARG OS_IMAGE_DIR=/images/release
ARG IMAGE_OUTPUT_DIR=/images/custom
#ARG VERSION
#ARG RELEASE

RUN mkdir -p ${OS_IMAGE_DIR}
RUN mkdir -p ${IMAGE_OUTPUT_DIR}
RUN mkdir -p /workspace

COPY ./entrypoint.sh /workspace/
RUN chmod a+x /workspace/entrypoint.sh

WORKDIR /workspace
RUN pip3 install rpios-tools

ARG VERSION
ENV raspios_version=${VERSION}

ARG RELEASE
ENV raspios_release=${VERSION}

ENV image_dir=${OS_IMAGE_DIR}
ENV output_dir=${IMAGE_OUTPUT_DIR}

ENTRYPOINT "./entrypoint.sh" ${version} ${release} ${image_dir} ${output_dir}

