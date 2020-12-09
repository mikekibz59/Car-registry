"""Car Registry model file """

from uuid import uuid4
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class AbstractRegistryModel(models.Model):
    """ Abstract class to hold related fields"""
    id = models.CharField(max_length=255, primary_key=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        """ AbstractRegistryModel Meta Data"""
        abstract = True


class CarMake(AbstractRegistryModel):
    """ Model class to define the Makes of different cars """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """model string representation """

        return f'id:{self.id}#name:{self.name}'

    def save(self, *args, **kwargs):
        """Ensure the pk is set correctly """

        if not self.pk:
            pk = '-'.join(self.name.lower().split())
            self.id = pk
        super(CarMake, self).save(*args, **kwargs)

    class Meta:
        """ CarMake Meta Data """
        db_table = 'makes'


class CarModel(AbstractRegistryModel):
    """Model class to define a car's models  """

    name = models.CharField(max_length=255, null=True, blank=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        """ model string representation """
        return f'id:{self.id}#name: {self.name}'

    class Meta:
        """ CarModel Meta Data """
        db_table = 'models'


class CarSubModel(AbstractRegistryModel):
    """Model class to define a car's submodel """

    name = models.CharField(max_length=255, null=True, blank=True)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

    def __str__(self):
        """ model string representation"""
        return f'id:{self.pk}#name:{self.name}'

    class Meta:
        """CarSubModel Meta Data """
        db_table = 'sub_models'


class Car(AbstractRegistryModel):
    """ Model class to define car attributes"""
    year = models.IntegerField()
    mileage = models.FloatField()
    price = MoneyField(max_digits=10, decimal_places=2,
                       default_currency='USD')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    submodel = models.ForeignKey(CarSubModel, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=255, null=True, blank=True)
    transmission = models.CharField(max_length=255, null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    exterior_color = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """ Car model string representation"""
        return f'make: {self.make.name}: model: {self.model.name}'

    def save(self, *args, **kwargs):
        """ Generate uuid to act as primary key"""
        if not self.pk:
            uuid = str(uuid4())
            self.id = ''.join(uuid.split('-'))
        super(Car, self).save(*args, **kwargs)
