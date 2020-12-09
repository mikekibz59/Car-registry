""" Car test file"""

import pytest
from django.test import TestCase
from django.db import IntegrityError
from mixer.backend.django import mixer
from car_registry.models import CarMake, CarModel, CarSubModel, Car


class TestCar(TestCase):
    """ Test Class to for the Car Model class """

    def setUp(self):
        """ Init file for the test class"""
        self.make = mixer.blend(CarMake, name='Toyota')
        self.model = mixer.blend(CarModel, id='mark-x', name='Toyota',
                                 make=self.make)
        self.submodel = mixer.blend(CarSubModel, id='mark-x-3', name='mark x',
                                    model=self.model)

    def test_succeful_car_creation(self):
        """Given all attibutes """
        car = Car.objects.create(make=self.make,
                                 model=self.model, submodel=self.submodel,
                                 year=2020, mileage=1200,
                                 body_type='convertible',
                                 transmission='Manual', fuel_type='Petrol',
                                 exterior_color='White',
                                 price=1000)
        self.assertTrue(car.year)
        self.assertTrue(car.id)

    def test_when_make_is_missing(self):
        """raises an error """
        message = 'NOT NULL constraint failed: car_registry_car.make_id'
        with pytest.raises(IntegrityError) as err:
            Car.objects.create(
                model=self.model, submodel=self.submodel,
                year=2020, mileage=1200,
                body_type='convertible',
                transmission='Manual', fuel_type='Petrol',
                exterior_color='White',
                price=1000)
        self.assertEqual(str(err.value),
                         message)

    def test_when_model_is_missing(self):
        """ raises an error """
        message = 'NOT NULL constraint failed: car_registry_car.model_id'
        with pytest.raises(IntegrityError) as err:
            Car.objects.create(
                make=self.make,
                submodel=self.submodel,
                year=2020, mileage=1200,
                body_type='convertible',
                transmission='Manual', fuel_type='Petrol',
                exterior_color='White',
                price=1000)
        self.assertEqual(str(err.value),
                         message)

    def test_when_submodel_is_missing(self):
        """ raises an error """
        message = 'NOT NULL constraint failed: car_registry_car.submodel_id'
        with pytest.raises(IntegrityError) as err:
            Car.objects.create(
                model=self.model,
                make=self.make,
                year=2020, mileage=1200,
                body_type='convertible',
                transmission='Manual', fuel_type='Petrol',
                exterior_color='White',
                price=1000)
        self.assertEqual(str(err.value),
                         message)

    def test_when_year_is_missing(self):
        """ raises an error """
        message = 'NOT NULL constraint failed: car_registry_car.year'
        with pytest.raises(IntegrityError) as err:
            Car.objects.create(
                model=self.model,
                submodel=self.submodel,
                make=self.make,
                mileage=1200,
                body_type='convertible',
                transmission='Manual', fuel_type='Petrol',
                exterior_color='White',
                price=1000)
        self.assertEqual(str(err.value),
                         message)

    def test_when_mileage_is_missing(self):
        """ raises an error """
        message = 'NOT NULL constraint failed: car_registry_car.mileage'
        with pytest.raises(IntegrityError) as err:
            Car.objects.create(
                model=self.model,
                submodel=self.submodel,
                make=self.make,
                year=2020,
                body_type='convertible',
                transmission='Manual', fuel_type='Petrol',
                exterior_color='White',
                price=1000)
        self.assertEqual(str(err.value),
                         message)


    def test_when_not_null_values_are_passed(self):
        """ the car is inserted into the database """
        car = Car.objects.create(make=self.make,
                                 model=self.model, submodel=self.submodel,
                                 year=2020, mileage=1200,
                                 price=1000)
        self.assertTrue(car.id)
