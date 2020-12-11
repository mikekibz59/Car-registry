"""Car registry api viewset """

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from car_registry.lib import (handle_error,
                              validate_post_car_params,
                              validate_query_params)
from car_registry.models import (
    Car, CarModel, CarMake, CarSubModel)
from .serializers import (
    CarSerializer, CarModelSerializer, CarMakeSerializer,
    CarSubModelSerializer
)


class CarRegistryViewSet(viewsets.ViewSet):
    """Car registry api endpoints declarations """

    @handle_error
    @action(methods=['GET'], detail=False)
    def get_car_makes(self, request) -> Response:
        """ endpoint to return all car makes """

        return self.__get_object_helper(CarMake, CarMakeSerializer)

    @handle_error
    @action(methods=['GET'], detail=False)
    def get_car_models(self, request) -> Response:
        """endpoint to return all car models """

        return self.__get_object_helper(CarModel, CarModelSerializer)

    @handle_error
    @action(methods=['GET'], detail=False)
    def get_car_submodels(self, request):
        """ endpoint to return all car submodel """

        return self.__get_object_helper(CarSubModel, CarSubModelSerializer)

    @handle_error
    @action(methods=['GET'], detail=False)
    def get_all_cars_in_range(self, request):
        """ Endpoint to query car with a certain price and mileage rage """

        validate_query_params(request.query_params)

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

    @handle_error
    @action(methods=['GET'], detail=False)
    def get_all_cars_on_parent(self, request):
        """
            Endpoint to query car with a baesed on make, model and submodel
        """

        make_name = request.query_params.get('make_name', None)
        model_name = request.query_params.get('model_name', None)
        submodel_name = request.query_params.get('submodel_name', None)

        car_qs = Car.objects.filter(
            model__name=model_name,
            submodel__name=submodel_name,
            make__name=make_name)
        json_res = CarSerializer(car_qs, many=True)
        return Response(json_res.data, status=status.HTTP_200_OK)

    @handle_error
    @action(methods=['POST'], detail=False)
    def create_car(self, request):
        """ Endpoint to handle car creation """

        post_params = request.data
        validate_post_car_params(post_params)
        car = Car.objects.create(**post_params)
        json_res = CarSerializer(car)
        return Response(json_res.data, status=status.HTTP_201_CREATED)

    def __get_object_helper(self, obj, serializer):
        """Helper Method to query all objects and serialize it """

        obj_qs = obj.objects.all()
        serialized_obj = serializer(obj_qs, many=True)
        return Response(serialized_obj.data, status=status.HTTP_200_OK)
