from django.contrib.auth.models import User, Group
from testapp.models import CmbUser
from rest_framework import serializers


# Java DTO 역할을 하는 직렬화 클래스
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         # url 필드는 상세페이지 링크를 출력해준다.
#         fields = ['url', 'username', 'email']

# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=200)
#     email = serializers.EmailField()
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#         return instance
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class CmbUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=63)
    country = serializers.CharField(max_length=63)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CmbUser.objects.create(**validated_data)

