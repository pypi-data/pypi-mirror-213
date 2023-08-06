from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from contract.models import ContractType, Contract, EmpPosition, EmpSalary, EmpPlacement
from employee.models import Employee
from custom.models import Position

class DateInput(forms.DateInput):
	input_type = 'date'

class ManDepForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['employee','department','start_date','end_date','file','disp_number']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(status_id=1).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-3 mb-0'),
				Column('department', css_class='form-group col-md-4 mb-0'),
				Column('start_date', css_class='form-group col-md-2 mb-0'),
				Column('end_date', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class ManDepForm2(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['department','start_date','end_date', 'file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('department', css_class='form-group col-md-6 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class ManUnitForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['employee','unit','start_date','end_date','file','disp_number']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(status_id=1).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-4 mb-0'),
				Column('unit', css_class='form-group col-md-4 mb-0'),
				Column('start_date', css_class='form-group col-md-2 mb-0'),
				Column('end_date', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ManUnitForm2(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['unit','start_date','end_date', 'file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('unit', css_class='form-group col-md-6 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class ManDEForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['employee','de', 'unit','start_date','end_date','file','disp_number']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(status_id=1).all()
		self.helper = FormHelper()
		self.fields['de'].label = 'Presidente & Vice-Presidente'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-4 mb-0'),
				Column('de', css_class='form-group col-md-4 mb-0'),
				Column('unit', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-6 mb-0'),
				Column('end_date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ManDEForm2(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=True)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = EmpPosition
		fields = ['de','start_date','end_date','file','disp_number']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('de', css_class='form-group col-md-6 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ManEndForm(forms.ModelForm):
	terminate_date = forms.DateField(label="Data remata", widget=DateInput(), required=True)
	class Meta:
		model = EmpPosition
		fields = ['terminate_date','reason']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('terminate_date', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)