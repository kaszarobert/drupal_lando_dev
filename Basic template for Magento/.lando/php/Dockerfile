FROM devwithlando/php:8.1-apache-4
RUN apt-get update -y && \
    apt-get install -y libxslt1-dev && \
    docker-php-ext-install xsl && \
    apt-get remove -y libxslt1-dev icu-devtools libicu-dev libxml2-dev && \
    rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install sockets