from django.urls import path
from . import views

urlpatterns = [
	path('dash/', views.ContractDash, name="cont-dash"),
	path('list/', views.ContractList, name="cont-list"),
	path('no/list/', views.NoContractList, name="cont-no-list"),
	path('add/<str:hashid>/', views.ContractAdd, name="cont-add"),
	path('detail/<str:hashid>/', views.ContractDetail, name="cont-detail"),
	path('update/<str:hashid>/', views.ContractUpdate, name="cont-update"),
	path('renew/<str:hashid>/', views.ContractRenew, name="cont-renew"),
	path('pdf/<str:hashid>/', views.ContractPDF, name="cont-pdf"),
	path('lock/<str:hashid>/', views.ContractLock, name="cont-lock"),
	path('unlock/<str:hashid>/', views.ContractUnLock, name="cont-unlock"),
	path('end/<str:hashid>/', views.ContractEnd, name="cont-end"),
	path('view/end-file/<str:hashid>/', views.ViewContractTerminateFile, name="cont-view-end-file"),
	
	###
	path('assign/<str:hashid>/', views.EmpPlacementAdd, name="empplace-assign"),
	path('update/placement/<str:hashid>/', views.EmpPlacementUpdate, name="empplacement-update"),
	
	path('salary/list/', views.SalaryList, name="salary-list"),
	path('salary/no/', views.NoSalaryList, name="emp-no-salary"),
	path('salary/update/<str:hashid>/', views.SalaryUpdate, name="salary-update"),
	path('salary/detail/<str:hashid>/', views.SalaryDetail, {'check':False}, name="salary-detail"),
	path('salary/lock/<str:hashid>/', views.SalaryLock, name="salary-lock"),
	path('salary/unlock/<str:hashid>/', views.SalaryUnLock, name="salary-unlock"),
    
	path('history/emp/<str:hashid>/', views.ContractHistList, name="contract-hist-emp"),
	# path('history/detail/<str:hashid>/', views.ContractHistDetail, name="contract-hist-detail"),

	path('chart/dash/', views.ContChartDash, name="cont-chart-dash"),
	path('organogram/<int:pk>/file/', views.OrganogramFileView.as_view(), name='organogram_file'),


	###TOR####
	path('tor/list/<str:hashid>/<str:hashid2>/', views.EmpToRList, name="tor-list"),
	path('tor/add/<str:hashid>/<str:hashid2>/', views.EmpToRAdd, name="tor-add"),
	path('tor/update/<str:hashid>/<str:hashid2>/<str:hashid3>/', views.EmpToRUpdate, name="tor-update"),
	path('tor/delete/<str:hashid>/<str:hashid2>/<str:hashid3>/', views.EmpToRDelete, name="tor-delete"),
	path('tor/lock/<str:hashid>/<str:hashid2>/', views.EmpToRlock, name="tor-lock"),



	# path('reports/category/<str:pk>/', views.RContractCatList, name="report-cont-cat"),
    # path('reports/type/<str:pk>/', views.RContractTyteList, name="report-cont-type"),
    # path('reports/position/<str:pk>/', views.RPositionList, name="report-position"),
	# path('reports/gab/position/<str:pk>/', views.RGabPositionList, name="report-position-gab"),
	# path('reports/min/position/<str:pk>/', views.RMinPositionList, name="report-position-min"),

	# path('dg/dash/', views.ContractDGDash, name="contract-dg-dash"),
	# path('dg/contract/list/', views.ContractDGList, name="contract-dg-list"),
	# path('dg/salary/list/', views.SalaryDGList, name="salary-dg-list"),
	# path('dg/salary/detail/<str:hashid>/', views.SalaryDGDetail, name="salary-dg-detail"),
	# path('dg/category/<str:pk>/', views.RContractCatDGList, name="report-cont-dg-cat"),
    # path('dg/type/<str:pk>/', views.RContractTyteDGList, name="report-cont-dg-type"),
    # path('dg/position/<str:pk>/', views.RPositionDGList, name="report-dg-position"),

	# path('div/dash/', views.ContractDivDash, name="contract-div-dash"),
	# path('div/contract/list/', views.ContractDivList, name="contract-div-list"),
	# path('div/salary/list/', views.SalaryDivList, name="salary-div-list"),
	# path('div/category/<str:pk>/', views.RContractCatDivList, name="report-cont-div-cat"),
    # path('div/type/<str:pk>/', views.RContractTyteDivList, name="report-cont-div-type"),
    # path('div/position/<str:pk>/', views.RPositionDivList, name="report-div-position"),
]