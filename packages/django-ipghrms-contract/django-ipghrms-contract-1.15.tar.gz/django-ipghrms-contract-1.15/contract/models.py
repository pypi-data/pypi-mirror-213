from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from custom.models import DE, Echelon, Grade, Unit, Department, Position
from employee.models import Employee
from settings_app.upload_utils import upload_contract, upload_place, upload_position,upload_organograma, upload_contract_end

class ContractType(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Category(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class BasicSalary(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="basicsalary")
	amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		template = '{0.category} - {0.amount}'
		return template.format(self)

class PositionSalary(models.Model):
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="positionsalary")
	amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	def __str__(self):
		template = '{0.position} - {0.amount}'
		return template.format(self)
###
class Contract(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contract')
	contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE, null=True, blank=True, related_name="contract")
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="contract")
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True, related_name="contract")
	echelon = models.ForeignKey(Echelon, on_delete=models.CASCADE, null=True, blank=True, related_name="contract")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="contract")	
	disp_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Dispatch Number")
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	terminate_date = models.DateField(null=True, blank=True)
	reason = models.CharField(max_length=200, null=True, blank=True)
	file = models.FileField(upload_to=upload_contract, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach ToR")
	file_end = models.FileField(upload_to=upload_contract_end, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anekso")
	is_active = models.BooleanField(default=True)
	is_lock = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.category}'
		return template.format(self)
	


class EmpContractToR(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='emptor')
	contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='emptor')
	tor = models.TextField()
	is_active = models.BooleanField(default=True, blank=True)
	is_lock = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.contract} - {0.employee}'
		return template.format(self)
	

class EmpSalary(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='empsalary')
	contract = models.OneToOneField(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='empsalary')
	amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	is_active = models.BooleanField(default=True, blank=True)
	is_lock = models.BooleanField(default=True, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.contract} - {0.amount}'
		return template.format(self)

class EmpPlacement(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="placement")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="placement")	
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="placement")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name="placement")
	de = models.ForeignKey(DE, on_delete=models.CASCADE, null=True, blank=True, related_name="placement")
	disp_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Dispatch Number")
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	terminate_date = models.DateField(null=True, blank=True)
	reason = models.CharField(max_length=200, null=True, blank=True)
	file = models.FileField(upload_to=upload_place, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Dispatch")
	is_active = models.BooleanField(default=True)
	is_confirm = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.de}/{0.unit}/{0.department}'
		return template.format(self)

class EmpPosition(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="empposition")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, related_name="empposition")
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="empposition")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name="empposition")
	de = models.ForeignKey(DE, on_delete=models.CASCADE, null=True, blank=True, related_name="empposition")
	disp_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Dispatch Number")
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	terminate_date = models.DateField(null=True, blank=True)
	reason = models.CharField(max_length=200, null=True, blank=True)
	file = models.FileField(upload_to=upload_position, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attachment")
	is_active = models.BooleanField(default=True)
	is_confirm = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.position}'
		return template.format(self)


class ActiveOrganogramaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Organograma(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Titulo")
	file = models.FileField(upload_to=upload_organograma, null=True, blank=True,
							validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attachment")
	is_active = models.BooleanField(default=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	objects = models.Manager() # The default manager
	active = ActiveOrganogramaManager() # The custom manager

	def save(self, *args, **kwargs):
		if self.is_active:
			# If the current instance is set to active, make all others inactive
			Organograma.objects.exclude(id=self.id).update(is_active=False)
			user = kwargs.pop('user', None)
			if user:
				self.user = user
			
		super().save(*args, **kwargs)

	def __str__(self):
		template = '{0.name} - {0.is_active}'
		return template.format(self)
