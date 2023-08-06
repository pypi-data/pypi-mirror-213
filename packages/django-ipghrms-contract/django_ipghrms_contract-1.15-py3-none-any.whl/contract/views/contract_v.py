import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from employee.models import CurEmpDivision, CurEmpPosition, Employee, FIDNumber, Photo
from contract.models import Contract, ContractType, EmpPosition, EmpSalary, EmpPlacement, Category
from custom.models import Position
from django.http import FileResponse

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ContractDash(request):
	group = request.user.groups.all()[0].name
	cat = Category.objects.all()
	type = ContractType.objects.all()
	pos = Position.objects.all()
	pos2 = Position.objects.filter(Q(id=9)).all()
	pos3 = Position.objects.filter(Q(id=10)|Q(id=11)).all()
	objects_i,objects_j,objects_k,objects_l,objects_m = [],[],[],[],[]
	for i in cat:
		i1 = Contract.objects.filter(category=i, is_active=True).all().count()
		i2 = EmpSalary.objects.filter(contract__category=i, contract__is_active=True, employee__status_id=1).\
				aggregate(Sum('amount')).get('amount__sum', 0.00)
		i3 = i2
		
		if i2 == None:
			i3 = 0
		if i1:
			objects_i.append([i,i1,i3])
	for j in pos:
		j1 = EmpPosition.objects.filter(position_id=j, is_active=True, employee__status_id=1).all().count()
		j2 = EmpSalary.objects.filter(employee__empposition__position_id=j, is_active=True,employee__status_id=1).\
				aggregate(Sum('amount')).get('amount__sum', 0.00)
		j3 = j2
		if j2 == None:
			j3 = 0
		if j1:
			objects_j.append([j,j1,j3])
	tot_i_b,tot_j_b = 0,0
	tot_i_a = None
	tot_j_a = None
	if objects_i:
		tot_i_a = np.sum(np.array(objects_i)[:,1])
		tot_i_b = np.sum(np.array(objects_i)[:,2])
	if objects_j:
		tot_j_a = np.sum(np.array(objects_j)[:,1])
		tot_j_b = np.sum(np.array(objects_j)[:,2])
	context = {
		'group': group, 'objects_i': objects_i, 'objects_j': objects_j, 'objects_k': objects_k,
		'objects_l': objects_l, 'objects_m': objects_m, 'tot_i_a':tot_i_a, 'tot_i_b':tot_i_b,
		'tot_j_b':tot_j_b,'tot_j_a':tot_j_a,
		'title': 'Painel Kontratu', 'legend': 'Painel Kontratu'
	}
	return render(request, 'contract/dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractList(request):
	group = request.user.groups.all()[0].name
	objects = Contract.objects.filter(is_active=True).all()
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'contract/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractDetail(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Contract, hashed=hashid)
	salary = EmpSalary.objects.filter(contract=objects).first()
	emp = Employee.objects.get(pk=objects.employee.id)
	img = Photo.objects.get(employee=emp)
	fidnumber = FIDNumber.objects.get(employee=emp)
	emppos = CurEmpPosition.objects.filter(employee=emp).first()
	empdiv = CurEmpDivision.objects.filter(employee=emp).first()
	emmplacement = EmpPlacement.objects.filter(employee=emp).first()
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'salary': salary, 'img': img,
		'fidnumber': fidnumber, 'emppos': emppos, 'empdiv': empdiv,
		'title': 'Detalha Kontratu', 'legend': 'Detalha Kontratu','emmplacement':emmplacement,
	}
	return render(request, 'contract/detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def NoContractList(request):
	group = request.user.groups.all()[0].name
	emp = Employee.objects.filter(status_id=1).all()
	objects = []
	for i in emp:
		a = Contract.objects.filter(employee=i,is_active=True).first()
		if not a:
			objects.append(i)
	context = {
		'group': group, 'objects': objects,
		'title': 'Funcionariu nebe seidauk atribui kontratu', 'legend': 'Funcionariu nebe seidauk atribui kontratu'
	}
	return render(request, 'contract/nocont_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContractHistList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	empcont = Contract.objects.filter(is_active=True, employee=emp).last()
	objects = Contract.objects.filter(employee=emp, is_active=False).all()
	context = {
		'group': group, 'objects': objects, 'empcont':empcont, 'emp':emp,
		'title': 'Historia Funsionario', 'legend': 'Historia Funsionario'
	}
	return render(request, 'contract/cont_hist.html', context)

###
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def ContractPDF(request, hashid):
	objects = get_object_or_404(Contract, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContChartDash(request):
	group = request.user.groups.all()[0].name
	context = {
		'group': group,
		'title': 'Grafiku', 'legend': 'Grafiku'
	}
	return render(request, 'contract_chart/cont_chart.html', context)

from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def ViewContractTerminateFile(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	file = str(settings.BASE_DIR)+str(cont.file_end.url)
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')