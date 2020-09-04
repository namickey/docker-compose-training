FROM python:3.6

ARG pdir=/projects/

ADD src/requirements.txt $pdir

WORKDIR $pdir

RUN pip install -r requirements.txt

