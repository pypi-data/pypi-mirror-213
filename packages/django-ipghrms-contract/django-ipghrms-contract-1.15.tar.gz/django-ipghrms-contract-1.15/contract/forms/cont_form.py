from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from contract.models import EmpContractToR, Contract, EmpPosition, EmpSalary, EmpPlacement
from employee.models import Employee
from custom.models import Position

class DateInput(forms.DateInput):
	input_type = 'date'

class ContractForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=False)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = Contract
		fields = ['contract_type','category','grade','echelon','start_date','end_date',\
			'file','disp_number', 'position']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['contract_type'].required = True
		self.fields['category'].required = True
		self.fields['start_date'].required = True
		self.fields['position'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('contract_type', css_class='form-group col-md-4 mb-0'),
				Column('category', css_class='form-group col-md-4 mb-0'),
				Column('position', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('grade', css_class='form-group col-md-3 mb-0'),
				Column('echelon', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-6 mb-0'),
				Column('file', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContractEndForm(forms.ModelForm):
	terminate_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = Contract
		fields = ['reason', 'terminate_date', 'file_end']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['terminate_date'].required = True
		self.fields['reason'].required = True

		self.helper.layout = Layout(
			Row(
				Column('terminate_date', css_class='form-group col-md-4 mb-0'),
				Column('reason', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file_end', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContractTernimateForm(forms.ModelForm):
	terminate_date = forms.DateField(widget=DateInput(), required=True)
	class Meta:
		model = Contract
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
###
class EmpSalaryForm(forms.ModelForm):
	class Meta:
		model = EmpSalary
		fields = ['amount']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('amount', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class EmpPlacementForm(forms.ModelForm):
	class Meta:
		model = EmpPlacement
		fields = ['de','unit','department','file','disp_number', 'position']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['position'].queryset = Position.objects.filter((Q(id=6)|Q(id=7)|Q(id=8)|Q(id=9))).all()
		self.fields['de'].label = 'Presidente & Vice-Presidente'
		self.fields['unit'].label = 'Divizaun'
		self.fields['department'].label = 'Ekipa'
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('de', css_class='form-group col-md-3 mb-0'),
				Column('unit', css_class='form-group col-md-3 mb-0'),
				Column('department', css_class='form-group col-md-3 mb-0'),
				Column('position', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('disp_number', css_class='form-group col-md-3 mb-0'),
				Column('file', css_class='form-group col-md-7 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EmpPlacementEndForm(forms.ModelForm):
	end_date = forms.DateField(widget=DateInput(), required=True)
	class Meta:
		model = EmpPlacement
		fields = ['end_date','reason']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class EmpContTorForm(forms.ModelForm):
	
	class Meta:
		model = EmpContractToR
		fields = ['tor']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'

		self.helper.layout = Layout(
			Row(
				Column('tor', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
