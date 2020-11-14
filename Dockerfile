FROM python:3.8-slim-buster
RUN apt-get update && apt upgrade -y && apt-get install sudo -y

RUN apt-get install -y\
    coreutils \
    bash \
    nodejs \
    bzip2 \
    curl \
    figlet \
    gcc \
    g++ \
    git \
    #aria2 \
    #util-linux \
    libevent-dev \
    libjpeg-dev \
    libffi-dev \
    libpq-dev \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    musl \
    neofetch \
    libcurl4-openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-server-dev-all \
    #chromedriver \
    openssl \
    pv \
    jq \
    wget \
    python3 \
    python3-dev \
    python3-pip \
    libreadline-dev \
    #metasploit-framework \
    #apktool \
    #openjdk-13-jdk \
    #zipalign \
    sqlite \
    ffmpeg \
    libsqlite3-dev \
    chromium \
    zlib1g-dev \
    recoverjpeg \
    zip \
    megatools \
    libfreetype6-dev




RUN pip3 install --upgrade pip setuptools 
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi 
RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi 
RUN rm -r /root/.cache
RUN git clone https://github.com/Team-Indus/IndusUserbot /root/indus
RUN mkdir /root/indus/bin/
WORKDIR /root/indus/
RUN chmod +x /usr/local/bin/*
RUN pip3 install -r requirements.txt
CMD ["python3","-m","indus"]
