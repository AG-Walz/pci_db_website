FROM nginx:1.23.1

RUN rm /etc/nginx/conf.d/default.conf
COPY conf.d/nginx.conf /etc/nginx/conf.d

COPY nginx.conf /etc/nginx/nginx.conf