import jwt
import time
from django.http import HttpRequest, JsonResponse


SALT = '123'
#   identity是str


def msg2token(num, identity):
    source = {
        'id': num,
        'identity': identity,
        'exp': time.time() + 60 * 60
    }
    token = jwt.encode(source, SALT, algorithm='HS256')
    return token


def token2msg(token):
    return jwt.decode(token, SALT, algorithms='HS256')
    try:
        source = jwt.decode(token, SALT, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return -2
    except jwt.DecodeError:
        return -1
    return source


'''
def expire(exp):
    #   jwt过期
    return exp < time.time()
'''


def get_token(request: HttpRequest):
    if 'token' in request.headers:
        print('yes')
        return request.headers.get('token')
    else:
        #   return status : -1
        return None


def check_token(*args):
    legal_identity = args

    #   试一下
    def check_token_(func):
        def wrapper(arg: HttpRequest):
            assert isinstance(arg, HttpRequest)
            token = get_token(arg)
            print(token)
            try:
                msg = token2msg(token)
                print(msg)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'status': -2})
            except jwt.DecodeError:
                print(-1)
                return JsonResponse({'status': -1})

            print(legal_identity)
            if msg['identity'] in legal_identity:
                return func(arg)
            else:
                return JsonResponse({'status': -3})
        return wrapper
    return check_token_
