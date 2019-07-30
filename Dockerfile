# source: https://hub.docker.com/_/python
FROM python:3.7.3-alpine3.9

COPY requirements.txt requirements.txt

# psycopg2 source: https://hub.docker.com/r/svlentink/psycopg2/dockerfile
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc g++ && \
    # install the dependencies required during runtime
    apk add --no-cache libpq && \
    # install the actual python packages
    pip3 install -r requirements.txt && \
    # cleanup the build dependencies
    apk del --purge .build-deps && \
    rm -vrf /var/cache/apk/* && \
    # check what is installed
    pip3 list

# Copy the application
COPY . /app

# Create a non-root user
RUN adduser -D dummyuser && \
    chown dummyuser /app

WORKDIR app
USER dummyuser

CMD ["python3", "app.py", "weather"]
