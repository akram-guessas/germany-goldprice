import django_filters
from django import forms

from .models import Item

class ItemFilter(django_filters.FilterSet):
    '''price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')
    
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    class Meta:
        model = Item
        fields = ['price', 'address','item_date','min_price', 'max_price']
    '''
    price = django_filters.RangeFilter()
    # item_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Item
        fields = ['price',]