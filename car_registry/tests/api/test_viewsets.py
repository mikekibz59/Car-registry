""" Test file for CarRegistryViewset """

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from mixer.backend.django import mixer
from car_registry.models import CarMake, CarModel, CarSubModel, Car


class TestCarRegistryViewSet(APITestCase):
    """CarRegistryViewSet Test Cases """

    def setUp(self):
        """Test class Initialization """
        self.make = mixer.blend(CarMake, name='Toyota', id='toyota')
        self.model = mixer.blend(CarModel, id='mark-x', name='Toyota',
                                 make=self.make)
        self.submodel = mixer.blend(CarSubModel, id='mark-x-3', name='mark x',
                                    model=self.model)
        self.car = Car.objects.create(make=self.make,
                                      model=self.model, submodel=self.submodel,
                                      year=2020, mileage=1200,
                                      body_type='convertible',
                                      transmission='Manual', fuel_type='Petrol',
                                      exterior_color='White',
                                      price=1000)
        self.client = APIClient()

    def test_get_make(self):
        """ return all makes"""
        path = '/api/car_registry/get_makes'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_models(self):
        """ return all models """
        path = '/api/car_registry/get_models'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_submodels(self):
        """ returns all submodels"""
        path = '/api/car_registry/get_submodels'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_car_query_range(self):
        """ return a car from param queries"""
        path = '/api/car_registry/car_price_mileage_range?start_mileage=100&max_mileage=1200&start_price=100&max_price=1500'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['model'], 'mark-x')

    def test_car_query_not_in_range(self):
        """ return an empty object"""
        path = '/api/car_registry/car_price_mileage_range?start_mileage=10000&max_mileage=12000&start_price=10000&max_price=1500000'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), list())

    def test_car_query_without_range_params(self):
        """
            it should return all cars with a price range of
            0 to 1_000_000 and a mileage range of between
            0 and 50_0000
        """
        path = '/api/car_registry/car_price_mileage_range'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['model'], 'mark-x')

    def test_car_query_without_range_params_but_name_provided(self):
        """
            it should return all cars with a make of toyota
        """
        path = '/api/car_registry/car_price_mileage_range?name=toyota'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['make'], 'toyota')
