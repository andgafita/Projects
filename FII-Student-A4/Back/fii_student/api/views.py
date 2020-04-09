from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-inserted_time')
    serializer_class = NewsSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('news_id', 'title', 'body', 'author_name', 'category', 'source', )


class PersonaliseViewSet(viewsets.ModelViewSet):
    queryset = Personalise.objects.all()
    serializer_class = PersonaliseSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'navbar_color', 'background_first', 'background_second', 'color1_first', 'color1_second',
                        'color2_first', 'color2_second', 'font_color', 'font_family', 'boards', 'classes', )


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'year', 'subject', 'teacher', 'description', )


class CardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'personalise', 'personalise_id', 'type', 'x', 'y', 'width', 'height', )


class ResourcesViewSet(viewsets.ModelViewSet):
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'resources_id', 'title', 'url', 'content', )


class OrarViewSet(viewsets.ModelViewSet):
    queryset = Rand.objects.all()
    serializer_class = OrarSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'curs', 'zi', 'ora_inceput', 'ora_sfarsit', 'grupa', 'tip', 'sala', 'profesor', 'pachet', )

