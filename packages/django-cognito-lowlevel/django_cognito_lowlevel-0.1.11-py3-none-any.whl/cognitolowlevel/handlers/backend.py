import requests
import base64
import json
import time
import colorama
import sys
from django.conf import settings
from jose import jwk, jwt
from jose.utils import base64url_decode
from django.utils.functional import cached_property
from django.core.cache import cache

# Check if all the settings are ready


def setting_check():
    sample_settings = '''COGNITO_USER_POOL_ID = "eu-west-2XXXXXXXXXXXXXXXXXX"
COGNITO_CLIENT_ID = "XXXXXXXXXXXXXXXXXX"
COGNITO_APP_CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
COGNITO_TOKEN_URL = "https://XXXXXXXXXXXX.auth.XXXXXXXXXXXX.amazoncognito.com/oauth2/token"
COGNIT_CALLBACK_URL_PATH = "cognitosaml/api/cognito/userpool/callback/"
COGNITO_REDIRECT_URL = f"http://localhost:8000/{COGNIT_CALLBACK_URL_PATH}"
COGNITO_HOST = "XXXXXXXXXXXX.auth.eu-west-2.amazoncognito.com"
COGNITO_USERPOOL_REGION = "XXXXXXXXXXXX"
COGNITO_AUTH_SUCCESS_REDIRECT_URL = "landing:index"
COGNITO_AUTH_ERROR_REDIRECT_URL = "landing:index"
    '''
    has_missing_settings = False
    for field in ["COGNITO_USER_POOL_ID", "COGNITO_CLIENT_ID", "COGNITO_APP_CLIENT_SECRET", "COGNITO_TOKEN_URL",
                  "COGNIT_CALLBACK_URL_PATH", "COGNITO_REDIRECT_URL", "COGNITO_HOST", "COGNITO_USERPOOL_REGION"]:
        if not hasattr(settings, field):
            print(f"{colorama.Fore.GREEN}cognitolowlevel:{colorama.Style.RESET_ALL} setting is missing field: {colorama.Fore.RED}{field}{colorama.Style.RESET_ALL}")
            has_missing_settings = True
    if has_missing_settings:
        print(
            f"\n\n{colorama.Fore.RED}Here is a sample settings that you can tweak:{colorama.Style.RESET_ALL}")
        print(sample_settings)
        sys.exit()


setting_check()

COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID
COGNITO_CLIENT_ID = settings.COGNITO_CLIENT_ID
COGNITO_APP_CLIENT_SECRET = settings.COGNITO_APP_CLIENT_SECRET
COGNITO_TOKEN_URL = settings.COGNITO_TOKEN_URL
COGNITO_REDIRECT_URL = settings.COGNITO_REDIRECT_URL
COGNITO_HOST = settings.COGNITO_HOST
COGNITO_USERPOOL_REGION = settings.COGNITO_USERPOOL_REGION


class CognitoAuthenticator:
    def __init__(self):
        self._get_public_key_if_needed()

    def _get_json_not_so_secret_keys(self):
        # print(f"{colorama.Fore.RED}_get_json_not_so_secret_keys(){colorama.Style.RESET_ALL}")
        keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(COGNITO_USERPOOL_REGION,
                                                                                          COGNITO_USER_POOL_ID)

        r = requests.get(keys_url)
        if r.status_code == 200:
            return r.json()['keys']
        else:
            return None

    def _get_public_key_if_needed(self):
        cache_data = cache.get("cache_key")

        if not cache_data:
            # print(f"{colorama.Fore.RED}not cached!{colorama.Style.RESET_ALL}")

            cache_data = self._get_json_not_so_secret_keys()
            timeout = getattr(
                settings, "COGNITO_PUBLIC_KEYS_CACHE_TIMEOUT", 300)
            cache.set("cache_key", cache_data, timeout=timeout)
        # else:
        #    print(f"{colorama.Fore.RED}Already cached!{colorama.Style.RESET_ALL}")

        return cache_data

    def verify_token(self, token, is_access_token=False):

        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']

        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self._get_public_key_if_needed())):
            if kid == self._get_public_key_if_needed()[i]['kid']:
                key_index = i
                break
        if key_index == -1:
            if settings.DEBUG:
                print('Public key not found in jwks.json')
            return False

        # construct the public key
        public_key = jwk.construct(self._get_public_key_if_needed()[key_index])
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit('.', 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            if settings.DEBUG:
                print('\nSignature verification failed')
            return False

        if settings.DEBUG:
            print(
                f'\n{colorama.Fore.GREEN}Signature successfully verified{colorama.Style.RESET_ALL}')
        # since we passed the verification, we can now safely
        # use the unverified claims
        claims = jwt.get_unverified_claims(token)
        # additionally we can verify the token expiration
        if time.time() > claims['exp']:
            if settings.DEBUG:
                print('Token is expired')
            return False
        # and the Audience  (use claims['client_id'] if verifying an access token)
        if is_access_token:
            if claims['client_id'] != COGNITO_CLIENT_ID:
                if settings.DEBUG:
                    print(
                        f'\n{colorama.Fore.YELLOW}Token was not issued for this audience{colorama.Style.RESET_ALL}')
                return False
        elif claims['aud'] != COGNITO_CLIENT_ID:
            if settings.DEBUG:
                print(
                    f'\n{colorama.Fore.RED}Token was not issued for this audience{colorama.Style.RESET_ALL}')
            return False
        # now we can use the claims
        if settings.DEBUG:
            print(
                f'\n{colorama.Fore.GREEN}Claims: {colorama.Fore.RED}{claims}{colorama.Style.RESET_ALL}')
        return claims

    @cached_property
    def authentication_url(self):
        return f"https://{COGNITO_HOST}/login?redirect_uri={COGNITO_REDIRECT_URL}&response_type=code&client_id={COGNITO_CLIENT_ID}"

    def authenticate_user_with_code(self, code):
        client_id_client_secret = "%s:%s" % (
            COGNITO_CLIENT_ID, COGNITO_APP_CLIENT_SECRET)
        headers = {
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(client_id_client_secret.encode()).decode()
        }
        data = {
            'grant_type': 'authorization_code',
            'client_id': COGNITO_CLIENT_ID,
            'code': code,
            'redirect_uri': COGNITO_REDIRECT_URL
        }
        r = requests.post(COGNITO_TOKEN_URL, data=data, headers=headers)
        if r.status_code == 200:
            results = r.json()

            access_token = results["access_token"]
            id_token = results["id_token"]

            # access_token_payload = jwt.get_unverified_claims(access_token)
            # id_token_payload = jwt.get_unverified_claims(id_token)

            # username = access_token_payload['username']  # The user name of the authenticated user
            # sub = access_token_payload['sub']  # The UUID of the authenticated user

            access_token_verified = self.verify_token(
                access_token, is_access_token=True)
            id_token_verified = self.verify_token(id_token)

            if settings.DEBUG:
                print(
                    f"\n{colorama.Fore.GREEN}access_token_verified:\n{colorama.Fore.RED}{access_token_verified}{colorama.Style.RESET_ALL}")
                print(
                    f"\n{colorama.Fore.GREEN}id_token_verified:\n{colorama.Fore.RED} {id_token_verified}{colorama.Style.RESET_ALL}")

            return id_token_verified
        else:
            return None
