from django.urls import path
from . import views

urlpatterns = [
	path('dash/', views.ManagerDash, name="man-dash"),
	#
	path('dep/list/', views.ManagerDepList, name="man-dep-list"),
	path('dep/add/', views.ManagerDepAdd, name="man-dep-add"),
	path('dep/hist/', views.ManagerDepHisList, name="man-dep-hist"),
	path('dep/update/<str:hashid>/', views.ManagerDepUpdate, name="man-dep-update"),
	#
	path('unit/list/', views.ManagerUnitList, name="man-unit-list"),
	path('unit/add/', views.ManagerUnitAdd, name="man-unit-add"),
	path('unit/update/<str:hashid>/', views.ManagerUnitUpdate, name="man-unit-update"),
	path('unit/hist/', views.ManagerUnitHisList, name="man-unit-hist"),
	#
	path('pr/list/', views.ManagerDEList, name="man-de-list"),
	path('pr/add/', views.ManagerDEAdd, name="man-de-add"),
	path('pr/update/<str:hashid>/', views.ManagerDEUpdate, name="man-de-update"),
	path('pr/hist/', views.ManagerPrHisList, name="man-pr-hist"),
	#
	path('remove/<str:hashid>/<str:page>/', views.ManagerRemove, name="man-remove"),
	path('lock/<str:hashid>/<str:page>/', views.ManagerLock, name="man-lock"),
	path('unlock/<str:hashid>/<str:page>/', views.ManagerUnLock, name="man-unlock"),
	path('end/<str:hashid>/<str:page>/', views.ManagerEnd, name="man-end"),
]