""" CarRegistry Serializer file"""

from rest_framework.serializers import ModelSerializer
from car_registry.models import (
    Car, CarModel, CarMake, CarSubModel)


class CarSerializer(ModelSerializer):
    """ Car Model Serializer """

    class Meta:
        """ CarSerializer META DATA """
        model = Car
        fields = '__all__'


class CarModelSerializer(ModelSerializer):
    """ CarModel Serializer """

    class Meta:
        """ CarModelSerializer META DATA """
        model = CarModel
        fields = '__all__'


class CarMakeSerializer(ModelSerializer):
    """ CarMake Serializer class  """

    class Meta:
        """ CarMakeSerializer META DATA"""
        model = CarMake
        fields = '__all__'


class CarSubModelSerializer(ModelSerializer):
    """ CarSubModel Serializer class """

    class Meta:
        """CarSubModelSerializer META DATA"""

        model = CarSubModel
        fields = '__all__'
