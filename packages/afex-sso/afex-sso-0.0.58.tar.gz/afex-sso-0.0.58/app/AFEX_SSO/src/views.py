import base64

from django.conf import settings as app_settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.views import View
from .get_hash_key import get_hash_key
from .sso import SSO


sso = SSO()
sso_url = app_settings.SSO_URL
UserModel = get_user_model()



class AdminLoginView(View):

    def get(self, request, *kwargs):
        request_url = base64.b64encode(
            request.build_absolute_uri().encode('utf-8')
        ).decode('utf-8')
        if 'q' in request.GET.keys() or request.session.get('state'):
            ses_id = request.GET.get('q') or request.session.get('state')
            if not request.session.get('state'):
                request.session['state'] = ses_id
            validate_sso = sso.check_credentials(session_key=ses_id)
            try:
                response_data = validate_sso['data']
            except:
                return redirect(f"{sso_url}?qz={request_url}")

            user_data = response_data.get('user')
            if user_data.get('email') and not UserModel.objects.filter(email=user_data.get('email')).exists():
                user = UserModel.objects.create(
                    email=user_data.get('email'),
                    username=user_data.get('email'),
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                )
            else:
                user = UserModel.objects.get(email=user_data.get('email'))

            if not user.is_staff:
                user.is_staff = True
                user.save()
            login(request, user)

            return redirect("admin:index")

        elif 'ec' in request.GET.keys() or 'next' in request.GET.keys():
            return redirect(f"/?ec={request.GET.get('ec')}")
        return redirect(f"{sso_url}?qz={request_url}")