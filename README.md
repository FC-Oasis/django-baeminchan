# baeminchan-django [![Build Status](https://www.travis-ci.org/FC-Oasis/baeminchan-django.svg?branch=master)](https://www.travis-ci.org/FC-Oasis/baeminchan-django)

## Requirements

#### Product

- Python (3.6)
- pipenv
- Django (2.x)
- psycopg2-binary
- pillow
- django-storages
- boto3
- uwsgi
- djangorestframework
- requests
- raven
- django-cors-headers

#### Dev

- ipython
- Django-Extensions
- awsebcli
- pygraphviz
- beautifulsoup4
- lxml

### Secrets

#### `.secrets/base.json`

```json
{
  "SECRET_KEY": "<Django secret key>"
}
```

#### `.secrets/production.json`

```json
{
  "ALLOWED_HOSTS": ["<Your list>"],
  "DATABASES": {
    "default": {
      "ENGINE": "<DB engine like django.db.backends.postgresql>",
      "HOST": "<DB host>",
      "PORT": "<DB port>",
      "USER": "<DB user>",
      "PASSWORD": "<DB pw>",
      "NAME": "<DB name>"
    }
  },
  "AWS_ACCESS_KEY_ID": "<Your AWS ACCESS KEY ID>",
  "AWS_SECRET_ACCESS_KEY": "<Your AWS SECRET ACCESS KEY>",
  "AWS_DEFAULT_ACL": "private",
  "AWS_S3_REGION_NAME": "<Your region like ap-northeast-2>",
  "AWS_S3_SIGNATURE_VERSION": "s3v4",
  "AWS_STORAGE_BUCKET_NAME": "<Your Bucket name>",
  
  "KAKAO_REST_API_KEY": "<Your KAKAO REST API KEY>",
  "SENTRY_DSN": "<Your SENTRY DSN>",
  "BLUEHOUSELAB_SMS_API_ID": "<Your BLUEHOUSELAB API ID>",
  "BLUEHOUSELAB_SMS_API_KEY": "<Your BLUEHOUSELAB API KEY>",
  "BLUEHOUSELAB_SENDER": "<Phone number for sender>",
  "AWS_ELASTI_CACHE": "<Your ElastiCache Endpoint>"
}
```

## Running

#### Local

```shell
# Move project's directory
pipenv install
pipenv shell
./runlocal.sh
```

#### Production

```shell
# Move project's directory
pipenv install
pipenv shell
./runproduction.sh
```

## Deploying

```shell
# Move project's directory
./deploy.sh
```

## Logging

```shell
# Move project's directory
./eblog.sh
```
