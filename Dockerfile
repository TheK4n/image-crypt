
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

RUN rm requirements-docker.txt && \
    chmod o+x image-crypt && \
    ln -s $(pwd)/image-crypt /usr/local/bin/image-crypt
