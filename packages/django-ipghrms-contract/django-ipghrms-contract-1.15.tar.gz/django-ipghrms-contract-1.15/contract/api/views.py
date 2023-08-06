import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from contract.models import Category, Contract, EmpPosition, ContractType
from custom.models import Position
from settings_app.user_utils import c_unit, c_dep

class APIContCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		cats = Category.objects.all()
		obj, label = [],[]
		for i in cats:
			a = []
			if group == 'dep':
				_, dep = c_dep(request.user)
				a = Contract.objects.filter(employee__curempdivision__department=dep, category=i).all().count()
			elif group == 'unit':
				_, unit = c_unit(request.user)
				a = Contract.objects.filter((Q(employee__curempdivision__unit=unit)|\
					Q(employee__curempdivision__department__unit=unit)), category=i).all().count()
			else:
				a = Contract.objects.filter(category=i, is_active=True).all().count()
			obj.append(a)
			label.append(i.name)
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class APIContPos(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		pos = Position.objects.filter().all()
		obj,label = [],[]
		for i in pos:
			a = []
			if group == 'unit':
				_, unit = c_unit(request.user)
				a = EmpPosition.objects.filter((Q(unit=unit)|Q(department__unit=unit)), position=i).all().count()
			else:
				a = EmpPosition.objects.filter(position=i).all().count()
			obj.append(a)
			label.append(i.name)
		data = { 'label': label, 'obj': obj, }
		return Response(data)


class APIContType(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		ct = ContractType.objects.filter().all()
		obj,label = [],[]
		for i in ct:
			a = []
			a = Contract.objects.filter(contract_type=i, is_active=True).all().count()
			obj.append(a)
			label.append(i.name)
		data = { 'label': label, 'obj': obj, }
		return Response(data)

