FROM python:3.12-slim AS runner

WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends g++ libpq-dev librabbitmq4 libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt --no-cache-dir && \
    apt-get purge -y --auto-remove g++

COPY backend gunicorn.conf.py /app/backend/

EXPOSE 8000

RUN chmod +x /app/backend/entrypoint.sh

RUN python /app/backend/manage.py collectstatic --noinput

FROM runner AS development

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]

FROM runner AS production

LABEL org.opencontainers.image.source=https://github.com/aliaflore/licenta
LABEL org.opencontainers.image.description="Licenta"
LABEL org.opencontainers.image.licenses=MIT

ARG user=django
ARG group=django
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group} && \
    useradd -u ${uid} -g ${group} -s /bin/sh -m ${user} && \
    chown -R ${uid}:${gid} /app

USER ${uid}:${gid}

ENV DJANGO_SETTINGS_MODULE=backend.settings

WORKDIR /app/backend
ENTRYPOINT [ "/app/backend/entrypoint.sh" ]

FROM node:latest AS frontend

WORKDIR /app/frontend
ENV HOST=0.0.0.0
ENV PORT=3000
ENV PROTOCOL_HEADER=x-forwarded-proto
ENV HOST_HEADER=x-forwarded-host

COPY frontend /app/frontend

RUN npm install
RUN npm run build

WORKDIR /app/frontend/build

CMD ["node", "index.js"]

FROM ubuntu:22.04 as nginxbuilder

RUN apt update \
    && apt upgrade -y \
    && apt install -y libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev wget git gcc make libbrotli-dev

WORKDIR /app
RUN wget https://nginx.org/download/nginx-1.25.3.tar.gz && tar -zxf nginx-1.25.3.tar.gz
RUN git clone https://github.com/google/ngx_brotli && cd ngx_brotli && git submodule update --init --recursive && cd ..
RUN cd nginx-1.25.3 && ./configure --with-compat --add-dynamic-module=../ngx_brotli \
    && make modules

FROM nginx:1.25.3 as nginx

COPY --from=nginxbuilder /app/nginx-1.25.3/objs/ngx_http_brotli_static_module.so /etc/nginx/modules/
COPY --from=nginxbuilder /app/nginx-1.25.3/objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/
RUN echo "load_module modules/ngx_http_brotli_filter_module.so;\nload_module modules/ngx_http_brotli_static_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf
RUN echo 'brotli on;\n \
    brotli_comp_level 6;\n \
    brotli_static on;\n \
    brotli_types application/atom+xml application/javascript application/json application/rss+xml\n \
            application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype\n \
            application/x-font-ttf application/x-javascript application/xhtml+xml application/xml\n \
            font/eot font/opentype font/otf font/truetype image/svg+xml image/vnd.microsoft.icon\n \
            image/x-icon image/x-win-bitmap text/css text/javascript text/plain text/xml;' > /etc/nginx/conf.d/brotli.conf

COPY nginx.conf /etc/nginx/conf.d/svelte.conf.template

RUN rm /etc/nginx/conf.d/default.conf

CMD cat /etc/nginx/conf.d/svelte.conf.template | envsubst '$UPSTREAM_BACKEND' | envsubst '$UPSTREAM_FRONTEND' | tee /etc/nginx/conf.d/svelte.conf && \
    exec nginx -g 'daemon off;'