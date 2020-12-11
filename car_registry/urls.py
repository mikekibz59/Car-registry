""" CarRegistry ViewSet Urls """

from django.urls import path, re_path
from car_registry.api.viewsets import CarRegistryViewSet

urlpatterns = [
    path('car_registry/get_makes',
         CarRegistryViewSet.as_view({'get': 'get_car_makes'})),
    path('car_registry/get_models',
         CarRegistryViewSet.as_view({'get': 'get_car_models'})),
    path('car_registry/get_submodels',
         CarRegistryViewSet.as_view({'get': 'get_car_submodels'})),
    path('car_registry/car_price_mileage_range',
         CarRegistryViewSet.as_view({'get': 'get_all_cars_in_range'})),
    path('car_registry/create_car',
         CarRegistryViewSet.as_view({'post': 'create_car'})),
    path('car_registry/search_car',
         CarRegistryViewSet.as_view({'get': 'get_all_cars_on_parent'}))
]
