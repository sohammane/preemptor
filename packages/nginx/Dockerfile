FROM nginx:1.17.4-alpine

ARG env_conf=nginx_prod.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY $env_conf /etc/nginx/nginx.conf
COPY fullchain.pem /etc/nginx/fullchain.pem
COPY privkey.pem /etc/nginx/privkey.pem