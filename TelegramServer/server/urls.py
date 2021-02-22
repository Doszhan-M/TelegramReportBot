from django.urls import path
from .views import GraphicList


urlpatterns = [
    path('', GraphicList.as_view(), name='GraphicList'),

]