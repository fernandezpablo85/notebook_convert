FROM ubuntu:bionic

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    pandoc \
    texlive-xetex \
    texlive-full \
    texlive-latex-extra \
    texlive-generic-extra \
    virtualenv && \
    apt-get clean

RUN virtualenv /venv -ppython3 && /venv/bin/pip install nbconvert pygit2
ENV PATH=/venv/bin:$PATH

COPY nb_lib /venv/lib/python3.6/site-packages/nb_lib
