from cgitb import lookup
from tabnanny import verbose
from django_filters import rest_framework as filters
from clients.models import Subscription
from service.models import Video, UserVideoRelation
import os



class VideosFilter(filters.FilterSet):
    liked_by_user = filters.BooleanFilter(method="filter_liked_by_user")
    tags = filters.CharFilter(method="filter_tags")
    #subs_by_user = filters.BooleanFilter(method="filter_subs_by_user")

    class Meta:
        model = Video
        fields = ["tags", "liked_by_user"]

    def filter_tags(self, queryset, name, value):
        tags = value.split(",")
        return queryset.filter(tags__tag_name__in=tags)


    def filter_liked_by_user(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.all(
                user_video_relations__user=user,
                user_video_relations__vote=UserVideoRelation.LIKE,
            )    

        else:
            return queryset.filter(
                user_video_relations__user=user,
                user_video_relations__vote=UserVideoRelation.DISLIKE,
            )
        return queryset

    # def filter_subs_by_user(self, queryset, name, value):
    #     user = self.request.user

    #     if not user.is_authenticated or not value:
    #         return queryset

    #     subscribed_channels = Subscription.objects.filter(subscriber=user).values_list(
    #         "channel", flat=True
    #     )
    #     return queryset.filter(author__id__in=subscribed_channels)


