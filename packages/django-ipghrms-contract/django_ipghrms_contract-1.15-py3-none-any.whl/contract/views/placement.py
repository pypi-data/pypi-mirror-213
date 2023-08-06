import datetime
from django.db.models.query import prefetch_related_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from custom.models import Department, Position
from employee.models import Employee, CurEmpPosition, CurEmpDivision, Photo, WorkExperience
from contract.models import Contract, EmpPlacement
from contract.forms import EmpPlacementForm, EmpPlacementEndForm
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpPlacementList(request):
	position = Position.objects.filter(pk=1).first()
	objects = EmpPlacement.objects.filter(is_active=True).all()
	context = {
		'objects': objects,
		'title': 'Kolokasaun Funcionariu', 'legend': 'Kolokasaun Funcionariu'
	}
	return render(request, 'placement/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpPlacementDetail(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	img = Photo.objects.get(employee=emp)
	emppos = CurEmpPosition.objects.get(employee=emp)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	place = EmpPlacement.objects.filter(employee=emp, is_active=True).last()
	place_hist = EmpPlacement.objects.filter(employee=emp, is_active=False).all().order_by('-end_date')
	# nom = Nomeasaun.objects.filter(employee=emp, is_active=True).first()
	nom = []
	a = 0
	if nom:
		a = 1
	context = {
		'emp': emp, 'img': img, 'emppos': emppos, 'empdiv': empdiv, 'place': place,
		'place_hist': place_hist, 'nom': nom, 'a': a, 'page': 'staff',
		'title': 'Detalha', 'legend': 'Detalha'
	}
	return render(request, 'placement/detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'hr'])
def EmpPlacementAdd(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpPlacement)
		form = EmpPlacementForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.is_active = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			de = form.cleaned_data.get('de')
			unit = form.cleaned_data.get('unit')
			dep = form.cleaned_data.get('department')
			empdiv = CurEmpDivision.objects.get(employee=emp)
			if dep:
				empdiv.department = dep
				if unit:
					empdiv.unit = unit
				else:
					empdiv.unit = None
				empdiv.de = None
			elif unit:
				empdiv.department = None
				empdiv.unit = unit
				empdiv.de = None
			else:
				empdiv.department = None
				empdiv.unit = None
				empdiv.de = de
			empdiv.save()
			messages.success(request, f'Susesu Aumenta')
			return redirect('emp-no-div')
	else: form = EmpPlacementForm()
	context = {
		'form': form, 'emp': emp,
		'title': 'Assign Employee', 'legend': 'Assign Employee'
	}
	return render(request, 'placement/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'hr'])
def EmpPlacementUpdate(request, hashid):
	objects = get_object_or_404(EmpPlacement, hashed=hashid)
	emp = Employee.objects.get(id=objects.employee.id)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	emppos = CurEmpPosition.objects.get(employee=emp)
	if request.method == 'POST':
		form = EmpPlacementForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			empdiv.de = instance.de
			empdiv.unit = instance.unit
			empdiv.department = instance.department
			empdiv.save()
			emppos.position = instance.position
			emppos.save()
			messages.success(request, f'Susesu Aumenta')
			return redirect('emp-no-div')
	else: form = EmpPlacementForm(instance=objects)
	context = {
		'form': form, 'emp': emp,'objects':objects,
		'title': 'Update placement', 'legend': 'update Employee'
	}
	return render(request, 'placement/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def KolokaStaffUpdate(request, hashid):
# 	objects = get_object_or_404(Kolokasaun,hashed=hashid)
# 	emp = objects.employee
# 	empdiv = EmployeeDivision.objects.get(employee=emp)
# 	print(empdiv)
# 	if request.method == 'POST':
# 		form = KolokaStaffForm(request.POST, request.FILES, instance=objects)
# 		if form.is_valid():
# 			sec = form.cleaned_data.get('section')
# 			dep = form.cleaned_data.get('department')
# 			div = form.cleaned_data.get('division')
# 			dg = form.cleaned_data.get('dg')
# 			instance = form.save(commit=False)
# 			instance.save()
# 			if sec:
# 				empdiv.section = sec
# 				empdiv.department = None
# 				empdiv.division = None
# 				empdiv.dg = None
# 			elif dep:
# 				empdiv.section = None
# 				empdiv.department = dep
# 				empdiv.division = None
# 				empdiv.dg = None
# 			elif div:
# 				empdiv.section = None
# 				empdiv.department = None
# 				empdiv.division = div
# 				empdiv.dg = None
# 			else:
# 				empdiv.section = None
# 				empdiv.department = None
# 				empdiv.division = None
# 				empdiv.dg = dg
# 			empdiv.save()
# 			messages.success(request, f'Kolokasaun altera ona.')
# 			return redirect('koloka-staff-detail', hashid=objects.employee.hashed)
# 	else:
# 		form = KolokaStaffForm(instance=objects)
# 	context = {
# 		'form': form, 'emp': emp,
# 		'title': 'Troka Departamento', 'legend': 'Troka Departamento'
# 	}
# 	return render(request, 'contract_koloka/form_assign.html', context)
# ##############

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def KolokaStaffEnd(request, hashid):
# 	objects = Kolokasaun.objects.filter(hashed=hashid).first()
# 	if request.method == 'POST':
# 		form = KolokaEndStaffForm(request.POST, instance=objects)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.is_active = False
# 			instance.save()
# 			empdiv = EmployeeDivision.objects.get(employee=objects.employee)
# 			empdiv.dg = None
# 			empdiv.division = None
# 			empdiv.department = None
# 			empdiv.section = None
# 			empdiv.save()
# 			emppos = EmployeePosition.objects.get(employee=objects.employee)
# 			emppos.position = None
# 			emppos.save()
# 			messages.success(request, f'Promosaun termina ona.')
# 			return redirect('koloka-staff-detail', hashid=objects.employee.hashed)
# 	else:
# 		form = KolokaEndStaffForm(instance=objects)
# 	context = {
# 		'form': form,
# 		'title': 'Kolokasuan Termina', 'legend': 'Kolokasuan Termina'
# 	}
# 	return render(request, 'contract_koloka/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def KolokaStaffRemove(request, hashid):
# 	objects = get_object_or_404(Kolokasaun, hashed=hashid)
# 	empdiv = EmployeeDivision.objects.get(employee=objects.employee)
# 	emppos = EmployeePosition.objects.get(employee=objects.employee)
# 	emppos.position = None
# 	emppos.save()
# 	empdiv.dg = None
# 	empdiv.division = None
# 	empdiv.department = None
# 	empdiv.section = None
# 	empdiv.save()
# 	objects.delete()
# 	messages.success(request, f'Promosaun hagapa ona.')
# 	return redirect('koloka-staff-detail', hashid=objects.employee.hashed)

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def KolokaStaffLock(request, hashid):
# 	objects = get_object_or_404(Kolokasaun, hashed=hashid)
# 	objects.is_confirm = True
# 	objects.save()
# 	ins = Institute.objects.filter(is_active=True).first()
# 	contract = Contract.objects.filter(employee=objects.employee, is_active=True).first()
# 	category,grade,echelon = "","",0
# 	if contract:
# 		category = contract.category.name
# 		grade = contract.grade.name
# 		echelon = contract.echelon.code
# 	dg,div,dep,sec,pos = "","","","",""
# 	if objects.dg:
# 		dg = objects.dg.name
# 	if objects.division:
# 		div = objects.division.name
# 	if objects.department:
# 		dep = objects.department.name
# 	if objects.section:
# 		sec = objects.section.name
# 	if objects.position:
# 		pos = objects.position.name
# 	newid, new_hashid = getnewid(WorkExperience)
# 	obj = WorkExperience(id=newid, employee=objects.employee, instituisaun=ins.name, dg=dg, diresaun=div, departamentu=dep,\
# 		seksaun=sec, pojisaun=pos, kategoria=category, grau=grade, eskalaun=echelon, \
# 		start_date=objects.start_date, end_date=objects.end_date,\
# 		municipality=ins.municipality, administrativepost=ins.administrativepost, village=ins.village,\
# 		aldeia=ins.aldeia, hashed=new_hashid)
# 	obj.save()
# 	messages.success(request, f'Promosaun xavi.')
# 	return redirect('koloka-staff-detail', hashid=objects.employee.hashed)

# @login_required
# @allowed_users(allowed_roles=['admin'])
# def KolokaStaffUnLock(request, hashid):
# 	objects = get_object_or_404(Kolokasaun, hashed=hashid)
# 	objects.is_confirm = False
# 	objects.save()
# 	messages.success(request, f'Promosaun loke.')
# 	return redirect('koloka-staff-detail', hashid=objects.employee.hashed)

# ###
# from django.conf import settings
# from django.http import FileResponse, Http404
# @login_required
# def KolokaPDF(request, hashid):
# 	objects = get_object_or_404(Kolokasaun, hashed=hashid)
# 	file = str(settings.BASE_DIR)+str(objects.file.url)
# 	# file = objects.file.url
# 	try:
# 		if file:
# 			return FileResponse(open(file, 'rb'), content_type='application/pdf')
# 		else:
# 			return FileResponse(open(file, 'rb'))
# 	except FileNotFoundError:
# 		raise Http404('not found')