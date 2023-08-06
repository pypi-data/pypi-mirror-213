from django.apps import AppConfig


class ContractConfig(AppConfig):
	name = 'contract'

	def ready(self):
		import contract.signals