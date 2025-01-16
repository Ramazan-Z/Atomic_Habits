FROM nginx:latest

RUN mkdir -p /var/www/html/static
RUN mkdir -p /var/www/html/media

COPY /nginx.conf /etc/nginx/nginx.conf
COPY /proxy_params /etc/nginx/proxy_params

EXPOSE 80