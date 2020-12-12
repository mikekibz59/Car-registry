""" CarSubModel model test file"""

import pytest
from django.test import TestCase
from django.db import IntegrityError
from mixer.backend.django import mixer
from car_registry.models import CarMake, CarModel, CarSubModel


class TestCarModel(TestCase):
    """Car Model Test case """

    def setUp(self):
        """ init file for the test class"""
        self.make = mixer.blend(CarMake, name='Alfa romeo')
        self.model = mixer.blend(CarModel, id='xxx', name='BMW',
                                 make=self.make)

    def test_successful_creation(self):
        """test we can create a model """
        model = CarSubModel.objects.create(id='345', name='alfa',
                                        model=self.model)
        self.assertTrue(model.id)
        self.assertTrue(model.name)
        self.assertTrue(model.created_at)
        self.assertTrue(model.updated_at)

    def test_fails_without_model(self):
        """test fails when models is not supplied   """
        with pytest.raises(IntegrityError) as err:
            CarSubModel.objects.create(id='345', name='toyota')
        self.assertEqual(str(err.value),
                         '(1048, "Column \'model_id\' cannot be null")')
