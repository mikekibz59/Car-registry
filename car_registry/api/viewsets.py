"""Car registry api viewset """

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from car_registry.models import (
    Car, CarModel, CarMake, CarSubModel)
from .serializers import (
    CarSerializer, CarModelSerializer, CarMakeSerializer,
    CarSubModelSerializer
)


class CarRegistryViewSet(viewsets.ViewSet):
    """Car registry api endpoints declarations """

    @action(methods=['GET'], detail=False)
    def get_car_makes(self, request) -> Response:
        """ endpoint to return all car makes """

        return self.__get_object_helper(CarMake, CarMakeSerializer)

    @action(methods=['GET'], detail=False)
    def get_car_models(self, request) -> Response:
        """endpoint to return all car models """

        return self.__get_object_helper(CarModel, CarModelSerializer)

    @action(methods=['GET'], detail=False)
    def get_car_submodels(self, request):
        """ endpoint to return all car submodel """

        return self.__get_object_helper(CarSubModel, CarSubModelSerializer)

    @action(methods=['GET'], detail=False)
    def get_all_cars_in_range(self, request):
        """ Endpoint to query car with a certain price and mileage rage """

        start_mileage = request.query_params.get('start_mileage', 0)
        max_mileage = request.query_params.get('last_mileage', 50000)
        start_price = request.query_params.get('start_price', 0)
        max_price = request.query_params.get('max_price', 1_000_000)
        name = request.query_params.get('name', str())
        car_qs = Car.objects.filter(
            price__range=[float(start_price), float(max_price)],
            mileage__range=[float(start_mileage), float(max_mileage)],
            make__name__icontains=name)\
            .order_by('-updated_at')
        json_res = CarSerializer(car_qs, many=True)
        return Response(json_res.data, status=status.HTTP_200_OK)


    def __get_object_helper(self, obj, serializer):
        """Helper Method to query all objects and serialize it """

        obj_qs = obj.objects.all()
        serialized_obj = serializer(obj_qs, many=True)
        return Response(serialized_obj.data, status=status.HTTP_200_OK)
