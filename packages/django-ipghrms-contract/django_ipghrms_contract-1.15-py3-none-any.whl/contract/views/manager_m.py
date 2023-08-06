import datetime
from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from custom.models import Position
from employee.models import Employee, FIDNumber, CurEmpPosition, CurEmpDivision, Photo
from contract.models import Category, Contract, EmpPlacement, EmpPosition
from contract.forms import ManDEForm, ManDEForm2, ManEndForm, ManUnitForm, ManUnitForm2, ManDepForm, ManDepForm2
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerDepAdd(request):
	# position = Position.objects.get(pk=4)
	# category = Category.objects.get(pk=5)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpPosition)
		form = ManDepForm(request.POST, request.FILES)
		if form.is_valid():
			dep = form.cleaned_data.get('department')
			emp = form.cleaned_data.get('employee')
			start_date = form.cleaned_data.get('start_date')
			cont = Contract.objects.filter(employee=emp, is_active=True).first()
			check = EmpPosition.objects.filter(department=dep, is_active=True).first()
			if not check:
				check2 = EmpPosition.objects.filter(employee=emp, is_active=True).first()
				staff_p = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
				# if staff_p:
				# 	staff_p.is_active = False
				# 	staff_p.end_date = start_date
				# 	staff_p.position = position
				# 	staff_p.save()
				instance = form.save(commit=False)
				instance.id = newid
				instance.position = cont.position
				instance.is_active = True
				instance.is_manager = True
				instance.datetime = datetime.datetime.now()
				instance.user = request.user
				instance.position = cont.position
				instance.hashed = new_hashid
				instance.save()
				empdiv = CurEmpDivision.objects.get(employee=emp)
				empdiv.department = dep
				empdiv.save()
				emppos = CurEmpPosition.objects.get(employee=emp)
				emppos.position = cont.position
				emppos.save()
				place = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
				if place:
					# place.is_active = False
					# place.end_date = start_date
					place.position = cont.position
					place.save()
				# cont.position = position
				# cont.category = category
				# cont.save()
				messages.success(request, f'Aumenta sucesu.')
				
			else:
				messages.error(request, f'Pojisaun ba %s iha ona.' % (dep))
			return redirect('man-dep-list')
	else: form = ManDepForm()
	context = {
		'form': form, 'page': 'dep',
		'title': 'Aumenta Chefe Departamento', 'legend': 'Aumenta Chefe Departamento'
	}
	return render(request, 'manager/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerDepUpdate(request, hashid):
	objects = EmpPosition.objects.filter(hashed=hashid).first()
	dep = objects.department
	if request.method == 'POST':
		form = ManDepForm2(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			dep2 = form.cleaned_data.get('department')
			if dep == dep2:
				form.save()
			else: 
				check = EmpPosition.objects.filter(department=dep2, is_active=True).first()
				if not check:
					form.save()
					empdiv = CurEmpDivision.objects.get(employee=objects.employee)
					empdiv.department = dep2
					empdiv.save()
					messages.success(request, f'Nomeasaun altera ona.')
				else:
					messages.error(request, f'Pojisaun ba %s iha ona.' % (dep2))
			return redirect('man-dep-list')
	else: form = ManDepForm2(instance=objects)
	context = {
		'form': form, 'page': 'dep',
		'title': 'Troka Chefe Seksaun', 'legend': 'Troka Chefe Seksaun'
	}
	return render(request, 'manager/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerUnitAdd(request):
	# position = Position.objects.get(pk=3)
	# category = Category.objects.get(pk=5)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpPosition)
		form = ManUnitForm(request.POST, request.FILES)
		if form.is_valid():
			unit = form.cleaned_data.get('unit')
			emp = form.cleaned_data.get('employee')
			start_date = form.cleaned_data.get('start_date')
			cont = Contract.objects.filter(employee=emp, is_active=True).first()
			check = EmpPosition.objects.filter(unit=unit,  is_active=True).first()
			if not check:
				check2 = EmpPosition.objects.filter(employee=emp, is_active=True).first()
				if not check2:
					staff_p = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
					# if staff_p:
					# 	staff_p.is_active = False
					# 	staff_p.end_date = start_date
					# 	staff_p.position = position
					# 	staff_p.save()
					instance = form.save(commit=False)
					instance.id = newid
					instance.position = cont.position
					instance.is_active = True
					instance.is_manager = True
					instance.datetime = datetime.datetime.now()
					instance.user = request.user
					instance.hashed = new_hashid
					instance.save()
					empdiv = CurEmpDivision.objects.get(employee=emp)
					empdiv.unit = unit
					empdiv.save()
					emppos = CurEmpPosition.objects.get(employee=emp)
					emppos.position = cont.position
					emppos.save()
					place = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
					if place:
						# place.is_active = False
						# place.end_date = start_date
						place.position = cont.position
						place.save()
					# cont.position = position
					# cont.category = category
					# cont.save()
					messages.success(request, f'Aumenta sucesu.')
				else:
					messages.error(request, f'%s asume hela kargu nudar %s. Halo favor termina lai procesu antes nomeasaun foun. Obrigadu...' % (emp,check2.position))
			else:
				messages.error(request, f'Coordenador ba %s iha ona.' % (unit.code))
			return redirect('man-unit-list')
	else: form = ManUnitForm()
	context = {
		'form': form, 'page': 'unit',
		'title': 'Aumenta Coordenador Unidade', 'legend': 'Aumenta Coordenador Unidade'
	}
	return render(request, 'manager/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerUnitUpdate(request, hashid):
	objects = EmpPosition.objects.filter(hashed=hashid).first()
	unit = objects.unit
	if request.method == 'POST':
		form = ManUnitForm2(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			unit2 = form.cleaned_data.get('unit')
			if unit == unit2:
				form.save()
			else: 
				check = EmpPosition.objects.filter(unit=unit2, is_active=True).first()
				if not check:
					form.save()
					empdiv = CurEmpDivision.objects.get(employee=objects.employee)
					empdiv.unit = unit2
					empdiv.save()
					messages.success(request, f'Nomeasaun altera ona.')
				else:
					messages.error(request, f'Coordenador ba %s iha ona.' % (unit2))
			return redirect('man-unit-list')
	else: form = ManUnitForm2(instance=objects)
	context = {
		'form': form, 'page': 'unit',
		'title': 'Troka Coordenador Unidade', 'legend': 'Troka Coordenador Unidade'
	}
	return render(request, 'manager/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerDEAdd(request):
	category = Category.objects.get(pk=5)
	position = []
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpPosition)
		form = ManDEForm(request.POST, request.FILES)
		if form.is_valid():
			de = form.cleaned_data.get('de')
			if de.id == 1:
				position = Position.objects.get(pk=1)
			else:
				position = Position.objects.get(pk=2)
			emp = form.cleaned_data.get('employee')
			start_date = form.cleaned_data.get('start_date')
			cont = Contract.objects.filter(employee=emp, is_active=True).first()
			check = EmpPosition.objects.filter(de=de, position=position, is_active=True).first()
			if not check:
				check2 = EmpPosition.objects.filter(employee=emp, is_active=True).first()
				if not check2:
					staff_p = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
					if staff_p:
						staff_p.is_active = False
						staff_p.end_date = start_date
						staff_p.position = position
						staff_p.save()
					instance = form.save(commit=False)
					instance.id = newid
					instance.position = position
					instance.is_active = True
					instance.datetime = datetime.datetime.now()
					instance.user = request.user
					instance.hashed = new_hashid
					instance.save()
					empdiv = CurEmpDivision.objects.get(employee=emp)
					empdiv.de = de
					empdiv.save()
					emppos = CurEmpPosition.objects.get(employee=emp)
					emppos.position = position
					emppos.save()
					place = EmpPlacement.objects.filter(employee=emp, is_active=True).first()
					if place:
						place.is_active = False
						place.end_date = start_date
						place.position = position
						place.save()
					cont.position = position
					cont.category = category
					cont.save()
					messages.success(request, f'Aumenta sucesu.')
				else:
					messages.error(request, f'%s asume hela kargu nudar %s. Halo favor termina lai procesu antes nomeasaun foun. Obrigadu...' % (emp,check2.position))
			else:
				messages.error(request, f'Pojisaun ba %s iha ona.' % (de.code))
			return redirect('man-de-list')
	else: form = ManDEForm()
	context = {
		'form': form, 'page': 'unit',
		'title': 'Aumenta DE / Adjuntu', 'legend': 'Aumenta DE / Adjuntu'
	}
	return render(request, 'manager/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerDEUpdate(request, hashid):
	objects = EmpPosition.objects.filter(hashed=hashid).first()
	de = objects.de
	position = []
	if request.method == 'POST':
		form = ManDEForm2(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			de2 = form.cleaned_data.get('de')
			if de2.id == 1: position = Position.objects.get(pk=1)
			else: position = Position.objects.get(pk=2)
			emppos = CurEmpPosition.objects.get(employee=objects.employee)
			emppos.position = position
			emppos.save()
			cont = Contract.objects.filter(employee=objects.employee, is_active=True).first()
			if de == de2:
				instance = form.save(commit=False)
				instance.position = position
				instance.save()
				cont.position = position
				cont.save()
			else: 
				check = EmpPosition.objects.filter(de=de2, is_active=True).first()
				if not check:
					instance = form.save(commit=False)
					instance.position = position
					instance.save()
					cont.position = position
					cont.save()
					empdiv = CurEmpDivision.objects.get(employee=objects.employee)
					empdiv.de = de2
					empdiv.save()
					messages.success(request, f'Nomeasaun altera ona.')
				else:
					messages.error(request, f'Pojisaun ba %s iha ona.' % (de2.code))
			return redirect('man-de-list')
	else: form = ManDEForm2(instance=objects)
	context = {
		'form': form, 'page': 'de',
		'title': 'Troka DE / Adjuntu', 'legend': 'Troka DE / Adjuntu'
	}
	return render(request, 'manager/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin', 'hr'])
def ManagerEnd(request, hashid, page):
	objects = EmpPosition.objects.filter(hashed=hashid).first()
	if request.method == 'POST':
		form = ManEndForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.is_active = False
			instance.is_manager = False
			
			instance.save()
			# empdiv = CurEmpDivision.objects.get(employee=objects.employee)
			# empdiv.de = None
			# empdiv.unit = None
			# empdiv.department = None
			# empdiv.save()
			# emppos = CurEmpPosition.objects.get(employee=objects.employee)
			# emppos.position = None
			# emppos.save()
			# emppos = Contract.objects.filter(employee=objects.employee, is_active=True).last()
			# emppos.contract_type = None
			# emppos.start_date = None
			# emppos.end_date = None
			# emppos.position = None
			# emppos.category = None
			# emppos.save()
			messages.success(request, f'Kargo termina ona.')
			if page == "dep":
				return redirect('man-dep-list')
			elif page == "unit":
				return redirect('man-unit-list')
			elif page == "de":
				return redirect('man-de-list')
	else: form = ManEndForm(instance=objects)
	context = {
		'form': form, 'page': page,
		'title': 'Kargo Termina', 'legend': 'Kargo Termina'
	}
	return render(request, 'manager/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerRemove(request, hashid, page):
	objects = get_object_or_404(EmpPosition, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=objects.employee)
	emppos = CurEmpPosition.objects.get(employee=objects.employee)
	cont = Contract.objects.filter(employee=objects.employee, is_active=True).first()
	emppos.position = None
	emppos.save()
	empdiv.department = None
	empdiv.unit = None
	empdiv.de = None
	empdiv.save()
	if cont:
		cont.position = None
		cont.save()
	objects.delete()
	messages.success(request, f'Hapaga sucesu.')
	if page == "dep":
		return redirect('man-dep-list')
	elif page == "unit":
		return redirect('man-unit-list')
	elif page == "de":
		return redirect('man-de-list')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerLock(request, hashid, page):
	objects = get_object_or_404(EmpPosition, hashed=hashid)
	objects.is_confirm = True
	objects.save()
	messages.success(request, f'Xavi.')
	if page == "dep":
		return redirect('man-dep-list')
	elif page == "unit":
		return redirect('man-unit-list')
	elif page == "de":
		return redirect('man-de-list')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerUnLock(request, hashid, page):
	objects = get_object_or_404(EmpPosition, hashed=hashid)
	objects.is_confirm = False
	objects.save()
	messages.success(request, f'Loke.')
	if page == "dep":
		return redirect('man-dep-list')
	elif page == "unit":
		return redirect('man-unit-list')
	elif page == "de":
		return redirect('man-de-list')
# ###