import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from employee.models import  Employee 
from contract.models import Contract, EmpContractToR
from settings_app.utils import getnewid
from contract.forms import EmpContTorForm
import datetime
from django.contrib import messages

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpToRList(request, hashid, hashid2):
    contract = get_object_or_404(Contract, hashed=hashid)
    employee = get_object_or_404(Employee, hashed=hashid2)
    tor = EmpContractToR.objects.filter(employee=employee, contract=contract)
    checktor = EmpContractToR.objects.filter(is_lock=False).exists()
    
    context = {
        'title': 'Lista ToR',
        'legend': 'Lista ToR',
        'tor': tor,
        'contract': contract,
        'employee': employee,
        'checktor':checktor
    }
    return render(request, 'tor/list.html', context)



@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpToRAdd(request, hashid, hashid2):
    contract = get_object_or_404(Contract, hashed=hashid)
    employee = get_object_or_404(Employee, hashed=hashid2)
    if request.method == 'POST':
        newid, new_hashid = getnewid(EmpContractToR)
        form = EmpContTorForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.contract  = contract
            instance.employee = employee
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            
            messages.success(request, f'Susesu Aumenta')
            return redirect('tor-list', hashid=contract.hashed, hashid2=employee.hashed)
    else: form = EmpContTorForm()
    context = {
        'form': form, 'emp': employee,  'contract': contract,
        'title': 'Aumenta ToR', 'legend': 'Aumenta ToR ba %s' % (employee)
    }
    return render(request, 'tor/form.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpToRUpdate(request, hashid, hashid2, hashid3):
    contract = get_object_or_404(Contract, hashed=hashid)
    employee = get_object_or_404(Employee, hashed=hashid2)
    tor = get_object_or_404(EmpContractToR, hashed=hashid3)
    if request.method == 'POST':
        form = EmpContTorForm(request.POST, instance=tor)
        if form.is_valid():
            form.save()
            
            messages.success(request, f'Susesu Altera')
            return redirect('tor-list', hashid=contract.hashed, hashid2=employee.hashed)
    else: form = EmpContTorForm(instance=tor)
    context = {
        'form': form, 'emp': employee,  'contract': contract,
        'title': 'Altera ToR', 'legend': 'Altera ToR ba %s' % (employee)
    }
    return render(request, 'tor/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpToRDelete(request, hashid, hashid2, hashid3):
    contract = get_object_or_404(Contract, hashed=hashid)
    employee = get_object_or_404(Employee, hashed=hashid2)
    tor = get_object_or_404(EmpContractToR, hashed=hashid3)
    tor.delete()
    messages.success(request, f'Susesu Delete')
    return redirect('tor-list', hashid=contract.hashed, hashid2=employee.hashed)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpToRlock(request, hashid, hashid2):
    contract = get_object_or_404(Contract, hashed=hashid)
    employee = get_object_or_404(Employee, hashed=hashid2)
    tor = EmpContractToR.objects.filter(contract=contract, employee=employee)
    for obj in tor:
        obj.is_lock = True
        obj.save()
    messages.success(request, f'Susesu Delete')
    return redirect('tor-list', hashid=contract.hashed, hashid2=employee.hashed)


