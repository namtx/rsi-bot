FROM amd64/python:3
MAINTAINER "namtx.93@gmail.com"

WORKDIR /home

ARG PORT

COPY ta-lib-0.4.0-src.tar.gz .
RUN tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && ./configure \
    && make \
    && make install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ta-lib

COPY . .

ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

EXPOSE $PORT

CMD [ "python", "./run.py" ]
