""" CarMake model test file """

import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from car_registry.models import CarMake


class CarMakeTest(TestCase):

    def test_car_make_creation_on_capitalize_name(self):
        """test to see if the id is make accordingly """

        make = CarMake.objects.create(name='Alfa')
        self.assertEqual(make.id, 'alfa')

    def test_car_make_creation_on_non_capitalized_name(self):
        """Ensure code works well when not capitalized """

        make = CarMake.objects.create(name='alfa')
        self.assertEqual(make.id, 'alfa')

    def test_space_separated_name(self):
        """if separated by spaces it should have a hyphen separating it """

        make = CarMake.objects.create(name='Alfa Romeo')
        make2 = CarMake.objects.create(name='Toyota     Hilux')
        self.assertEqual(make.id, 'alfa-romeo')
        self.assertEqual(make2.id, 'toyota-hilux')

    def test_attributes_presence(self):
        """test to see if all attributes are present """

        make = CarMake.objects.create(name='Benz')
        self.assertTrue(make.id)
        self.assertTrue(make.name)
        self.assertTrue(make.created_at)
        self.assertTrue(make.updated_at)
