from rest_framework import serializers
from news.models import News
from orar.models import Rand
from personalise.models import Personalise, Board, Cards
from resources.models import Resources


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('news_id', 'title', 'body', 'author_name', 'category', 'source')


class PersonaliseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Personalise
        fields = ('id', 'url', 'navbar_color', 'background_first', 'background_second', 'color1_first', 'color1_second',
                  'color2_first', 'color2_second', 'font_color', 'font_family', 'boards', 'classes', )


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'url', 'year', 'subject', 'teacher', 'description')


class CardsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cards
        fields = ('id', 'url', 'personalise', 'personalise_id', 'type', 'x', 'y', 'width', 'height')


class ResourcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resources
        fields = ('id', 'url', 'resources_id', 'title', 'url', 'content')


class OrarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rand
        fields = ('id', 'url', 'curs', 'zi', 'ora_inceput', 'ora_sfarsit', 'grupa', 'tip', 'sala', 'profesor', 'pachet', )

