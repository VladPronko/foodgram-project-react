from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
# from django_filters import rest_framework as filters
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Follow
from .serializers import (CustomUserSerializer, FollowSerializer,
                          ShowFollowsSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,
            methods=["GET"],
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        user_obj = User.objects.filter(following__user=request.user)
        # user_obj = User.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = ShowFollowsSerializer(
            result_page, many=True, context={'current_user': request.user})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=["POST", "DELETE"],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'user': request.user.id, 'author': id}
        )
        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=request.user, author__id=id)
        follow.delete()
        return Response(f'{request.user} отписался от {follow.author}',
                        status=status.HTTP_204_NO_CONTENT)

