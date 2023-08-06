
============================
Django IPG HRMS contract
============================


Quick start
============


1. Add 'contract' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'contract'
    ]

2. Include the contract to project URLS like this::

    path('contract/', include('contract.urls')),

3. Run ``python manage.py migrate`` to create contract model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user