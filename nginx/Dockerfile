FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf && rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d
COPY proxy.conf /etc/nginx
COPY nginx_root.conf /etc/nginx/nginx.conf

