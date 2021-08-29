### Build and install packages
FROM python:3.9 as build-python

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /home/backend/
COPY requirements.txt /home/backend/
RUN pip install -r requirements.txt

### Final image
FROM python:3.9-slim

RUN groupadd -r backend && useradd -r -g backend backend

RUN apt-get update \
  && apt-get install -y \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  liblcms2-2 \
  libopenjp2-7 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libssl1.1 \
  libtiff5 \
  libwebp6 \
  libxml2 \
  libpq5 \
  shared-mime-info \
  mime-support \
  gdal-bin \
  libgdal-dev \
  python3-gdal \
  binutils \
  libproj-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

COPY . /home/backend/
WORKDIR /home/backend/

ENV PYTHONUNBUFFERED 1

CMD "gunicorn" "backend.asgi" "-c" "gunicorn.conf" "-k" "uvicorn.workers.UvicornWorker"
