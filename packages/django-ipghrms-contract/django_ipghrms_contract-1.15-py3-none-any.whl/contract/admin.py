from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]    
admin.site.register(Category, CategoryAdmin)

class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]    
admin.site.register(ContractType, ContractTypeAdmin)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('employee','category',)
    search_fields = ['employee__first_name','employee__first_name','category__name',]    
admin.site.register(Contract, ContractAdmin)

class BasicSalaryAdmin(admin.ModelAdmin):
    list_display = ('category','amount',)
    search_fields = ['category__name','amount',]    
admin.site.register(BasicSalary, BasicSalaryAdmin)

class PositionSalaryAdmin(admin.ModelAdmin):
    list_display = ('position','amount')
    search_fields = ['position__name','amount']    
admin.site.register(PositionSalary, PositionSalaryAdmin)

class EmpSalaryAdmin(admin.ModelAdmin):
    list_display = ('contract','amount')
    search_fields = ['contract__employee__first_name','contract__employee__last_name','amount']    
admin.site.register(EmpSalary, EmpSalaryAdmin)

class EmpPlacementAdmin(admin.ModelAdmin):
    list_display = ('employee','de','unit','department')
    search_fields = ['employee__first_name','employee__last_name','de__name','unit__name','department__name']    
admin.site.register(EmpPlacement, EmpPlacementAdmin)

class EmpPositionAdmin(admin.ModelAdmin):
    list_display = ('employee','position')
    search_fields = ['employee__first_name','employee__last_name','position__name']    
admin.site.register(EmpPosition, EmpPositionAdmin)

class EmpContractToRAdmin(admin.ModelAdmin):
    list_display = ('contract','employee')
    search_fields = ['contract__employee__first_name','contract__employee__last_name','employee__first_name','employee__last_name']    
admin.site.register(EmpContractToR, EmpContractToRAdmin)

class OrganogramaAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Organograma, OrganogramaAdmin)
