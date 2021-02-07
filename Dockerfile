# pull official base image
FROM python:3.6.9-alpine as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the vika_app user
RUN mkdir -p /home/vika_app

# create the vika_app user
RUN addgroup -S vika_app && adduser -S vika_app -G vika_app

# create the appropriate directories
ENV HOME=/home/vika_app
ENV APP_HOME=/home/vika_app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update \
    && apk add  \
    build-base \
    python3-dev \
    openssl \
    git \
    bash \
    sudo \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    postgresql-dev \
    gcc \
    python3-dev \ 
    musl-dev \
    libpq \
    libxml2-dev \
    libxslt-dev \
    ffmpeg \
    imagemagick


RUN pip install --upgrade pip

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

RUN chown -R vika_app:vika_app $APP_HOME

RUN pip install -r requirements.txt --no-cache-dir
# chown all the files to the vika_app user


# change to the vika_app user
USER vika_app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/vika_app/web/entrypoint.sh"]