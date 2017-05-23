FROM python:3.6-alpine
#curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt
ENV KUBE_VERSION=v1.6.4

RUN adduser -h /home/bundle -D bundle
ENV BUNDLE_NAME=kubectl
ENV BUNDLE_DIR=/home/bundle/$BUNDLE_NAME/

COPY setup.py requirements.txt $BUNDLE_DIR
WORKDIR $BUNDLE_DIR

# install bundle dependencies
# (provides a chaching layer with dependencies)
RUN set -ex \
  && apk add --no-cache git curl ca-certificates \
  && pip install -r requirements.txt \
  && curl -Lo /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl \
  && chmod +x /usr/local/bin/kubectl \
  && apk del git

# Copy and install bundle code
COPY $BUNDLE_NAME/ $BUNDLE_DIR/$BUNDLE_NAME/
# add support for separate sub commands
COPY bin/ $BUNDLE_DIR/bin/
RUN set -ex \
  && pip install . \
  && mkdir -p /etc/kube/
