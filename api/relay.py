import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post, User 

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        # fields = ['title', 'con']

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        #3
        interfaces = (graphene.relay.Node, )


class RelayQuery(graphene.ObjectType):
    #4
    relay_link = graphene.relay.Node.Field(PostNode)
    #5
    relay_links = DjangoFilterConnectionField(PostNode, filterset_class=PostFilter)