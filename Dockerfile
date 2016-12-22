# docker build -t tyghe/biopython .

FROM continuumio/miniconda

RUN apt-get install -y gcc
RUN pip install git+https://github.com/biopython/biopython.git
