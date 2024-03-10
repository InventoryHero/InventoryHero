FROM node:lts-alpine as frontend-build
RUN mkdir -p /app
WORKDIR /app
COPY frontend/ ./
RUN npm install && \
        npm run build


FROM python:3.11-alpine as release
LABEL authors="codewizards"
WORKDIR /var/www/html
RUN  mkdir -p /backend && \
    mkdir -p /var/log/docker && \
    mkdir -p /var/www/html

COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/default.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-build /app/dist /var/www/html


WORKDIR /app/inventoryhero/backend
ENV PYTHONPATH="/app/inventoryhero:${PYTHONPATH}"
COPY backend/requirements.txt requirements.txt
RUN apk update 
RUN apk add --no-cache --virtual build-deps gcc musl-dev pkgconf mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev && \
    apk add --no-cache nginx && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

ENV PUID 1000
ENV PGID 1000
ENV IS_DEVELOPMENT false

VOLUME [ "/app/inventoryhero/data" ]
COPY /docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
COPY backend .

EXPOSE 80
RUN chmod +x /entrypoint.sh
RUN chown nginx:nginx /var/www/html 

