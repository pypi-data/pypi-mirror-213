from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary, EmpPlacement
from settings_app.decorators import allowed_users
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.contrib import messages
from datetime import datetime
from leave.models import Leave, LeaveCount, LeavePeriod, LeaveType
from leave.utils import check_period_date, check_period_range
import pandas as pd
from attendance.models import Attendance, AttendanceStatus, Year, Month
from settings_app.utils import f_monthname
from django.urls import reverse
from onboard.models import Onboard, OnboardEmp, OnboardDet
from trip.models import TripEmp
from training.models import TrainingEmp
from perform.models import Eval, EvalDetA, EvalDetB, Evaluator, EvalDate, EvalFinalScore, EvalYear
from django.db.models import Sum
from django.contrib.auth.hashers import check_password
import urllib
import datetime as dt
from attendance.utils import sum_times, calculate_total_hours_week, get_weeks
from settings_app.models import IPGInfo
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
			return redirect('custom-uni-list')
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
			return redirect('custom-uni-list')
	else: form = EmpCusUniForm(instance=objects)
	context = {
		'form': form, 'page': 'add-university','employee':employee,
		'title': 'Altera Universidade', 'legend': 'Altera Universidade'
	}
	return render(request, 'employee_custom/form.html', context)