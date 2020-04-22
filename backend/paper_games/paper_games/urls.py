"""Корневая конфигурация маршрутизации для HTTP-запросов.

Examples:
    Для авторизации используется библиотека djoser.
    \n Доступные конечные точки для api/auth/ :
    \n /users/
    \n /users/me/
    \n /users/confirm/
    \n /users/resend_activation/
    \n /users/set_password/
    \n /users/reset_password/
    \n /users/reset_password_confirm/
    \n /users/set_username/
    \n /users/reset_username/
    \n /users/reset_username_confirm/
    \n /token/login/ (Token Based Authentication)
    \n /token/logout/ (Token Based Authentication)

Подробнее: https://djoser.readthedocs.io/en/latest/getting_started.html
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('admin/',      admin.site.urls),
    path('api/auth/',   include('djoser.urls')),
    path('api/auth/',   include('djoser.urls.authtoken')),
    path('api/',        include('virus_war.urls')),
]
