
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

RUN rm requirements-docker.txt && \
    grep -v design_rsa image_crypt/__init__.py > .tmp && \
    cat .tmp > image_crypt/__init__.py && rm .tmp && \
    pip install --no-deps . && \
    install -Dm755 image-crypt /usr/bin/image-crypt
