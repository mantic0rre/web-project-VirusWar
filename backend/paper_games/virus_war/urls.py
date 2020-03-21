from django.urls import path
from virus_war.views import *


urlpatterns = [
    path('users/',                         UserList.as_view()),
    path('users/<int:pk>/',                UserRetrieve.as_view()),
]