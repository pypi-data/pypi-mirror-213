from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from custom.models import Position
from employee.models import Employee, FIDNumber, CurEmpPosition, CurEmpDivision, Photo
from contract.models import Contract, EmpPosition, Organograma
from django.views import View



@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def ManagerDash(request):
	group = request.user.groups.all()[0].name
	deps = EmpPosition.objects.filter(is_manager=True,is_active=True,department__isnull=False)
	units = EmpPosition.objects.filter(is_manager=True, is_active=True,unit__isnull=False)
	des = EmpPosition.objects.filter((Q(position_id=1)|Q(position_id=2)), is_active=True).all()
	organograma  = Organograma.objects.filter(is_active=True).last()
	# file_url = request.build_absolute_uri(org.file.url)
	context = {
		'group': group, 'deps': deps, 'units': units, 'des': des,'organograma': organograma,
		'title': 'Painel Jestor - Institute of Petroleum and Geology', 'legend': 'Painel Jestor -  Institute of Petroleum and Geology'
	}
	return render(request, 'manager/dash.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','de', 'deputy'])
def ManagerDepList(request):
	group = request.user.groups.all()[0].name
	objects = EmpPosition.objects.filter(is_manager=True,is_active=True,department__isnull=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects, 'page': 'dep',
		'title': 'Chefe Ekipa', 'legend': 'Chefe Ekipa'
	}
	return render(request, 'manager/man_dep.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ManagerDepHisList(request):
	group = request.user.groups.all()[0].name
	objects = EmpPosition.objects.filter(department__isnull=False, is_manager=False, is_active=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects, 'page': 'dep',
		'title': 'Historia Chefe Ekipa', 'legend': 'Historia Chefe Ekipa'
	}
	return render(request, 'manager/man_hist.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ManagerUnitList(request):
	group = request.user.groups.all()[0].name
	position = Position.objects.filter(pk=3).first()
	objects = EmpPosition.objects.filter(is_manager=True,is_active=True,unit__isnull=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,'page': 'unit',
		'title': 'Lista Diretor Divizaun', 'legend': 'Lista Diretor Divizaun'
	}
	return render(request, 'manager/man_unit.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ManagerUnitHisList(request):
	group = request.user.groups.all()[0].name
	objects = EmpPosition.objects.filter(unit__isnull=False, is_manager=False, is_active=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects, 'page': 'dep',
		'title': 'Historia Chefe Divizaun', 'legend': 'Historia Chefe Divizaun'
	}
	return render(request, 'manager/man_hist.html', context)

###
@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ManagerDEList(request):
	group = request.user.groups.all()[0].name
	objects = EmpPosition.objects.filter((Q(position_id=1)|Q(position_id=2)), is_active=True).all()
	context = {
		'group': group, 'objects': objects,'page': 'de',
		'title': 'Presidente & Vice Presidente', 'legend': 'Presidente & Vice Presidente'
	}
	return render(request, 'manager/man_de.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ManagerDetail(request, hashid, page):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(EmpPosition, hashed=hashid)
	emp = objects.employee
	img = Photo.objects.get(employee=emp)
	context = {
		'group': group, 'objects': objects, 'emp': emp, 'img': img, 'page': page,
		'title': 'Detalha Nomeasaun', 'legend': 'Detalha Nomeasaun'
	}
	return render(request, 'manager/detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr', 'de', 'deputy'])
def ManagerPrHisList(request):
	group = request.user.groups.all()[0].name
	objects = EmpPosition.objects.filter(de__isnull=False, is_manager=False, is_active=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects, 'page': 'dep',
		'title': 'Historia Presidente & Vice Presidente', 'legend': 'Historia Presidente & Vice Presidente'
	}
	return render(request, 'manager/man_hist.html', context)
###
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def ManagerPDF(request, hashid):
	objects = get_object_or_404(EmpPosition, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')


class OrganogramFileView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        organograma = get_object_or_404(Organograma, pk=pk)
        file = organograma.file
        return FileResponse(open(file.path, 'rb'), content_type='application/pdf')