FROM node:lts-alpine as frontend-build
RUN mkdir -p /app
WORKDIR /app
COPY frontend/ ./
RUN npm install && \
        npm run build


FROM python:3.11-alpine as release
LABEL authors="codewizards"
WORKDIR /var/www/html
RUN  mkdir -p /app && \
    mkdir -p /var/log/docker && \
    mkdir -p /var/www/html

COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/default.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-build /app/dist /var/www/html


WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN apk update 
RUN apk add --no-cache --virtual build-deps gcc musl-dev pkgconf mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev && \
    apk add --no-cache nginx && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

ENV PUID 1000
ENV PGID 1000
ENV IS_DEVELOPMENT false


COPY /docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
COPY backend /app

EXPOSE 80
RUN chmod +x /entrypoint.sh
RUN chown nginx:nginx /var/www/html 


FROM python:3.11-alpine as dev
LABEL authors="codewizards"

COPY --from=frontend-build /app/dist /var/www/html

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN apk update 
RUN apk add --no-cache --virtual build-deps gcc musl-dev pkgconf mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev && \
    apk add --no-cache nginx && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

ENV PUID 1000
ENV PGID 1000


COPY /docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
COPY backend /app

EXPOSE 5000
EXPOSE 80

RUN chmod +x /entrypoint.sh
RUN chown nginx:nginx /var/www/html 