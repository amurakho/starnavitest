from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action, api_view
from datetime import datetime, timedelta

from main import serializers, models


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        obj = self.get_object()
        created, _ = obj.like_manage(request.user)

        message = 'Liked' if created else 'Unliked'
        return Response(data=message)

    @action(methods=['GET'], detail=True)
    def get_likes(self, request, *args, **kwargs):
        obj = self.get_object()
        likes = obj.get_all_likes()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_likes_by_period(request, *args, **kwargs):
    date_from = datetime.strptime(request.GET.get('date_from'), '%Y-%m-%d')
    date_to = datetime.strptime(request.GET.get('date_to'), '%Y-%m-%d')

    likes = models.Like.objects.filter(date__lt=date_to, date__gt=date_from)
    # split by date
    delta = date_to - date_from
    # each day add to date_from, try to get all likes by this day and count it
    data = []
    for day in range(delta.days + 1):
        day = date_from + timedelta(days=day)
        likes_per_day = likes.filter(date__exact=day.date())
        if likes_per_day:
            d = {
                'date': datetime.date(day),
                'count': len(likes_per_day),
            }
            data.append(d)
    serializer = serializers.AnalyticsByDaySerializer(data, many=True)
    return Response(serializer.data)
