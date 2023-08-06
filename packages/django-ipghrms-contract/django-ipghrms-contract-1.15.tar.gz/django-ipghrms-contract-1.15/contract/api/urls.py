from django.urls import path
from . import views

urlpatterns = [
	path('cat/', views.APIContCat.as_view(), name="cont-api-cat"),
	path('pos/', views.APIContPos.as_view(), name="cont-api-pos"),
	path('type/', views.APIContType.as_view(), name="cont-api-type"),
]