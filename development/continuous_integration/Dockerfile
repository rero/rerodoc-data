FROM python:3.5-slim

LABEL maintainer="software@rero.ch"
LABEL description="RERO DOC data model by RERO."



RUN apt-get update && apt-get install -y git curl

RUN pip install -U setuptools pip &&\
    pip install -U virtualenv

#Add rerodoc-data sources to `code` and work there:
WORKDIR  /rerodoc/rerodoc/src
COPY build_app.sh /rerodoc/build_app.sh

# Run container as user `invenio` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' invenio && \
     chown -R invenio:invenio /rerodoc && \
     chmod 755 /rerodoc/build_app.sh

USER invenio

SHELL ["/bin/bash", "-c"]
WORKDIR /rerodoc
RUN virtualenv rerodoc

ARG GIT_COMMIT

RUN /rerodoc/build_app.sh $GIT_COMMIT

CMD  /rerodoc/rerodoc/src/rerodoc-data/development/continuous_integration/test.sh
