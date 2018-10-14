from rest_framework import viewsets
from myapp.serializers import PersonSerializer
from myapp.serializers import TestSerializer
from myapp.models import Person
from myapp.models import Test

class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer

class TestViewSet(viewsets.ModelViewSet):
	queryset = Test.objects.all()
	serializer_class = TestSerializer
