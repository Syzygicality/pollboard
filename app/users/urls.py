from .views import CharacteristicsCreateView, CharacteristicsSingleView
from django.urls import path

urlpatterns = [
    path('characteristics', CharacteristicsSingleView.as_view(), name='get_characteristics'),
    path('characteristics/post', CharacteristicsCreateView.as_view(), name='create_characteristics'),
]