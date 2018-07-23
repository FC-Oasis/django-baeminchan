# baeminchan-django

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

#### Dev

- ipython
- Django-Extensions
- awsebcli

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
  "AWS_STORAGE_BUCKET_NAME": "<Your Bucket name>"
}
```

## Running

```shell
# Move project's directory
pipenv install
pipenv shell
./runlocal.sh
```

## Deploying
```shell
# Move project's directory
./deploy.sh
```
