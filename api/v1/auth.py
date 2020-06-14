from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

auth = HTTPTokenAuth(scheme='JWT')
serializer = Serializer("740125zaq`", expires_in=60000)


@auth.verify_token
def verify_token(token):
    try:
        data = serializer.loads(token)
        print(data)
    except Exception as e:
        print(e)
        return False
    if 'username' in data:
        return True
    return False
