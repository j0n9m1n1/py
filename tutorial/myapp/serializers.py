from myapp.models import Person
from myapp.models import Test
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name')
        
class TestSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Test
		fields = ('id', 'pw')