from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from employee.models import Employee, CurEmpDivision, CurEmpPosition, FIDNumber, Photo
from contract.models import Contract, EmpSalary
from contract.forms import EmpSalaryForm
from settings_app.utils import getnewid
from log.utils import log_action

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryList(request):
	group = request.user.groups.all()[0].name
	objects = EmpSalary.objects.filter(contract__is_active=True).all()
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Salariu', 'legend': 'Lista Salariu'
	}
	return render(request, 'salary/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def NoSalaryList(request):
	group = request.user.groups.all()[0].name
	emp = Employee.objects.filter().all()
	objects = []
	for i in emp:
		a = Contract.objects.filter(employee=i, is_active=True).first()
		if not a:
			objects.append(i)
	context = {
		'group': group, 'objects': objects,
		'title': 'Funcionariu nebe seidauk atribui salariu', 'legend': 'Funcionariu nebe seidauk atribui salariu'
	}
	return render(request, 'salary/no_salary_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de'])
def SalaryDetail(request, hashid, check):
	data = False
	checkSession = request.session.get('data')
	if checkSession == 'pass':
		data = True
		del request.session['data']
	group = request.user.groups.all()[0].name
	salary = get_object_or_404(EmpSalary, hashed=hashid)
	contract = salary.contract
	emp = contract.employee
	img = Photo.objects.get(employee=emp)
	idnumber = FIDNumber.objects.get(employee=emp)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	emppos = CurEmpPosition.objects.get(employee=emp)
	context = {
		'group': group, 'salary': salary, 'contract': contract, 'emp': emp, 'img': img,
		'idnumber': idnumber, 'empdiv': empdiv, 'emppos': emppos, 'page':data,
		'title': 'Detalha Salariu', 'legend': 'Detalha Salariu'
	}
	return render(request, 'salary/detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryUpdate(request, hashid):
	objects = get_object_or_404(EmpSalary, hashed=hashid)
	contract = objects.contract
	emp_position = CurEmpPosition.objects.filter(employee=contract.employee).first()
	if request.method == 'POST':
		form = EmpSalaryForm(request.POST, instance=objects)
		if form.is_valid():
			# pos_salary = form.cleaned_data.get('position_salary')
			# transport = form.cleaned_data.get('transport')
			# if not transport:
			# 	transport = 0
			# if pos_salary:
			# 	total = objects.basic_salary.amount + objects.position_salary.amount + transport
			# else:
			# 	total = objects.basic_salary.amount + transport
			
			instance = form.save(commit=False)
			# instance.position = emp_position.position
			# instance.total = total
			instance.save()
			log_action(request, model=EmpSalary._meta.model_name, action="Update",field_id=objects.pk)
			messages.success(request, f'Salariu altera ona.')
			return redirect('salary-detail', hashid=hashid)
	else: form = EmpSalaryForm(instance=objects)
	context = {
		'objects': objects, 'form': form, 'emp': contract.employee, 'contract': contract, 'emp_position': emp_position,
		'title': 'Altera Salariu', 'legend': 'Altera Salariu'
	}
	return render(request, 'salary/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryLock(request, hashid):
	objects = get_object_or_404(EmpSalary, hashed=hashid)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Kontratu xavi.')
	return redirect('salary-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def SalaryUnLock(request, hashid):
	objects = get_object_or_404(EmpSalary, hashed=hashid)
	objects.is_lock = False
	objects.save()
	messages.success(request, f'Kontratu loke.')
	return redirect('salary-detail', hashid=hashid)
