from django.urls import path
from virus_war.views import *


urlpatterns = [
    path('users/',                         UserList.as_view()),
    path('users/<int:pk>/',                UserRetrieve.as_view()),
    path('rooms/',                         RoomListCreate.as_view()),
    path('rooms/<int:pk>/',                RoomRetrieveUpdateDestroy.as_view()),
    path('starred/',                       StarredCreate.as_view()),
    path('starred/<int:room_id>/',         StarredDestroy.as_view()),
]