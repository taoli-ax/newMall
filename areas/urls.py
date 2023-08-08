from django.urls import path, re_path
from .views import AreaView
urlpatterns = [
    path('areas/',AreaView.as_view(),name='areas'),

]