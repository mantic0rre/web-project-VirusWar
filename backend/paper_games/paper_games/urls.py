from django.contrib import admin
from django.urls import path
from django.conf.urls import include


""" Available endpoints for api/auth/
/users/
/users/me/
/users/confirm/
/users/resend_activation/
/users/set_password/
/users/reset_password/
/users/reset_password_confirm/
/users/set_username/
/users/reset_username/
/users/reset_username_confirm/
/token/login/ (Token Based Authentication)
/token/logout/ (Token Based Authentication)
"""

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('api/auth/',   include('djoser.urls')),
    path('api/auth/',   include('djoser.urls.authtoken')),
    path('api/',        include('virus_war.urls')),
]
