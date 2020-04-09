from personalise import models
from api.serializers import PersonaliseSerializer
from rest_framework import generics

class PersonaliseList(generics.ListAPIView):
    serializer_class = PersonaliseSerializer

    def get_queryset(self):
        pass