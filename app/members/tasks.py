from config.celery import app


__all__ = (
    'send_sms',
)

@app.task()
def send_sms(contact_phone, auth_key):
    import requests
    from config.settings.production import secrets

    BLUEHOUSELAB_SMS_API_ID = secrets['BLUEHOUSELAB_SMS_API_ID']
    BLUEHOUSELAB_SMS_API_KEY = secrets['BLUEHOUSELAB_SMS_API_KEY']
    BLUEHOUSELAB_SENDER = secrets['BLUEHOUSELAB_SENDER']
    receiver = contact_phone.replace('-', '')
    content = f'[배민찬COPY] 인증번호는 {auth_key}입니다.'

    requests.post(
        'https://api.bluehouselab.com/smscenter/v1.0/sendsms',
        auth=requests.auth.HTTPBasicAuth(
            BLUEHOUSELAB_SMS_API_ID,
            BLUEHOUSELAB_SMS_API_KEY,
        ),
        headers={
            'Content-Type': 'application/json; charset=utf-8',
        },
        json={
            'sender': BLUEHOUSELAB_SENDER,
            'receivers': [receiver],
            'content': content,
        }
    )
