"""Права доступа для API.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешить для запросов GET, HEAD или OPTIONS.
    Для остальных запросов проверка на владельца комнаты.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешить для запросов GET, HEAD или OPTIONS.
    Для остальных запросов проверка на пользователя.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user