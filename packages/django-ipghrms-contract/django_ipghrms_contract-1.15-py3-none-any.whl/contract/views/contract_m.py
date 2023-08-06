import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum, Count, Q
from employee.models import CurEmpDivision, CurEmpPosition, Employee, FIDNumber, Photo
from contract.models import Contract, EmpSalary, EmpPosition, ContractType, EmpPlacement
from contract.forms import ContractForm, ContractEndForm, ContractTernimateForm
from custom.models import Position
from settings_app.utils import getnewid
from log.utils import log_action

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractAdd(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	emppos = CurEmpPosition.objects.filter(employee=emp).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(Contract)
		form = ContractForm(request.POST, request.FILES)
		if form.is_valid():
			position = form.cleaned_data.get('position')
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			
			emppos.position = position
			emppos.save()
			messages.success(request, f'Susesu Aumenta')
			return redirect('cont-no-list')
	else: form = ContractForm()
	context = {
		'form': form, 'emp': emp, 'page': 'add',
		'title': 'Aumenta Kontrato', 'legend': 'Aumenta Kontrato ba %s' % (emp)
	}
	return render(request, 'contract/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractUpdate(request, hashid):
	objects = get_object_or_404(Contract, hashed=hashid)
	emppos = CurEmpPosition.objects.filter(employee=objects.employee).first()
	if request.method == 'POST':
		form = ContractForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			position = form.cleaned_data.get('position')
			instance = form.save(commit=False)
			instance.save()
			emppos.position = position
			emppos.save()
			log_action(request, model=Contract._meta.model_name, action="Update",field_id=objects.pk)
			messages.success(request, f'Susesu Altera.')
			return redirect('cont-detail', hashid=hashid)
	else: form = ContractForm(instance=objects)
	context = {
		'objects': objects, 'form': form, 'emp': objects.employee, 'page': 'update',
		'title': 'Altera Servisu', 'legend': 'Altera Servisu'
	}
	return render(request, 'contract/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractRenew(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	objects2 = EmpSalary.objects.get(contract=cont)
	employee = get_object_or_404(Employee, id=cont.employee.id)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Contract)
		form = ContractForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			# employee.status.pk = 1
			# employee.save()
			employee =  Employee.objects.filter(id=cont.employee.id).update(status_id=1)
			instance.id = newid
			instance.employee = cont.employee
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			
			end_date = form.cleaned_data.get('end_date')
			cont.end_date = end_date
			# cont.is_active = False
			cont.save()
			messages.success(request, f'Susesu Halo Foun')
			return redirect('cont-detail', hashid=new_hashid)
	else: form = ContractForm()
	context = {
		'form': form, 'emp': cont.employee, 'cont': cont, 'page': 'contract',
		'title': 'Renew Contract', 'legend': 'Renew Contract'
	}
	return render(request, 'contract/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractEnd(request, hashid):
	objects = get_object_or_404(Contract, hashed=hashid)
	objects2 = EmpSalary.objects.get(contract=objects)
	emp = Employee.objects.filter(id=objects.employee.id).first()
	objects3 = EmpPosition.objects.filter(employee=emp, is_manager=True, is_active=True).first()
	objects4 = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
	objects5 = CurEmpPosition.objects.filter(employee=emp).first()
	objects6 = CurEmpDivision.objects.filter(employee=emp).first()
	
	if request.method == 'POST':
		form = ContractEndForm(request.POST,request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.is_active = False
			instance.save()
			objects2.is_active = False
			objects2.save()
			emp.status_id = 2
			emp.save()
			if objects3:
				objects3.is_active = False
				objects3.is_manager = False
				objects3.save()
			if objects4:
				objects4.is_active = False
				objects4.save()
			if objects5:
				objects5.position = None
				objects5.save()
			if objects6:
				objects6.de = None
				objects6.unit = None
				objects6.department = None
				objects6.save()
			messages.success(request, f'Susesu Altera')
			return redirect('cont-list')
	else: form = ContractEndForm(instance=objects)
	context = {
		'objects': objects, 'form': form, 'emp': objects.employee, 'page': 'update',
		'title': 'Contract Termination', 'legend': 'Contract Termination'
	}
	return render(request, 'contract/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractLock(request, hashid):
	objects = get_object_or_404(Contract, hashed=hashid)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Locked.')
	return redirect('cont-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractUnLock(request, hashid):
	objects = get_object_or_404(Contract, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Unlocked.')
	return redirect('cont-detail', hashid=hashid)
