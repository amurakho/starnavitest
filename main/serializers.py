from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, user_logged_in

from main import models


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = models.Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class AnalyticsByDaySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    date = serializers.DateField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user_logged_in.send(sender=self.user.__class__, request=self.context['request'], user=self.user)
        return data
