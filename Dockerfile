FROM        bluemeta/baeminchan:base
MAINTAINER  yeojin.dev@gmail.com

ENV         BUILD_MODE              production
ENV         DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}
ENV         PROJECT_DIR              /srv/backend

RUN         mkdir /var/log/django

COPY        .                       ${PROJECT_DIR}
WORKDIR     ${PROJECT_DIR}

# Front-end
RUN         mv -f /srv/node_modules/    /srv/backend/front/

RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx.conf           /etc/nginx
RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx_app.conf       /etc/nginx/sites-available

RUN         rm -f /etc/nginx/sites-enabled/*
RUN         ln -fs /etc/nginx/sites-available/nginx_app.conf                    /etc/nginx/sites-enabled

RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/supervisor_app.conf  /etc/supervisor/conf.d

EXPOSE      7000

CMD         supervisord -n
