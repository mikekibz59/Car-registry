""" Test file for CarRegistryViewset """

import pytest
from rest_framework.test import APIClient, APITestCase
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework import status
from mixer.backend.django import mixer
from car_registry.models import CarMake, CarModel, CarSubModel, Car


class TestCarRegistryViewSet(APITestCase):
    """CarRegistryViewSet Test Cases """

    def setUp(self):
        """Test class Initialization """
        self.make = mixer.blend(CarMake, name='Toyota', id='toyota')
        self.bmw_make = mixer.blend(CarMake, name='BMW', id='bmw')
        self.model = mixer.blend(CarModel, id='mark-x', name='Toyota',
                                 make=self.make)
        self.model2 = mixer.blend(CarModel, id='Prado', name='Toyota',
                                  make=self.make)
        self.bmw_model = mixer.blend(CarModel, id='BMW', name='BMW',
                                     make=self.bmw_make)
        self.submodel = mixer.blend(CarSubModel, id='mark-x-3', name='mark x',
                                    model=self.model)
        self.bmw_submodel = mixer.blend(CarSubModel, id='x6', name='bmw x6',
                                        model=self.bmw_model)
        self.car = Car.objects.create(make=self.make,
                                      model=self.model, submodel=self.submodel,
                                      year=2020, mileage=1200,
                                      body_type='convertible',
                                      transmission='Manual', fuel_type='Petrol',
                                      exterior_color='White',
                                      price=1_000)
        self.car2 = Car.objects.create(make=self.make,
                                       model=self.model2, submodel=self.submodel,
                                       year=2010, mileage=12_000,
                                       body_type='SUV',
                                       transmission='Automatic', fuel_type='Petrol',
                                       exterior_color='black',
                                       price=1000)
        self.bmw = Car.objects.create(make=self.bmw_make,
                                      model=self.bmw_model, submodel=self.bmw_submodel,
                                      year=2010, mileage=12_000,
                                      body_type='SUV',
                                      transmission='Automatic', fuel_type='Petrol',
                                      exterior_color='silver',
                                      price=1000)
        self.car_params = {
            'make_id': self.make.id,
            'model_id': self.model.id,
            'submodel_id': self.submodel.id,
            'year': 2020,
            'mileage': 1200,
            'transmission': 'Automatic',
            'fuel_type': 'Petrol',
            'exterior_color': 'white',
            'price': 1000
        }
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
        self.assertEqual(response.json()[0]['model'], 'BMW')

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
        self.assertEqual(response.json()[0]['model'], 'BMW')
        self.assertEqual(response.json()[1]['model'], 'Prado')

    def test_order_in_which_query_is_returned(self):
        """
            it should return the SUV first before convertible
        """
        path = '/api/car_registry/car_price_mileage_range'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['model'], 'BMW')

    def test_when_name_is_provided(self):
        """
            it should return the SUV first before convertible
        """
        path = '/api/car_registry/car_price_mileage_range?name=bmw'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['model'], 'BMW')
        self.assertEqual(len(response.json()), 1)

    def test_car_query_without_range_params_but_name_provided(self):
        """
            it should return all cars with a make of toyota
        """
        path = '/api/car_registry/car_price_mileage_range?name=toyota'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['make'], 'toyota')

    def test_successful_car_creation(self):
        """
            it should return all cars with a make of toyota
        """
        path = '/api/car_registry/create_car'
        params = self.car_params
        response = self.client.post(path, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['make'], 'toyota')

    def test_when_model_id_is_null(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params['model_id'] = None
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'model_id cannot be blank')

    def test_when_make_id_is_null(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params['make_id'] = None
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'make_id cannot be blank')

    def test_when_submodel_is_null(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params['submodel_id'] = None
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'submodel_id cannot be blank')

    def test_when_price_is_null(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params['price'] = None
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'price cannot be blank')

    def test_when_mileage_is_null(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params['mileage'] = None
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         'mileage cannot be blank')

    def test_when_submodel_id_not_in_params(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params.pop('submodel_id')
        error_message = 'submodel_id should be in the request param'
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], error_message)

    def test_when_make_id_not_in_params(self):
        """ it should fail """
        path = '/api/car_registry/create_car'
        self.car_params.pop('make_id')
        error_message = 'make_id should be in the request param'
        response = self.client.post(path, self.car_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], error_message)

    def test_search_car_query_params(self):
        """ it should return a car based on make, submodel, model name """
        path = f'/api/car_registry/search_car?make_name={self.make.name}&model_name={self.model.name}&submodel_name={self.submodel.name}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['make'], 'toyota')
        self.assertEqual(len(response.json()), 2)

    def test_search_car_when_one_param_is_missing(self):
        """ it should return a car based on make, submodel, model name """
        path = f'/api/car_registry/search_car?&model_name={self.model.name}&submodel_name={self.submodel.name}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), list())

