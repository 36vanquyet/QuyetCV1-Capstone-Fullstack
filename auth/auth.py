import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'quyetcv1.us.auth0.com')
ALGORITHMS = os.getenv('ALGORITHMS', ['RS256'])
API_AUDIENCE = os.getenv('API_AUDIENCE', 'http://localhost:5000')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    '''
    Get the header from the request.

    Argument:
        None
        
    Return:
        The token part of the header.

    Raises:
        AuthError 401: If no header is present
        AuthError 401: If the header is malformed
        AuthError 401: If the Token is not found in the header
        AuthError 401: If the header is not bearer token
    '''
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError(
            error={
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
            },
            status_code=401
        )

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError(
            error={
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
            },
            status_code=401
        )

    elif len(parts) == 1:
        raise AuthError(
            error={
            'code': 'invalid_header',
            'description': 'Token not found.'
            },
            status_code=401
        )

    elif len(parts) > 2:
        raise AuthError(
            error={
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
            },
            status_code=401
        )

    token = parts[1]
    return token

def check_permissions(permission, payload):
    '''
    Check if the payload contains the permission.

    Argument:
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload.

    Return:
        True otherwise.

    Raises:
        AuthError 400: If the permission is not in the payload
        AuthError 403: If the permission is not found in the payload
    '''
    if 'permissions' not in payload:
        raise AuthError(
            error={
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
            }, 
            status_code=400
        )

    if permission not in payload['permissions']:
        raise AuthError(
            error={
            'code': 'unauthorized',
            'description': 'Permission not found.'
            },
            status_code=403
        )

    return True

def verify_decode_jwt(token):
    '''
    Verify and decode the JWT.

    Argument:
        token: JWT token

    Return
        The decoded payload.

    Raises:
        AuthError 401: If the token is expired
        AuthError 401: If the token is invalid
        AuthError 401: If the token is malformed
        AuthError 400: If the token is not found
        AuthError 403: If the key is not found
    '''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            error={
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
            },
            status_code=401
        )

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token=token,
                key=rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                error={
                'code': 'token_expired',
                'description': 'Token expired.'
                }, 
                status_code=401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                error={
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 
                status_code=401
            )
        except Exception:
            raise AuthError(
                error={
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
                },
                status_code=400
            )
    raise AuthError(
        error={
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        },
        status_code=403
    )

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator