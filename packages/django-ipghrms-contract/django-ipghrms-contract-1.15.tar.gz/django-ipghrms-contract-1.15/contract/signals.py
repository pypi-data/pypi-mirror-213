from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contract, EmpSalary

@receiver(post_save, sender=Contract)
def create_contract(sender, instance, created, **kwargs):
	if created:
		EmpSalary.objects.create(id=instance.pk, employee=instance.employee, contract=instance, hashed=instance.hashed)