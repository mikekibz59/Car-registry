""" Car model test file"""

import pytest
from django.test import TestCase
from django.db import IntegrityError
from mixer.backend.django import mixer
from car_registry.models import CarMake, CarModel


class TestCarModel(TestCase):
    """Car Model Test case """

    def setUp(self):
        """ init file for the test file"""
        self.make = mixer.blend(CarMake, name='Alfa romeo')

    def test_successful_creation(self):
        """test we can create a model """
        model = CarModel.objects.create(id='345', name='alfa',
                                        make=self.make)
        self.assertTrue(model.id)
        self.assertTrue(model.name)
        self.assertTrue(model.created_at)
        self.assertTrue(model.updated_at)

    def test_fails_without_make(self):
        """test fails when not null constraint is not enforced """
        with pytest.raises(IntegrityError) as err:
            CarModel.objects.create(id='345', name='toyota')
        self.assertEqual(str(err.value),
                         'NOT NULL constraint failed: models.make_id')
