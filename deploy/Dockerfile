FROM node:lts-alpine
RUN apk add --update nginx && \
    mkdir -p /tmp/nginx/vue-single-page-app && \
    mkdir -p /var/log/nginx && \
    mkdir -p /var/www/html

COPY ./deploy/nginx.conf /etc/nginx/nginx.conf
COPY ./deploy/default.conf /etc/nginx/conf.d/default.conf
COPY ./deploy/nginx-selfsigned.crt /etc/ssl/private/nginx-selfsigned.crt
COPY ./deploy/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key

WORKDIR /tmp/nginx/vue-single-page-app
COPY . .
RUN npm install && \
    npm run build && \
    cp -r dist/* /var/www/html && \
    chown nginx:nginx /var/www/html
CMD ["nginx", "-g", "daemon off;"]