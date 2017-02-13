# build a container
#  docker build --rm=true -t parsenip . 

# start disposable container
# docker run --rm -itd -p 80:80 --name parsenip parsenip /bin/bash

# Start Prod container
# docker run -itd -p 80:80 --name parsenip parsenip /bin/bash

FROM php:7.0-apache
RUN apt-get -y update
RUN apt-get install -y git nano wget

ADD index.html /var/www/html/index.html
ADD scripts/ /var/www/html/scripts
ADD styles/ /var/www/html/styles

EXPOSE 80
