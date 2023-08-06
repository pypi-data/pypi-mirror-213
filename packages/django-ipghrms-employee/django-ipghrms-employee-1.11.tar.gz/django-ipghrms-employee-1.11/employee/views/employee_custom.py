from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.contrib import messages
from custom.models import University
from employee.forms import EmpCusUniForm
from employee.models import Employee


@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s', 'de', 'deputy'])
def EmpCustomUniversityList(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	objects = University.objects.all().order_by('name')
	context = {
		'objects': objects, 'page': 'uni-list', 'employee':employee,
		'title': 'Lista Universidade', 'legend': 'Lista Universidade', 
		'title_p': f' <center> <h2>LISTA UNIVERSIDADE</h2> </center>'
	}
	return render(request, 'employee_custom/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomUniversityAdd(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusUniForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('custom-uni-list', employee.hashed)
	else: form = EmpCusUniForm()
	context = {
		'form': form, 'page': 'add-university','employee':employee,
		'title': 'Aumenta Universidade', 'legend': 'Aumenta Universidade'
	}
	return render(request, 'employee_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomUniversityUpdate(request, pk, hashid):
	objects = get_object_or_404(University, pk = pk)
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusUniForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('custom-uni-list', employee.hashed)
	else: form = EmpCusUniForm(instance=objects)
	context = {
		'form': form, 'page': 'add-university','employee':employee,
		'title': 'Altera Universidade', 'legend': 'Altera Universidade'
	}
	return render(request, 'employee_custom/form.html', context)