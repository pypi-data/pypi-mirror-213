from django.shortcuts import render, redirect
import colorama, pprint

from cognitolowlevel.handlers.backend import CognitoAuthenticator
from django.conf import settings

def cognito_callback(request):
    code = request.GET.get("code", None)

    if code:
        print(f"{colorama.Fore.GREEN}Code is: {colorama.Fore.RED}{code}{colorama.Style.RESET_ALL}")
        c = CognitoAuthenticator().authenticate_user_with_code(code)

        if c:
            if settings.DEBUG:
                print(f"\n{colorama.Fore.GREEN}call back payload:{colorama.Style.RESET_ALL}")
                pp = pprint.PrettyPrinter(depth=4)
                pp.pprint(c)

            email = c["email"]
            if settings.DEBUG:
                print(f"\n{colorama.Fore.GREEN}email:{colorama.Fore.RED}", email, colorama.Fore.RESET)

            cognito_username = c["cognito:username"]
            if settings.DEBUG:
                print(f"\n{colorama.Fore.GREEN}cognito:username:{colorama.Fore.RED}", cognito_username, colorama.Fore.RESET)

            if "family_name" in c:
                first_name = c["family_name"]
                if settings.DEBUG:
                    print(f"\n{colorama.Fore.GREEN}family name:{colorama.Fore.RED}", first_name, colorama.Fore.RESET)

            if "given_name" in c:
                given_name = c["given_name"]
                if settings.DEBUG:
                    print(f"\n{colorama.Fore.GREEN}given name:{colorama.Fore.RED}", given_name, colorama.Fore.RESET)

            sub = c["sub"]                  # Identifies the subject of the JWT.
            if settings.DEBUG:
                print(f"\n{colorama.Fore.GREEN}sub:{colorama.Fore.RED}", sub, colorama.Fore.RESET)

            return redirect( settings.COGNITO_AUTH_SUCCESS_REDIRECT_URL )

    return redirect(settings.COGNITO_AUTH_ERROR_REDIRECT_URL)
