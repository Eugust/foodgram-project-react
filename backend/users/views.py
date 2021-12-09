from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UserSerializer, SignUpSerializer, SetPasswordSerializer
from .models import User
from recipes.models import Follow
from api.serializers import FollowSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny,]

    @action(methods=['get'], detail=False, url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='set_password', url_name='set_password')
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=self.request.data)
        new_password = self.request.data.get('new_password')
        current_password = self.request.data.get('current_password')
        if serializer.is_valid():
            user = get_object_or_404(User, pk=self.request.user.id)
            user.password = new_password
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False,
            url_path='subscriptions', url_name='subscriptions')
    def subscriptions(self, request, *args, **kwargs):
        '''
        subs = Follow.objects.filter(user=self.request.user)
        for sub in subs:
            serializer = UserSerializer(sub.following)
        return Response(serializer.data, status=status.HTTP_200_OK)
        '''
        sub = get_object_or_404(Follow, user=self.request.user)
        serializer = UserSerializer(sub.following, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        '''
        '''

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/subscribe')
    def subscribe(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        following = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'GET':
            subscribe_serializer = FollowSerializer(data={'user': user.id, 'following': following.id})
            subscribe_serializer.is_valid(raise_exception=True)
            subscribe_serializer.save()
            serializer = UserSerializer(following, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            subscribe = get_object_or_404(Follow, user=user)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    password = request.data.get('password')
    if serializer.is_valid():
        user = get_object_or_404(User, email=email)
        if user:
            token = AccessToken.for_user(user)
            return Response({'auth_token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
