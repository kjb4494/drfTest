from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
# from testapp.serializers import UserSerializer, GroupSerializer
from testapp.serializers import CmbUserSerializer
from testapp.models import CmbUser


# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     http_method_names = ['get', 'post', 'put', 'delete']
#     permission_classes = [permissions.AllowAny]
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     http_method_names = ['get']
#     permission_classes = [permissions.AllowAny]

class CmbUserViewSet(viewsets.ModelViewSet):
    queryset = CmbUser.objects.all().order_by('-reg_date')
    serializer_class = CmbUserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [permissions.AllowAny]
